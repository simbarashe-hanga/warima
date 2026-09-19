# backend/app/engine/wallet_engine.py

from typing import Dict, Any

from app.services.identity.session_manager import SessionManager

from app.services.wallet.wallet_service import WalletService
from app.services.wallet.wallet_balance_service import WalletBalanceService
from app.services.wallet.contribution_service import ContributionService

from app.services.treasury.treasury_service import TreasuryService
from app.services.treasury.treasury_balance_service import TreasuryBalanceService

from app.models.wallet import Wallet
from app.models.stokvel import Stokvel


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
        db=None,
    ) -> Dict[str, Any]:
        """
        Process a wallet conversation.

        The wallet engine currently operates on session state.
        User/account lookup and blockchain operations should be
        handled by the appropriate service layer.
        """

        intent_name = intent.get("intent")

        if intent_name == "wallet.balance":
            member_account = member_context.get("member_account")

            if db is None:
                return {
                    "message": (
                        "I'm unable to access your wallet right now."
                        "Please try again."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            if member_account is None:
                return {
                    "message": (
                        "I couldn't find your member account."
                        "Please complete your account setup first."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            wallet = WalletService.get_wallet(
                db=db,
                member_account=member_account,
            )

            wallet_balance = (
                WalletBalanceService.get_balance(wallet)
                if wallet is not None
                else 0
            )

            selected_stokvel_id = (
                SessionManager.selected_stokvel_id(session)
            )

            if not selected_stokvel_id:
                return {
                    "message": (
                        "*Your Wallet*\\n"
                        f"R{wallet_balance:,.2f} ZAR\n\n"
                        "No stokvel is currently selected."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            stokvel = (
                db.query(Stokvel)
                .filter(Stokvel.id == selected_stokvel_id)
                .first()
            )

            if stokvel is None:
                return {
                    "message": (
                        "*Your Wallet*\n"
                        f"R{wallet_balance:,.2f} ZAR\n\n"
                        "The selected stokvel could not be found."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            treasury = (
                TreasuryService.get_treasury_by_stokvel(
                    db=db,
                    stokvel_id=selected_stokvel_id,
                )
            )

            if treasury is None:
                return {
                    "message": (
                        "*Your Wallet*\n"
                        f"R{wallet_balance:,.2f} ZAR\n\n"
                        f"*{stokvel.name}*\n"
                        "Treasury is not configured yet."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            treasury_balance = (
                TreasuryBalanceService.get_balance(
                    db=db,
                    treasury=treasury,
                )
            )

            return {
                "message": (
                    "*Your Wallet*\n"
                    f"R{wallet_balance:,.2f} ZAR\n\n"
                    f"*{stokvel.name}*\n"
                    f"Treasury: R{treasury_balance:,.2f} "
                    f"{treasury.denomination.value}"
                ),
                "type": "text",
                "context_update": {},
            }

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
                member_context,
                db,
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
        member_context,
        db,
    ):
        """
        Handle contribution confirmation.

        Creates a pending wallet transaction.
        Does not credit the wallet or execute blockchain operations.
        """
        confirmation = message.strip().lower()

        selected_stokvel_id = (
            SessionManager.selected_stokvel_id(session)
        )
        
        amount = SessionManager.wallet_amount(session)

        stokvel_name = None

        if selected_stokvel_id and db is not None:
            from app.services.stokvel.stokvel_service import StokvelService

            stokvel_service = StokvelService(db)
            stokvel = stokvel_service.get_stokvel(
                selected_stokvel_id
            )

            if stokvel:
                stokvel_name = stokvel.name

            if stokvel_name:
                message = (
                    f"Please confirm your contribution of "
                    f"*R{amount:.2f}* to *{stokvel_name}*.\n\n"
                    "Reply *1* to confirm or *2* to cancel."
                )
            else:
                message = (
                    f"Please confirm your contribution of "
                    f"*R{amount:.2f}*.\n\n"
                    "Reply *1* to confirm or *2* to cancel."
                )


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

        if confirmation in {"1", "yes", "y"}:
            member_account = member_context.get("member_account")

            if db is None:
                raise RuntimeError("Database session is required")

            try:
                transaction = WalletService.create_contribution(
                    db=db,
                    member_account=member_account,
                    amount=amount,
                    stokvel_id=selected_stokvel_id,
                )

                transaction = ContributionService.complete_contribution(
                    db=db,
                    transaction=transaction,
                )

            except ValueError as exc:
                return {
                    "message": str(exc),
                    "type": "text",
                    "context_update": {},
                }

            SessionManager.finish_wallet(session)

            return {
                "message": (
                    f"Contribution of *R{amount:,.2f}* completed successfully.\n\n"
                    f"Reference: *{transaction.reference}*\n\n"
                    "Status: *Completed*"
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
