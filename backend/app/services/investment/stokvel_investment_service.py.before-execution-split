from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import (
    InvestmentAssetStatus,
    StokvelInvestmentStatus,
    WalletTransactionStatus,
    WalletTransactionType,
    StokvelStatus,
)
from app.models.investment_asset import InvestmentAsset
from app.models.investment_allocation import InvestmentAllocation
from app.models.stokvel import Stokvel
from app.models.stokvel_investment import StokvelInvestment
from app.models.wallet_transaction import WalletTransaction

from app.services.treasury.treasury_ledger_service import TreasuryLedgerService
from app.services.treasury.treasury_resolver import TreasuryResolver


class StokvelInvestmentService:
    """
    Creates collective stokvel investments.

    Investment funds come from completed member contributions
    already credited to the stokvel treasury.

    This service does not:
    - create member wallets
    - create contributions
    - debit member wallets
    - execute external payments
    - execute blockchain transactions
    - commit the database transaction

    The caller owns the database transaction boundary.
    """

    @staticmethod
    def create_investment(
        db: Session,
        stokvel_id,
        investment_asset_id,
        term_start: datetime,
        maturity_at: datetime,
    ) -> StokvelInvestment:

        # --------------------------------------------------------------
        # Validate identifiers
        # --------------------------------------------------------------

        if stokvel_id is None:
            raise ValueError("Stokvel ID is required")

        if investment_asset_id is None:
            raise ValueError("Investment asset ID is required")

        if term_start is None:
            raise ValueError("Investment term start is required")

        if maturity_at is None:
            raise ValueError("Investment maturity date is required")

        if maturity_at <= term_start:
            raise ValueError(
                "Investment maturity must be after term start"
            )

        # --------------------------------------------------------------
        # Resolve active stokvel
        # --------------------------------------------------------------

        stokvel = (
            db.query(Stokvel)
            .filter(
                Stokvel.id == stokvel_id,
                Stokvel.status == StokvelStatus.ACTIVE,
            )
            .one_or_none()
        )

        if stokvel is None:
            raise ValueError("Stokvel is not active")

        # --------------------------------------------------------------
        # Resolve active investment asset
        # --------------------------------------------------------------

        asset = (
            db.query(InvestmentAsset)
            .filter(
                InvestmentAsset.id == investment_asset_id,
                InvestmentAsset.status == InvestmentAssetStatus.ACTIVE,
            )
            .one_or_none()
        )

        if asset is None:
            raise ValueError("Investment asset is not active")

        # --------------------------------------------------------------
        # Validate asset pricing
        # --------------------------------------------------------------

        unit_price = Decimal(str(asset.price))

        if unit_price <= 0:
            raise ValueError(
                "Investment asset price must be greater than zero"
            )

        # --------------------------------------------------------------
        # Resolve stokvel treasury
        # --------------------------------------------------------------

        treasury = stokvel.treasury

        if treasury is None:
            raise ValueError(
                "Stokvel treasury could not be found"
            )

        # --------------------------------------------------------------
        # MVP currency rule
        #
        # Stocklana investment is currently ZAR/off-chain.
        # Do not silently convert ZAR into another asset/rail.
        # --------------------------------------------------------------

        treasury_currency = treasury.denomination.value
        asset_currency = asset.currency

        if treasury_currency != asset_currency:
            raise ValueError(
                f"Investment currency mismatch: "
                f"treasury={treasury_currency}, "
                f"asset={asset_currency}"
            )

        if asset_currency != "ZAR":
            raise ValueError(
                "Stocklana MVP investments must use ZAR"
            )

        # --------------------------------------------------------------
        # Find eligible completed contributions
        #
        # A contribution is eligible when:
        # - it belongs to this stokvel
        # - it is a CONTRIBUTION
        # - it is COMPLETED
        # - it has not already been allocated
        # --------------------------------------------------------------

        allocated_subquery = (
            db.query(InvestmentAllocation.contribution_transaction_id)
            .subquery()
        )

        contributions = (
            db.query(WalletTransaction)
            .filter(
                WalletTransaction.stokvel_id == stokvel_id,
                WalletTransaction.transaction_type
                == WalletTransactionType.CONTRIBUTION,
                WalletTransaction.status
                == WalletTransactionStatus.COMPLETED,
                ~WalletTransaction.id.in_(allocated_subquery),
            )
            .order_by(WalletTransaction.created_at.asc())
            .all()
        )

        if not contributions:
            raise ValueError(
                "No eligible completed contributions are available "
                "for investment"
            )

        # --------------------------------------------------------------
        # Calculate investment amount
        # --------------------------------------------------------------

        total_amount = sum(
            (Decimal(str(transaction.amount))
             for transaction in contributions),
            Decimal("0.00"),
        )

        if total_amount <= 0:
            raise ValueError(
                "Eligible contribution amount must be greater than zero"
            )

        # --------------------------------------------------------------
        # Verify treasury balance
        # --------------------------------------------------------------

        treasury_balance = TreasuryLedgerService.get_balance(
            db,
            treasury,
        )

        if treasury_balance < total_amount:
            raise ValueError(
                f"Insufficient treasury balance: "
                f"available={treasury_balance}, "
                f"required={total_amount}"
            )

        # --------------------------------------------------------------
        # Calculate investment quantity
        # --------------------------------------------------------------

        quantity = total_amount / unit_price

        # --------------------------------------------------------------
        # Create investment
        # --------------------------------------------------------------

        investment = StokvelInvestment(
            stokvel_id=stokvel.id,
            investment_asset_id=asset.id,
            amount=total_amount,
            quantity=quantity,
            unit_price=unit_price,
            currency=asset_currency,
            term_start=term_start,
            maturity_at=maturity_at,
            status=StokvelInvestmentStatus.PENDING,
        )

        db.add(investment)
        db.flush()

        # --------------------------------------------------------------
        # Create member allocations
        # --------------------------------------------------------------

        for transaction in contributions:

            contribution_amount = Decimal(
                str(transaction.amount)
            )

            participation_percentage = (
                contribution_amount / total_amount
            )

            allocated_quantity = (
                quantity * participation_percentage
            )

            allocation = InvestmentAllocation(
                investment_id=investment.id,
                member_account_id=transaction.wallet.member_account_id,
                contribution_transaction_id=transaction.id,
                contributed_amount=contribution_amount,
                participation_percentage=participation_percentage,
                allocated_quantity=allocated_quantity,
                returned_amount=Decimal("0.00"),
            )

            db.add(allocation)

        # --------------------------------------------------------------
        # Record treasury investment deployment
        # --------------------------------------------------------------

        TreasuryLedgerService.record_investment_debit(
            db,
            treasury,
            total_amount,
            investment.id,
        )

        # --------------------------------------------------------------
        # Activate investment
        # --------------------------------------------------------------

        investment.status = StokvelInvestmentStatus.ACTIVE

        db.flush()

        return investment
