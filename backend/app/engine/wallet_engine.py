# backend/app/engine/wallet_engine.py

from typing import Dict, Any

from app.services.identity.session_manager import SessionManager


class WalletEngine:
    """
    Handles wallet-related conversation flows.

    The engine is responsible for conversation state and routing.
    Actual wallet/blockchain operations belong to services.

    Important:
        Blockchain services are NOT initialized here.
        This prevents API startup from requiring blockchain
        contract artifacts such as ABIs.
    """

    def __init__(self):
        self._smart_account_service = None
        self._token_service = None

    @property
    def smart_account_service(self):
        if self._smart_account_service is None:
            from app.services.blockchain.smart_account_service import (
                SmartAccountService
            )

            self._smart_account_service = SmartAccountService()

        return self._smart_account_service

    @property
    def token_service(self):
        if self._token_service is None:
            from app.services.blockchain.token_service import TokenService

            self._token_service = TokenService()

        return self._token_service

    async def handle(
        self,
        message: str,
        intent: Dict[str, Any],
        session,
        member_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Process a wallet conversation.

        The wallet engine currently operates on session state.
        User/account lookup and blockchain operations should be
        handled by the appropriate service layer.
        """

        step = SessionManager.wallet_step(session)

        if step == "awaiting_amount":
            return await self._handle_amount_input(
                session,
                message,
            )

        if step == "awaiting_confirmation":
            return await self._handle_confirmation(
                session,
                message,
            )

        if step == "chatting":
            return self._handle_chat_mode(
                session,
                message,
            )

        return self._start_wallet_flow(session)

    # ------------------------------------------------------------------
    # AMOUNT
    # ------------------------------------------------------------------

    async def _handle_amount_input(
        self,
        session,
        message,
    ):
        """
        Handle contribution amount input.

        No blockchain operation happens here.
        """

        try:
            amount = float(message.strip())

        except (ValueError, AttributeError):
            return {
                "message": "Please enter a valid number.",
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": True,
                        "step": "awaiting_amount",
                    }
                },
            }

        if amount <= 0:
            return {
                "message": "Please enter a valid amount greater than 0.",
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": True,
                        "step": "awaiting_amount",
                    }
                },
            }

        SessionManager.set_wallet_amount(
            session,
            amount,
        )

        SessionManager.set_wallet_step(
            session,
            "awaiting_confirmation",
        )

        return {
            "message": (
                f"Confirm R{amount:,.2f}?\n\n"
                "Reply 1 to confirm or 2 to cancel."
            ),
            "type": "text",
            "context_update": {
                "wallet": {
                    "active": True,
                    "step": "awaiting_confirmation",
                    "amount": amount,
                }
            },
        }

    # ------------------------------------------------------------------
    # CONFIRMATION
    # ------------------------------------------------------------------

    async def _handle_confirmation(
        self,
        session,
        message,
    ):
        """
        Handle contribution confirmation.

        Actual contribution processing will be delegated to a
        wallet/finance service once the user/account architecture
        is connected.
        """

        amount = SessionManager.wallet_amount(session)

        if amount is None:
            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "I couldn't find your contribution amount. "
                    "Please type 'contribute' to start again."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        if message.strip().lower() in {"1", "yes", "y"}:

            # Business operation intentionally not implemented here.
            #
            # Future architecture:
            #
            # WalletEngine
            #       ↓
            # WalletService
            #       ↓
            # Finance / Ledger
            #       ↓
            # BlockchainService
            #
            # For now we acknowledge the command without pretending
            # that a blockchain transaction occurred.

            SessionManager.finish_wallet(session)

            return {
                "message": (
                    f"Contribution of R{amount:,.2f} "
                    "has been requested.\n\n"
                    "Wallet processing is currently being configured."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        SessionManager.finish_wallet(session)

        return {
            "message": (
                "Cancelled.\n\n"
                "Type 'contribute' to start again."
            ),
            "type": "text",
            "context_update": {
                "wallet": {
                    "active": False,
                }
            },
        }

    # ------------------------------------------------------------------
    # CHAT MODE
    # ------------------------------------------------------------------

    def _handle_chat_mode(
        self,
        session,
        message,
    ):
        """
        Handle general wallet conversation.
        """

        return {
            "message": (
                f"You said: {message}\n\n"
                "Type 'help' to see available wallet commands."
            ),
            "type": "text",
            "context_update": {
                "wallet": {
                    "active": True,
                    "step": "chatting",
                }
            },
        }

    # ------------------------------------------------------------------
    # START FLOW
    # ------------------------------------------------------------------

    def _start_wallet_flow(
        self,
        session,
    ):
        """
        Start the wallet conversation.
        """

        SessionManager.start_wallet(
            session,
            step="awaiting_amount",
        )

        return {
            "message": (
                "*Wallet Management*\n\n"
                "How much would you like to contribute?"
            ),
            "type": "text",
            "context_update": {
                "wallet": {
                    "active": True,
                    "step": "awaiting_amount",
                }
            },
        }
