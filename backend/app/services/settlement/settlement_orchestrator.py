from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import WalletTransactionStatus
from app.models.wallet_transaction import WalletTransaction

from app.services.settlement.settlement_asset_resolver import (
    SettlementAssetResolver,
)
from app.services.settlement.settlement_result import (
    SettlementExecutionStatus,
    SettlementResult,
)
from app.services.settlement.settlement_router import (
    SettlementRouter,
)
from app.services.treasury.treasury_resolver import (
    TreasuryResolver,
)


class SettlementOrchestrator:
    """
    Coordinates settlement execution for a WalletTransaction.

    Responsibilities:
    - validate the transaction
    - validate settlement execution state
    - resolve the governing treasury
    - resolve the target settlement asset
    - prevent execution when asset conversion is required
    - resolve the settlement handler
    - execute the selected handler
    - return a normalized SettlementResult

    This class does not:
    - create WalletTransactions
    - modify wallet balances
    - create ledger entries
    - perform FX/token conversion
    - commit database transactions
    - rollback database transactions
    - implement rail-specific settlement logic

    The caller owns the database transaction.
    """

    @staticmethod
    def validate_execution_state(
        transaction: WalletTransaction,
    ) -> None:
        if transaction is None:
            raise ValueError(
                "Wallet transaction is required"
            )

        status = transaction.status

        if status == WalletTransactionStatus.COMPLETED:
            raise ValueError(
                "Wallet transaction has already been settled"
            )

        if status == WalletTransactionStatus.PROCESSING:
            raise ValueError(
                "Wallet transaction is already being settled. "
                "Reconciliation is required before retrying."
            )

        if status == WalletTransactionStatus.CANCELLED:
            raise ValueError(
                "Wallet transaction has been cancelled"
            )

        if status not in (
            WalletTransactionStatus.PENDING,
            WalletTransactionStatus.FAILED,
        ):
            raise ValueError(
                f"Wallet transaction cannot be settled "
                f"from status: {status}"
            )

    @staticmethod
    async def settle(
        db: Session,
        transaction: WalletTransaction,
        destination: str,
    ) -> SettlementResult:

        SettlementOrchestrator.validate_execution_state(
            transaction
        )

        if not destination:
            raise ValueError(
                "Settlement destination is required"
            )

        source_amount = Decimal(
            str(transaction.amount)
        )

        if source_amount <= 0:
            raise ValueError(
                "Wallet transaction amount must be "
                "greater than zero"
            )

        treasury = TreasuryResolver.resolve(
            db=db,
            wallet_transaction=transaction,
        )

        resolution = SettlementAssetResolver.resolve(
            transaction=transaction,
            treasury=treasury,
        )

        if resolution.conversion_required:
            return SettlementResult(
                status=SettlementExecutionStatus.FAILED,
                error=(
                    f"Settlement conversion required: "
                    f"{resolution.source_amount} "
                    f"{resolution.source_currency} -> "
                    f"{resolution.target_asset.value}. "
                    "No conversion rate/provider is configured."
                ),
                metadata={
                    "source_currency": (
                        resolution.source_currency
                    ),
                    "source_amount": str(
                        resolution.source_amount
                    ),
                    "target_asset": (
                        resolution.target_asset.value
                    ),
                    "target_amount": None,
                    "conversion_required": True,
                    "treasury_id": str(treasury.id),
                    "treasury_denomination": (
                        treasury.denomination.value
                    ),
                    "treasury_rail": (
                        treasury.rail.value
                    ),
                },
            )

        target_amount = resolution.target_amount

        if target_amount is None:
            raise ValueError(
                "Settlement target amount is required"
            )

        if target_amount <= 0:
            raise ValueError(
                "Settlement target amount must be "
                "greater than zero"
            )

        handler = SettlementRouter.resolve_handler(
            treasury
        )

        result = await handler.settle(
            db=db,
            transaction=transaction,
            destination=destination,
            amount=target_amount,
        )

        result.metadata.setdefault(
            "source_currency",
            resolution.source_currency,
        )

        result.metadata.setdefault(
            "source_amount",
            str(resolution.source_amount),
        )

        result.metadata.setdefault(
            "target_asset",
            resolution.target_asset.value,
        )

        result.metadata.setdefault(
            "target_amount",
            str(target_amount),
        )

        result.metadata.setdefault(
            "conversion_required",
            False,
        )

        return result
