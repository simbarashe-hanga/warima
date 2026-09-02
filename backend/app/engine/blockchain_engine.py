# backend/app/engine/blockchain_engine.py

from typing import Dict, Any


class BlockchainEngine:
    """
    Handles blockchain-related conversation flows.

    IMPORTANT:
    This engine does not initialize blockchain services during
    application startup.

    Blockchain services are loaded only when a blockchain operation
    is actually requested.
    """

    def __init__(self):
        """
        Keep initialization lightweight.

        Do NOT create:
            SmartAccountService
            PigService
            TokenService
            ContractService

        here.

        This allows the API to start before blockchain contracts
        and ABIs have been compiled/deployed.
        """

        self._smart_account_service = None
        self._pig_service = None
        self._token_service = None
        self._portfolio_service = None

    # ------------------------------------------------------------------
    # LAZY SERVICES
    # ------------------------------------------------------------------

    @property
    def smart_account_service(self):
        """
        Load SmartAccountService only when required.
        """

        if self._smart_account_service is None:
            from app.services.blockchain.smart_account_service import (
                SmartAccountService
            )

            self._smart_account_service = SmartAccountService()

        return self._smart_account_service

    @property
    def pig_service(self):
        """
        Load PigService only when required.
        """

        if self._pig_service is None:
            from app.services.blockchain.pig_service import PigService

            self._pig_service = PigService()

        return self._pig_service

    @property
    def token_service(self):
        """
        Load TokenService only when required.
        """

        if self._token_service is None:
            from app.services.blockchain.token_service import TokenService

            self._token_service = TokenService()

        return self._token_service

    @property
    def portfolio_service(self):
        """
        Load PortfolioService only when required.
        """

        if self._portfolio_service is None:
            from app.services.portfolio.portfolio_service import (
                PortfolioService
            )

            self._portfolio_service = PortfolioService()

        return self._portfolio_service

    # ------------------------------------------------------------------
    # ROUTING
    # ------------------------------------------------------------------

    async def handle(
        self,
        message: str,
        intent: Dict[str, Any],
        session_context: Dict[str, Any],
        member_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Process blockchain-related messages.

        This method only determines which blockchain operation should
        handle the message.
        """

        user_id = session.get("user_id")

        if not user_id:
            return {
                "message": "Please complete onboarding first.",
                "type": "text",
                "context_update": {},
            }

        if flow == "blockchain/create_smart_account":
            return await self._handle_create_smart_account(
                session,
                message,
            )

        if flow == "blockchain/deploy_smart_account":
            return await self._handle_deploy_smart_account(
                session,
                message,
            )

        if flow == "blockchain/recover_smart_account":
            return await self._handle_recover_smart_account(
                session,
                message,
            )

        if flow == "blockchain/portfolio":
            return await self._handle_portfolio(
                session,
                message,
            )

        if flow == "blockchain/buy_pig":
            return await self._handle_buy_pig(
                session,
                message,
            )

        if flow == "blockchain/sell_pig":
            return await self._handle_sell_pig(
                session,
                message,
            )

        if flow == "blockchain/record_health":
            return await self._handle_record_health(
                session,
                message,
            )

        if flow == "blockchain/view_pigs":
            return await self._handle_view_pigs(
                session,
                message,
            )

        if flow == "blockchain/transaction_status":
            return await self._handle_transaction_status(
                session,
                message,
            )

        return {
            "message": (
                "Blockchain command not recognized."
            ),
            "type": "text",
            "context_update": {},
        }

    # ------------------------------------------------------------------
    # SMART ACCOUNT
    # ------------------------------------------------------------------

    async def _handle_create_smart_account(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:
        """
        Create a smart account.

        The actual operation belongs to SmartAccountService.
        """

        user_id = session.get("user_id")

        if not user_id:
            return {
                "message": "Please complete onboarding first.",
                "type": "text",
                "context_update": {},
            }


        result = await self.smart_account_service.create_user_account(
            user_id=user_id
        )

        if not result.get("success"):
            return {
                "message": (
                    "Failed to create smart account: "
                    f"{result.get('error', 'Unknown error')}"
                ),
                "type": "text",
                "context_update": {},
            }

        user = result.get("user", {})

        address = user.get("smart_account_address", "")

        return {
            "message": (
                "*Smart Account Created!*\n\n"
                f"Account: {address[:10]}...\n\n"
                "Your account is now ready for transactions."
            ),
            "type": "text",
            "context_update": {
                "blockchain": {
                    "active": False,
                    "smart_account_created": True,
                    "address": address,
                }
            },
        }

    # ------------------------------------------------------------------
    # PLACEHOLDER FLOWS
    # ------------------------------------------------------------------

    async def _handle_deploy_smart_account(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self._not_implemented(
            "Smart account deployment"
        )

    async def _handle_recover_smart_account(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self._not_implemented(
            "Smart account recovery"
        )

    async def _handle_portfolio(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self._not_implemented(
            "Blockchain portfolio"
        )

    async def _handle_buy_pig(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self._not_implemented(
            "Pig purchase"
        )

    async def _handle_sell_pig(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self._not_implemented(
            "Pig sale"
        )

    async def _handle_record_health(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self._not_implemented(
            "Pig health recording"
        )

    async def _handle_view_pigs(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self._not_implemented(
            "Pig portfolio"
        )

    async def _handle_transaction_status(
        self,
        session: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self._not_implemented(
            "Blockchain transaction status"
        )

    # ------------------------------------------------------------------
    # RESPONSE HELPERS
    # ------------------------------------------------------------------

    def _not_implemented(self, operation: str) -> Dict[str, Any]:
        """
        Return a safe response for blockchain functionality that is
        not yet ready.
        """

        return {
            "message": (
                f"{operation} is not available yet. "
                "Blockchain infrastructure is still being configured."
            ),
            "type": "text",
            "context_update": {},
        }
