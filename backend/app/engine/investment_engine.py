from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict

from app.models.enums import (
    InvestmentAssetStatus,
    StokvelInvestmentStatus,
    WalletTransactionStatus,
    WalletTransactionType,
)
from app.models.investment_asset import InvestmentAsset
from app.models.investment_allocation import InvestmentAllocation
from app.models.stokvel import Stokvel
from app.models.wallet_transaction import WalletTransaction

from app.services.identity.session_manager import SessionManager
from app.services.investment.stokvel_investment_service import (
    StokvelInvestmentService,
)


class InvestmentEngine:
    """
    Handles WhatsApp investment interactions.

    The engine owns the conversational flow.
    StokvelInvestmentService owns the investment business logic.
    """

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

        asset = (
            db.query(InvestmentAsset)
            .filter(
                InvestmentAsset.symbol == "STOCKLANA",
                InvestmentAsset.status == InvestmentAssetStatus.ACTIVE,
            )
            .one_or_none()
        )

        if asset is None:
            SessionManager.finish_investment(session)

            return {
                "message": (
                    "Stocklana is currently unavailable."
                ),
                "type": "text",
                "context_update": {},
            }

        investment_context = SessionManager.investment_context(
            session
        )

        step = investment_context.get("step")

        # --------------------------------------------------------------
        # CONFIRMATION
        # --------------------------------------------------------------

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
                        "Reply *1* to confirm the Stocklana "
                        "investment or *2* to cancel."
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
                        "*Stocklana investment created*\n\n"
                        f"Stokvel: *{stokvel.name}*\n"
                        f"Investment: R{investment.amount:,.2f}\n"
                        f"Units: {investment.quantity:,.0f}\n"
                        f"Participation: 100%\n\n"
                        f"Members allocated: {len(allocations)}\n"
                        "Term: 30 days\n\n"
                        "The collective investment has been "
                        "recorded successfully."
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

        # --------------------------------------------------------------
        # INVESTMENT PREVIEW
        # --------------------------------------------------------------

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
            "*Stocklana Investment*",
            "",
            f"*{stokvel.name}*",
            "",
            f"Investment: R{total_amount:,.2f}",
            f"Stocklana price: R{asset.price:,.2f}",
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
        )

        return {
            "message": "\n".join(lines),
            "type": "text",
            "context_update": {},
        }
