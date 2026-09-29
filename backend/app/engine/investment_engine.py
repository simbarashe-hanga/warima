from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict

from app.core.config import settings
from app.models.enums import (
    InvestmentAssetStatus,
    MembershipRole,
    MembershipStatus,
    StokvelInvestmentStatus,
    WalletTransactionStatus,
    WalletTransactionType,
)
from app.models.investment_asset import InvestmentAsset
from app.models.investment_allocation import InvestmentAllocation
from app.models.stokvel import Stokvel
from app.models.wallet_transaction import WalletTransaction
from app.models.member_account import MemberAccount
from app.models.membership import Membership

from app.services.identity.session_manager import SessionManager
from app.services.investment.stokvel_investment_service import (
    StokvelInvestmentService,
)
from app.services.solana.solana_service import SolanaService
from app.services.settlement.settlement_orchestrator import (
    SettlementOrchestrator,
)
from app.services.settlement.settlement_result import (
    SettlementExecutionStatus,
)
from app.services.treasury.treasury_ledger_service import (
    TreasuryLedgerService,
)
from app.services.wallet.wallet_service import WalletService


class InvestmentEngine:
    """
    Handles WhatsApp investment interactions.

    Two investment modes are supported:

    1. generic
       Treasury -> configured investment destination

    2. stocklana
       Existing Stocklana investment flow
    """

    # Simple SOL transfer fee reserve.
    #
    # The treasury must retain enough SOL to pay the
    # transaction fee. The remaining on-chain balance
    # is forwarded to the investment destination.
    SOL_TRANSACTION_FEE_RESERVE = Decimal("0.000005")

    async def handle(
        self,
        message: str,
        intent: Dict[str, Any],
        session,
        member_context: Dict[str, Any],
        db,
    ) -> Dict[str, Any]:

        selected_stokvel_id = (
            SessionManager.selected_stokvel_id(session)
        )

        if not selected_stokvel_id:
            SessionManager.finish_investment(session)

            return {
                "message": (
                    "Please select a stokvel first.\n\n"
                    "Type *Stokvels* to choose your stokvel."
                ),
                "type": "text",
                "context_update": {},
            }

        stokvel = (
            db.query(Stokvel)
            .filter(Stokvel.id == selected_stokvel_id)
            .one_or_none()
        )

        if stokvel is None:
            SessionManager.finish_investment(session)

            return {
                "message": "That stokvel could not be found.",
                "type": "text",
                "context_update": {},
            }

        investment_context = SessionManager.investment_context(
            session
        )

        mode = investment_context.get("mode")

        if not mode:
            mode = intent.get("action") or "generic"

        # ==============================================================
        # GENERIC WARIMA INVESTMENT
        #
        # Treasury -> Investment Destination
        # ==============================================================

        if mode == "generic":

            destination = getattr(
                settings,
                "SOLANA_INVESTMENT_DESTINATION_ADDRESS",
                None,
            )

            if not destination:
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        "Warima's investment destination is "
                        "not configured yet."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            treasury = getattr(
                stokvel,
                "treasury",
                None,
            )

            if treasury is None:
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        f"*{stokvel.name}* does not have "
                        "a treasury configured."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            if treasury.rail.value != "SOLANA":
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        f"*{stokvel.name}* is not configured "
                        "for Solana investment."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            if treasury.network != "devnet":
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        "Generic Warima investment currently "
                        "supports Solana devnet only."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            if not treasury.blockchain_address:
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        f"*{stokvel.name}* treasury does not "
                        "have a blockchain address."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            # ----------------------------------------------------------
            # INVESTMENT AUTHORIZATION
            #
            # Only the ACTIVE OWNER of the selected stokvel may
            # move treasury funds into an investment.
            #
            # The membership is resolved from the authenticated
            # member account + selected stokvel. We deliberately do
            # not trust membership_id from the WhatsApp session.
            # ----------------------------------------------------------

            member_account_id = (
                member_context.get("member_account_id")
            )

            if not member_account_id:
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        "Your member account could not "
                        "be resolved."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            member_account = (
                db.query(MemberAccount)
                .filter(
                    MemberAccount.id == member_account_id
                )
                .one_or_none()
            )

            if member_account is None:
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        "Your member account could not "
                        "be found."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            membership = (
                db.query(Membership)
                .filter(
                    Membership.member_account_id
                    == member_account.id,
                    Membership.stokvel_id
                    == stokvel.id,
                    Membership.status
                    == MembershipStatus.ACTIVE,
                )
                .one_or_none()
            )

            if membership is None:
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        "You are not an active member "
                        "of this stokvel."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            if membership.role != MembershipRole.OWNER:
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        "Only the stokvel owner can "
                        "invest the treasury."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            solana_service = SolanaService()

            # ----------------------------------------------------------
            # Read the REAL on-chain treasury balance.
            #
            # We deliberately do not use TreasuryLedger.get_balance()
            # here because historical ledger data may not represent
            # actual on-chain SOL.
            # ----------------------------------------------------------

            try:
                on_chain_balance = Decimal(
                    str(
                        await solana_service.get_balance(
                            treasury.blockchain_address
                        )
                    )
                )

            except Exception as exc:
                print("=" * 70)
                print("GENERIC INVESTMENT BALANCE ERROR")
                print(exc)
                print("=" * 70)

                SessionManager.finish_investment(session)

                return {
                    "message": (
                        "I couldn't read the Solana treasury balance."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            transferable_amount = (
                on_chain_balance
                - self.SOL_TRANSACTION_FEE_RESERVE
            )

            if transferable_amount <= 0:
                SessionManager.finish_investment(session)

                return {
                    "message": (
                        f"*{stokvel.name}* does not have enough "
                        "SOL available for investment."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            step = investment_context.get("step")

            # ----------------------------------------------------------
            # GENERIC INVESTMENT CONFIRMATION
            # ----------------------------------------------------------

            if step == "awaiting_confirmation":

                choice = message.strip()

                if choice == "2":
                    SessionManager.finish_investment(session)

                    return {
                        "message": "Investment cancelled.",
                        "type": "text",
                        "context_update": {},
                    }

                if choice != "1":
                    return {
                        "message": (
                            "Reply *1* to confirm the investment "
                            "or *2* to cancel."
                        ),
                        "type": "text",
                        "context_update": {},
                    }

                # Re-read the balance immediately before execution.
                try:
                    on_chain_balance = Decimal(
                        str(
                            await solana_service.get_balance(
                                treasury.blockchain_address
                            )
                        )
                    )

                except Exception as exc:
                    print("=" * 70)
                    print("GENERIC INVESTMENT BALANCE ERROR")
                    print(exc)
                    print("=" * 70)

                    SessionManager.finish_investment(session)

                    return {
                        "message": (
                            "I couldn't verify the current "
                            "treasury balance."
                        ),
                        "type": "text",
                        "context_update": {},
                    }

                transferable_amount = (
                    on_chain_balance
                    - self.SOL_TRANSACTION_FEE_RESERVE
                )

                if transferable_amount <= 0:
                    SessionManager.finish_investment(session)

                    return {
                        "message": (
                            "The treasury no longer has enough "
                            "SOL available for this investment."
                        ),
                        "type": "text",
                        "context_update": {},
                    }

                try:
                    transaction = (
                        WalletService.create_investment(
                            db=db,
                            member_account=member_account,
                            amount=transferable_amount,
                            stokvel_id=stokvel.id,
                            currency="SOL",
                        )
                    )

                    db.flush()

                    # --------------------------------------------------
                    # Treasury -> investment destination
                    #
                    # SettlementService will automatically use
                    # the treasury signer because this transaction
                    # is INVESTMENT, not CONTRIBUTION.
                    # --------------------------------------------------

                    result = await SettlementOrchestrator.settle(
                        db=db,
                        transaction=transaction,
                        destination=destination,
                    )

                    if (
                        result.status
                        != SettlementExecutionStatus.COMPLETED
                    ):
                        SessionManager.finish_investment(session)

                        return {
                            "message": (
                                "The investment could not be "
                                "executed.\n\n"
                                f"Reason: {result.error or 'Settlement failed'}"
                            ),
                            "type": "text",
                            "context_update": {},
                        }

                    # --------------------------------------------------
                    # Record the treasury-side accounting entry.
                    #
                    # This does NOT debit the member wallet.
                    # --------------------------------------------------

                    TreasuryLedgerService.record_debit(
                        db=db,
                        treasury=treasury,
                        amount=transferable_amount,
                        transaction_id=transaction.id,
                    )

                    db.flush()

                    SessionManager.finish_investment(session)

                    signature = result.external_reference

                    return {
                        "message": (
                            "*Investment executed successfully* \n\n"
                            f"Stokvel: *{stokvel.name}*\n"
                            f"Amount: *{transferable_amount:.9f} SOL*\n"
                            f"Destination:\n"
                            f"`{destination}`\n\n"
                            f"Transaction:\n"
                            f"`{signature}`\n\n"
                            "Status: *Completed*"
                        ),
                        "type": "text",
                        "context_update": {},
                    }

                except Exception as exc:

                    print("=" * 70)
                    print("GENERIC INVESTMENT ERROR")
                    print(exc)
                    print("=" * 70)

                    SessionManager.finish_investment(session)

                    return {
                        "message": (
                            "I couldn't execute the investment.\n\n"
                            f"Reason: {exc}"
                        ),
                        "type": "text",
                        "context_update": {},
                    }

            # ----------------------------------------------------------
            # GENERIC INVESTMENT PREVIEW
            # ----------------------------------------------------------

            SessionManager.start_investment(
                session,
                step="awaiting_confirmation",
                mode="generic",
            )

            return {
                "message": (
                    "*Warima Investment*\n\n"
                    f"*{stokvel.name}*\n\n"
                    f"Treasury balance: "
                    f"*{on_chain_balance:.9f} SOL*\n"
                    f"Investment amount: "
                    f"*{transferable_amount:.9f} SOL*\n"
                    f"Network reserve: "
                    f"{self.SOL_TRANSACTION_FEE_RESERVE:.9f} SOL\n\n"
                    f"Destination:\n"
                    f"`{destination}`\n\n"
                    "The investment will transfer the "
                    "available treasury SOL to the configured "
                    "investment destination.\n\n"
                    "Reply *1* to confirm.\n"
                    "Reply *2* to cancel."
                ),
                "type": "text",
                "context_update": {},
            }

        # ==============================================================
        # STOCKLANA INVESTMENT
        #
        # Existing Stocklana flow
        # ==============================================================

        if mode == "stocklana":

            asset = (
                db.query(InvestmentAsset)
                .filter(
                    InvestmentAsset.symbol == "STOCKLANA",
                    InvestmentAsset.status
                    == InvestmentAssetStatus.ACTIVE,
                )
                .one_or_none()
            )

            if asset is None:
                SessionManager.finish_investment(session)

                return {
                    "message": "Stocklana is currently unavailable",
                    "type": "text",
                    "context_update": {},
                }

            step = investment_context.get("step")
            asset_name = asset.name

            # ----------------------------------------------------------
            # CONFIRMATION
            # ----------------------------------------------------------

            if step == "awaiting_confirmation":

                choice = message.strip()

                if choice == "2":

                    SessionManager.finish_investment(session)

                    return {
                        "message": "Investment cancelled.",
                        "type": "text",
                        "context_update": {},
                    }

                if choice != "1":

                    return {
                        "message": (
                            f"Reply *1* to confirm the "
                            f"{asset_name} investment or *2* to cancel."
                        ),
                        "type": "text",
                        "context_update": {},
                    }

                try:

                    term_start = datetime.now(timezone.utc)

                    maturity_at = (
                        term_start + timedelta(days=30)
                    )

                    investment = (
                        StokvelInvestmentService.create_investment(
                            db=db,
                            stokvel_id=stokvel.id,
                            investment_asset_id=asset.id,
                            term_start=term_start,
                            maturity_at=maturity_at,
                        )
                    )

                    db.flush()

                    allocations = (
                        db.query(InvestmentAllocation)
                        .filter(
                            InvestmentAllocation.investment_id
                            == investment.id
                        )
                        .all()
                    )

                    SessionManager.finish_investment(session)

                    return {
                        "message": (
                            f"*{asset_name} investment created*\n\n"
                            f"Stokvel: *{stokvel.name}*\n"
                            f"Investment: R{investment.amount:,.2f}\n"
                            f"Units: {investment.quantity:,.0f}\n"
                            "Participation: 100%\n\n"
                            f"Members allocated: {len(allocations)}\n"
                            "Term: 30 days\n\n"
                            "Status: *Pending execution*\n"
                            "The collective investment has been "
                            "created and is awaiting execution."
                        ),
                        "type": "text",
                        "context_update": {},
                    }

                except Exception as exc:

                    print("=" * 70)
                    print("INVESTMENT ERROR")
                    print(exc)
                    print("=" * 70)

                    SessionManager.finish_investment(session)

                    return {
                        "message": (
                            "I couldn't create the investment.\n\n"
                            f"Reason: {exc}"
                        ),
                        "type": "text",
                        "context_update": {},
                    }

            # ----------------------------------------------------------
            # STOCKLANA INVESTMENT PREVIEW
            # ----------------------------------------------------------

            allocated_subquery = (
                db.query(
                    InvestmentAllocation.contribution_transaction_id
                )
                .subquery()
            )

            contributions = (
                db.query(WalletTransaction)
                .filter(
                    WalletTransaction.stokvel_id == stokvel.id,
                    WalletTransaction.transaction_type
                    == WalletTransactionType.CONTRIBUTION,
                    WalletTransaction.status
                    == WalletTransactionStatus.COMPLETED,
                    ~WalletTransaction.id.in_(allocated_subquery),
                )
                .all()
            )

            total_amount = sum(
                (
                    Decimal(transaction.amount)
                    for transaction in contributions
                ),
                Decimal("0"),
            )

            if total_amount <= 0:

                SessionManager.finish_investment(session)

                return {
                    "message": (
                        f"*{stokvel.name}* has no available "
                        "completed contributions to invest."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            quantity = (
                total_amount / Decimal(asset.price)
            )

            lines = [
                f"*{asset_name} Investment*",
                "",
                f"*{stokvel.name}*",
                "",
                f"Investment: R{total_amount:,.2f}",
                f"{asset_name} price: R{asset.price:,.2f}",
                f"Units: {quantity:,.0f}",
                "",
                "*Member participation:*",
            ]

            for transaction in contributions:

                wallet = transaction.wallet
                member_account = wallet.member_account
                user = member_account.user

                name = (
                    user.display_name
                    or "Member"
                )

                percentage = (
                    Decimal(transaction.amount)
                    / total_amount
                    * Decimal("100")
                )

                lines.append(
                    f"• {name} — {percentage:.0f}%"
                )

            lines.extend(
                [
                    "",
                    "Reply *1* to confirm.",
                    "Reply *2* to cancel.",
                ]
            )

            SessionManager.start_investment(
                session,
                step="awaiting_confirmation",
                mode=mode,
            )

            return {
                "message": "\n".join(lines),
                "type": "text",
                "context_update": {},
            }

        # ==============================================================
        # UNKNOWN MODE
        # ==============================================================

        SessionManager.finish_investment(session)

        return {
            "message": (
                "I couldn't determine the investment type."
            ),
            "type": "text",
            "context_update": {},
        }
