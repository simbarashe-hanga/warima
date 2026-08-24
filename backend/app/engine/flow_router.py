# backend/app/engine/flow_router.py

from typing import Dict, Any

from app.engine.onboarding_engine import OnboardingEngine
from app.engine.wallet_engine import WalletEngine
from app.engine.stokvel_engine import StokvelEngine
from app.engine.investment_engine import InvestmentEngine
from app.engine.kyc_engine import KYC


class FlowRouter:
    """
    Routes incoming user messages to the appropriate conversation engine.

    Responsibilities:
        - Determine the user's active conversation flow
        - Route the message to that flow's engine
        - Return the engine response

    Non-responsibilities:
        - Database operations
        - Wallet creation
        - Blockchain transactions
        - Portfolio calculations
        - Investment logic
        - KYC/business logic
        - WhatsApp communication
    """

    def __init__(self):
        # Conversation engines
        self.onboarding_engine = OnboardingEngine()
        self.wallet_engine = WalletEngine()
        self.stokvel_engine = StokvelEngine()
        self.investment_engine = InvestmentEngine()
        self.kyc_engine = KYC()

    #-------------------------------------------------------------------
    # Lazy blockchain initialization
    #-------------------------------------------------------------------

    @property
    def blockchain_engine(self):
        """
        Initialize BlockchainEngine only when a blockchain flow
        is actually requested.
        """
        if self._blockchain_engine is None:
            from app.engine.blockchain_engine import BlockchainEngine

            self._blockchain_engine

    # ------------------------------------------------------------------
    # FLOW DETECTION
    # ------------------------------------------------------------------

    def current_flow(self, session: Dict[str, Any]) -> str:
        """
        Determine the currently active conversation flow.

        The session context is the source of truth for conversational state.

        Priority:
            1. Onboarding
            2. KYC
            3. Wallet
            4. Stokvel
            5. Investment
            6. Blockchain
            7. Default
        """

        context = session.get("context", {})

        # Blockchain
        blockchain = context.get("blockchain", {})
        if blockchain.get("active"):
            return self._determine_blockchain_flow(blockchain)

        # --------------------------------------------------------------
        # 1. ONBOARDING
        # --------------------------------------------------------------

        onboarding = context.get("onboarding", {})

        if onboarding.get("active"):
            return "onboarding"

        # --------------------------------------------------------------
        # 2. KYC
        # --------------------------------------------------------------

        kyc = context.get("kyc", {})

        if kyc.get("active"):
            return "kyc"

        # --------------------------------------------------------------
        # 3. WALLET
        # --------------------------------------------------------------

        wallet = context.get("wallet", {})

        if wallet.get("active"):
            return "wallet"

        # --------------------------------------------------------------
        # 4. STOKVEL
        # --------------------------------------------------------------

        stokvel = context.get("stokvel", {})

        if stokvel.get("active"):
            return "stokvel"

        # --------------------------------------------------------------
        # 5. INVESTMENT
        # --------------------------------------------------------------

        investment = context.get("investment", {})

        if investment.get("active"):
            return "investment"

        # --------------------------------------------------------------
        # 6. DEFAULT
        # --------------------------------------------------------------
        transaction = context.get("transaction", {})
        if transaction.get("active"):
            return "transaction_monitor"

        return "default"

    # ------------------------------------------------------------------
    # BLOCKCHAIN FLOW DETECTION
    # ------------------------------------------------------------------

    def _determine_blockchain_flow(self, blockchain: Dict[str, Any]) -> str:
        """
        Determine the active blockchain sub-flow.

        This method only determines routing.
        Blockchain operations themselves belong to BlockchainEngine
        and its underlying services.
        """

        action = blockchain.get("action", "")

        blockchain_flows = {
            "create_smart_account": "blockchain/create_smart_account",
            "deploy_smart_account": "blockchain/deploy_smart_account",
            "recover_smart_account": "blockchain/recover_smart_account",
            "view_portfolio": "blockchain/portfolio",
            "buy_pig": "blockchain/buy_pig",
            "sell_pig": "blockchain/sell_pig",
            "record_health": "blockchain/record_health",
            "view_pigs": "blockchain/view_pigs",
            "transaction_status": "blockchain/transaction_status",
        }

        return blockchain_flows.get(
            action,
            "blockchain/default"
        )

    # ------------------------------------------------------------------
    # MESSAGE ROUTING
    # ------------------------------------------------------------------

    async def route_message(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:
        """
        Route a user message to the appropriate conversation engine.

        Args:
            session:
                Current user session and conversation context.

            message:
                Incoming user message.

        Returns:
            Standardized engine response.
        """

        flow = self.current_flow(session)

        # --------------------------------------------------------------
        # ONBOARDING
        # --------------------------------------------------------------

        if flow == "onboarding":
            return await self._route_onboarding(
                session,
                message
            )

        # --------------------------------------------------------------
        # KYC
        # --------------------------------------------------------------

        if flow == "kyc":
            return await self._route_kyc(
                session,
                message
            )

        # --------------------------------------------------------------
        # WALLET
        # --------------------------------------------------------------

        if flow == "wallet":
            return await self._route_wallet(
                session,
                message
            )

        # --------------------------------------------------------------
        # STOKVEL
        # --------------------------------------------------------------

        if flow == "stokvel":
            return await self._route_stokvel(
                session,
                message
            )

        # --------------------------------------------------------------
        # INVESTMENT
        # --------------------------------------------------------------

        if flow == "investment":
            return await self._route_investment(
                session,
                message
            )

        # --------------------------------------------------------------
        # BLOCKCHAIN
        # --------------------------------------------------------------

        if flow.startswith("blockchain/"):
            return await self.blockchain_engine.process(
                session,
                message,
                flow
            )

        return self._default_response(message)

    # ------------------------------------------------------------------
    # DEFAULT
    # ------------------------------------------------------------------
    def _default_response(self, message:str) -> Dict:
        message_lower = message.lower().strip()
        if message_lower in {
            "hi",
            "hello",
            "hey",
            "start",
            "ndeipi"
        }:
            return {
                "message": (
                    "Hello! Welcome to Warima Wealth.\n\n"
                    "Type *Help* to see what I can do."
                ),
                "type": "text",
                "context_update": {}
            }

        if message_lower in {
            "help",
            "menu",
            "?"
        }:
            return {
                "message": (
                    "*Warima Wealth*\n\n"
                    "Onboard - Create your account\n"
                    "Wallet - Manage your wallet\n"
                    "Portfolio - View your portfolio\n"
                    "Stokvel - Manage your stokvel\n"
                    "KYC - Verify your identity\n"
                    "Help - Show this menu"
                ),
                "type": "text",
                "context_update": {}
            }

        if message_lower == "onboard":
            return {
                "message": "Let's get you started. Type *Start* to begin onboarding.",
                "type": "text",
                "context_update": {
                    "onboarding": {
                        "active": True,
                        "step": "start"
                    }
                }
            }

        if message_lower == "wallet":
            return {
                "message": "Opening your wallet...",
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": True,
                        "step": "start"
                    }
                }
            }

        return {
            "message": (
                f"I didn't understand '{message}'.\n\n"
                "Type *Help* to see available commands."
            ),
            "type": "text",
            "context_update": {}
        }
