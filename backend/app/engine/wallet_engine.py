# backend/app/engine/wallet_engine.py

import uuid
from decimal import Decimal

from typing import Dict, Any

from app.services.identity.session_manager import SessionManager

from app.services.wallet.wallet_service import WalletService
from app.services.wallet.wallet_balance_service import WalletBalanceService
from app.services.wallet.contribution_service import ContributionService

from app.services.treasury.treasury_service import TreasuryService
from app.services.treasury.treasury_balance_service import TreasuryBalanceService

from app.models.wallet import Wallet
from app.models.stokvel import Stokvel

from app.models.enums import (
    WalletTransactionStatus,
    WalletTransactionType,
    TreasuryDenomination,
)

from app.models.wallet_transaction import WalletTransaction

from app.services.blockchain.blockchain_accounts.blockchain_account_service import (
    BlockchainAccountService,
)

from app.services.settlement.settlement_orchestrator import (
    SettlementOrchestrator,
)

from app.services.payments.payment_service import PaymentService
from app.services.payments.payment_registry import payment_provider_registry



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

        if intent_name == "wallet.solana":
            return self._start_solana_flow(session)

        if intent_name == "wallet.deposit":
            return self._start_deposit_flow(session)

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
                        "*Your Wallet*\n"
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

        if step == "solana_confirmation":
            return await self._handle_solana_confirmation(
                session,
                message,
                member_context,
                db,
            )

        if step == "deposit_awaiting_amount":
            return await self._handle_deposit_amount(
                session,
                message,
                member_context,
                db,
            )

        if step == "deposit_awaiting_email":
            return await self._handle_deposit_email(
                session,
                message,
                member_context,
                db,
            )

        if step == "awaiting_amount":
            return await self._handle_amount_input(
                session,
                message,
                db,
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
    # DEPOSIT
    # ------------------------------------------------------------------

    def _start_deposit_flow(
        self,
        session,
    ):
        """
        Start the external wallet funding flow.

        The actual wallet credit only happens after the payment
        provider confirms successful payment through the webhook.
        """

        SessionManager.start_wallet(
            session,
            step="deposit_awaiting_amount",
        )

        return {
            "message": (
                "How much would you like to deposit into your wallet?\n\n"
                "Enter the amount in ZAR."
            ),
            "type": "text",
            "context_update": {
                "wallet": {
                    "active": True,
                    "step": "deposit_awaiting_amount",
                    "amount": None,
                }
            },
        }

    # ------------------------------------------------------------------
    # DEPOSIT AMOUNT
    # ------------------------------------------------------------------

    async def _handle_deposit_amount(
        self,
        session,
        message,
        member_context,
        db,
    ):
        """
        Initialize an external wallet funding payment.

        This creates a Paystack payment but does NOT credit the wallet.
        Wallet funding happens only after the verified provider webhook.
        """

        if db is None:
            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "I'm unable to start the deposit right now. "
                    "Please try again."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        member_account = member_context.get("member_account")

        if member_account is None:
            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "I couldn't find your member account. "
                    "Please complete your account setup first."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        try:
            amount = Decimal(message.strip())
        except (ValueError, AttributeError):
            return {
                "message": "Please enter a valid ZAR amount.",
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": True,
                        "step": "deposit_awaiting_amount",
                    }
                },
            }

        if amount <= 0:
            return {
                "message": "Please enter an amount greater than R0.",
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": True,
                        "step": "deposit_awaiting_amount",
                    }
                },
            }

        user = member_account.user

        if user is None:
            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "I couldn't find your user profile. "
                    "Please try again."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        user_email = (
            user.email.strip()
            if user.email
            else None
        )

        if not user_email:
            SessionManager.set_wallet_amount(
                session,
                str(amount),
            )

            SessionManager.set_wallet_step(
                session,
                "deposit_awaiting_email",
            )

            return {
                "message": (
                    "I need your email address to create the "
                    "secure payment.\n\n"
                    "Please enter your email address."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": True,
                        "step": "deposit_awaiting_email",
                        "amount": str(amount),
                    }
                },
            }

        try:
            provider = payment_provider_registry.get("paystack")

            payment = PaymentService.create_payment(
                db=db,
                provider=provider,
                member_account=member_account,
                amount=amount,
                currency="ZAR",
                email=user_email,
            )

            db.commit()

        except ValueError as exc:
            db.rollback()

            SessionManager.finish_wallet(session)

            return {
                "message": str(exc),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        except Exception:
            db.rollback()

            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "I couldn't create the payment right now. "
                    "Please try again."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        SessionManager.finish_wallet(session)

        if not payment.payment_url:
            return {
                "message": (
                    "The payment was created, but no checkout link "
                    "was returned. Please try again."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        return {
            "message": (
                f"Your *R{amount:,.2f}* wallet deposit is ready.\n\n"
                "Complete your payment here:\n"
                f"{payment.payment_url}\n\n"
                "Your wallet will be credited after the payment is "
                "successfully confirmed."
            ),
            "type": "text",
            "context_update": {
                "wallet": {
                    "active": False,
                }
            },
        }

    # ------------------------------------------------------------------
    # DEPOSIT EMAIL
    # ------------------------------------------------------------------

    async def _handle_deposit_email(
        self,
        session,
        message,
        member_context,
        db,
    ):
        """
        Complete deposit payment initialization using a
        payment-specific email address.

        The email is used only for payment initialization.
        It does not update the user's profile.
        """

        if db is None:
            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "I'm unable to start the deposit right now. "
                    "Please try again."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        member_account = member_context.get("member_account")

        if member_account is None:
            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "I couldn't find your member account. "
                    "Please complete your account setup first."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        amount = SessionManager.wallet_amount(session)

        if amount is None:
            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "I couldn't find your deposit amount. "
                    "Please type 'deposit' to start again."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        amount = Decimal(str(amount))

        email = message.strip().lower()

        if "@" not in email or "." not in email.split("@")[-1]:
            return {
                "message": (
                    "Please enter a valid email address."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": True,
                        "step": "deposit_awaiting_email",
                        "amount": amount,
                    }
                },
            }

        try:
            provider = payment_provider_registry.get("paystack")

            payment = PaymentService.create_payment(
                db=db,
                provider=provider,
                member_account=member_account,
                amount=amount,
                currency="ZAR",
                email=email,
            )

            db.commit()

        except ValueError as exc:
            db.rollback()
            SessionManager.finish_wallet(session)

            return {
                "message": str(exc),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        except Exception:
            db.rollback()
            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "I couldn't create the payment right now. "
                    "Please try again."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        SessionManager.finish_wallet(session)

        if not payment.payment_url:
            return {
                "message": (
                    "The payment was created, but no checkout link "
                    "was returned. Please try again."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        return {
            "message": (
                f"Your *R{amount:,.2f}* wallet deposit is ready.\n\n"
                "Complete your payment here:\n"
                f"{payment.payment_url}\n\n"
                "Your wallet will be credited after the payment is "
                "successfully confirmed."
            ),
            "type": "text",
            "context_update": {
                "wallet": {
                    "active": False,
                }
            },
        }

    # ------------------------------------------------------------------
    # AMOUNT
    # ------------------------------------------------------------------

    async def _handle_amount_input(
        self,
        session,
        message,
        db,
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

        selected_stokvel_id = SessionManager.selected_stokvel_id(
            session
        )

        is_solana_contribution = False

        if selected_stokvel_id:
            from app.services.treasury.treasury_service import TreasuryService
            from app.models.enums import TreasuryDenomination

            treasury = TreasuryService.get_treasury_by_stokvel(
                db,
                selected_stokvel_id,
            )

            if (
                treasury is not None
                and treasury.denomination == TreasuryDenomination.SOL
                and treasury.rail.value == "SOLANA"
            ):
                is_solana_contribution = True

        if is_solana_contribution:
            confirmation_message = (
                f"Confirm {amount:,.4f} SOL?\n\n"
                "Reply 1 to confirm or 2 to cancel."
            )
        else:
            confirmation_message = (
                f"Confirm R{amount:,.2f}?\n\n"
                "Reply 1 to confirm or 2 to cancel."
            )

        return {
            "message": confirmation_message,
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

        ZAR contributions use the existing wallet/treasury accounting
        flow.

        SOL contributions to an on-chain stokvel use the generic
        settlement layer and settle from the member's Solana account
        to the stokvel treasury address.
        """
        confirmation = message.strip().lower()

        selected_stokvel_id = (
            SessionManager.selected_stokvel_id(session)
        )

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

        stokvel_name = None
        treasury = None
        is_solana_contribution = False

        if selected_stokvel_id and db is not None:
            from app.services.stokvel.stokvel_service import StokvelService

            stokvel_service = StokvelService(db)
            stokvel = stokvel_service.get_stokvel(
                selected_stokvel_id
            )

            if stokvel:
                stokvel_name = stokvel.name

            treasury = TreasuryService.get_treasury_by_stokvel(
                db,
                selected_stokvel_id,
            )

            if (
                treasury is not None
                and treasury.denomination == TreasuryDenomination.SOL
                and treasury.rail.value == "SOLANA"
            ):
                is_solana_contribution = True

        if is_solana_contribution:
            confirmation_message = (
                f"Please confirm your contribution of "
                f"*{amount:.4f} SOL*"
            )

        else:
            confirmation_message = (
                f"Please confirm your contribution of "
                f"*R{amount:.2f}*"
            )

        if stokvel_name:
            confirmation_message += (
                f" to *{stokvel_name}*.\n\n"
                "Reply *1* to confirm or *2* to cancel."
            )
        else:
            confirmation_message += (
                ".\n\n"
                "Reply *1* to confirm or *2* to cancel."
            )

        if confirmation in {"1", "yes", "y"}:
            member_account = member_context.get("member_account")

            if db is None:
                raise RuntimeError("Database session is required")

            try:
                if is_solana_contribution:
                    if treasury is None:
                        raise ValueError(
                            "The selected digital stokvel has no treasury."
                        )

                    if not treasury.blockchain_address:
                        raise ValueError(
                            "The selected digital stokvel has no blockchain treasury address."
                        )

                    transaction = WalletService.create_contribution(
                        db=db,
                        member_account=member_account,
                        amount=amount,
                        stokvel_id=selected_stokvel_id,
                        currency="SOL",
                    )

                    result = await SettlementOrchestrator.settle(
                        db=db,
                        transaction=transaction,
                        destination=treasury.blockchain_address,
                    )

                    if not result.succeeded:
                        raise ValueError(
                            result.error
                            or "Solana contribution settlement failed."
                        )

                else:
                    transaction = WalletService.create_contribution(
                        db=db,
                        member_account=member_account,
                        amount=amount,
                        stokvel_id=selected_stokvel_id,
                        currency="ZAR",
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

            if is_solana_contribution:
                return {
                    "message": (
                        f"Contribution of *{amount:,.4f} SOL* "
                        f"to *{stokvel_name or 'digital stokvel'}* "
                        "completed successfully.\n\n"
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
    # SOLANA SETTLEMENT
    # ------------------------------------------------------------------

    def _start_solana_flow(
        self,
        session,
    ):
        """
        Start a real Solana Devnet settlement flow.

        This is intentionally separate from the ZAR contribution flow.
        """

        SessionManager.start_wallet(
            session,
            step="solana_confirmation",
        )

        SessionManager.set_wallet_amount(
            session,
            0.01,
        )

        return {
            "message": (
                "*Solana Devnet Settlement*\n\n"
                "This will execute a real *0.01 SOL* transfer "
                "on Solana Devnet.\n\n"
                "Reply *1* to confirm or *2* to cancel."
            ),
            "type": "text",
            "context_update": {
                "wallet": {
                    "active": True,
                    "step": "solana_confirmation",
                    "amount": 0.01,
                }
            },
        }

    async def _handle_solana_confirmation(
        self,
        session,
        message,
        member_context,
        db,
    ):
        """
        Execute a real Solana Devnet settlement.
        """

        confirmation = message.strip().lower()

        if confirmation not in {
            "1",
            "yes",
            "y",
            "2",
            "no",
            "n",
        }:
            return {
                "message": (
                    "Reply *1* to confirm the "
                    "0.01 SOL Devnet settlement "
                    "or *2* to cancel."
                ),
                "type": "text",
                "context_update": {},
            }

        if confirmation in {"2", "no", "n"}:
            SessionManager.finish_wallet(session)

            return {
                "message": "Solana settlement cancelled.",
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        if db is None:
            raise RuntimeError("Database session is required")

        member_account = member_context.get("member_account")

        if member_account is None:
            SessionManager.finish_wallet(session)

            return {
                "message": "I couldn't find your member account.",
                "type": "text",
                "context_update": {},
            }

        try:
            # ----------------------------------------------------------
            # Resolve selected stokvel
            # ----------------------------------------------------------

            selected_stokvel_id = (
                SessionManager.selected_stokvel_id(session)
            )

            if not selected_stokvel_id:
                raise ValueError(
                    "Please select your digital asset stokvel first."
                )

            # ----------------------------------------------------------
            # Resolve treasury
            # ----------------------------------------------------------

            treasury = TreasuryService.get_treasury_by_stokvel(
                db=db,
                stokvel_id=selected_stokvel_id,
            )

            if treasury is None:
                raise ValueError(
                    "The selected stokvel does not have a configured treasury."
                )

            if treasury.denomination.value != "SOL":
                raise ValueError(
                    "The selected stokvel is not configured for Solana settlement."
                )

            # ----------------------------------------------------------
            # Resolve member's Solana account
            # ----------------------------------------------------------

            blockchain_service = BlockchainAccountService(db)

            account = blockchain_service.get_or_create_solana_account(
                member_account_id=member_account.id,
            )

            destination = account.address

            # ----------------------------------------------------------
            # Create settlement transaction
            # ----------------------------------------------------------

            wallet = WalletService.get_or_create_wallet(
                db=db,
                member_account=member_account,
            )

            transaction = WalletTransaction(
                wallet_id=wallet.id,
                stokvel_id=selected_stokvel_id,
                transaction_type=WalletTransactionType.TRANSFER,
                amount=Decimal("0.01"),
                currency="SOL",
                status=WalletTransactionStatus.PENDING,
                reference=f"SOL-{uuid.uuid4().hex[:12].upper()}",
                description="Solana Devnet settlement transfer",
            )

            db.add(transaction)
            db.flush()

            # ----------------------------------------------------------
            # Execute through generic settlement layer
            # ----------------------------------------------------------

            result = await SettlementOrchestrator.settle(
                db=db,
                transaction=transaction,
                destination=destination,
            )

            if not result.succeeded:
                raise ValueError(
                    result.error or "Solana settlement failed."
                )

            signature = result.external_reference

            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "*Solana Devnet Settlement Complete*\n\n"
                    "Amount: *0.01 SOL*\n\n"
                    f"Destination:\n`{destination}`\n\n"
                    f"Transaction:\n`{signature}`\n\n"
                    "The transfer was executed on Solana Devnet."
                ),
                "type": "text",
                "context_update": {
                    "wallet": {
                        "active": False,
                    }
                },
            }

        except ValueError as exc:
            SessionManager.finish_wallet(session)

            return {
                "message": (
                    "*Solana settlement failed.*\n\n"
                    f"{exc}"
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
