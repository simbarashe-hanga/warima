from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import WalletTransactionStatus
from app.models.wallet_transaction import WalletTransaction

from app.services.settlement.settlement_result import (
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
    - resolve the settlement handler
    - execute the selected handler
    - return a normalized SettlementResult

    This class does not:
    - create WalletTransactions
    - modify wallet balances
    - create ledger entries
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
        amount: Decimal | None = None,
    ) -> SettlementResult:

        SettlementOrchestrator.validate_execution_state(
            transaction
        )

        if not destination:
            raise ValueError(
                "Settlement destination is required"
            )

        if amount is None:
            amount = Decimal(
                str(transaction.amount)
            )
        else:
            amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError(
                "Settlement amount must be greater than zero"
            )

        treasury = TreasuryResolver.resolve(
            db=db,
            wallet_transaction=transaction,
        )

        handler = SettlementRouter.resolve_handler(
            treasury
        )

        return await handler.settle(
            db=db,
            transaction=transaction,
            destination=destination,
            amount=amount,
        )
