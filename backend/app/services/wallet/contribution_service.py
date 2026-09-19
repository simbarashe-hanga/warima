from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.wallet_transaction import WalletTransaction
from app.models.enums import WalletTransactionStatus

from app.services.wallet.wallet_balance_service import WalletBalanceService
from app.services.wallet.wallet_ledger_service import WalletLedgerService
from app.services.treasury.treasury_ledger_service import TreasuryLedgerService
from app.services.treasury.treasury_resolver import TreasuryResolver


class ContributionService:

    @staticmethod
    def complete_contribution(
        db: Session,
        transaction: WalletTransaction,
    ) -> WalletTransaction:
        """
        Complete a pending contribution.

        Accounting effects:

        Member wallet:
            DEBIT contribution amount

        Member wallet ledger:
            DEBIT contribution amount

        Stokvel treasury ledger:
            CREDIT contribution amount

        Transaction:
            PENDING -> COMPLETED

        Idempotency:

            COMPLETED -> return unchanged

        This method does NOT commit.
        The caller owns the database transaction.
        """

        if transaction is None:
            raise ValueError("Contribution transaction is required")

        # --------------------------------------------------------------
        # Idempotency
        # --------------------------------------------------------------

        if transaction.status == WalletTransactionStatus.COMPLETED:
            return transaction

        # --------------------------------------------------------------
        # State validation
        # --------------------------------------------------------------

        if transaction.status != WalletTransactionStatus.PENDING:
            raise ValueError(
                f"Contribution transaction cannot be completed "
                f"from status {transaction.status.value}"
            )

        amount = Decimal(str(transaction.amount))

        if amount <= 0:
            raise ValueError(
                "Contribution amount must be greater than zero"
            )

        if transaction.stokvel_id is None:
            raise ValueError(
                "Contribution must belong to a stokvel"
            )

        # --------------------------------------------------------------
        # Resolve member wallet
        # --------------------------------------------------------------

        wallet = transaction.wallet

        if wallet is None:
            raise ValueError(
                "Contribution wallet could not be found"
            )

        # --------------------------------------------------------------
        # Resolve stokvel treasury
        # --------------------------------------------------------------

        treasury = TreasuryResolver.resolve(
            db,
            transaction,
        )

        # --------------------------------------------------------------
        # Debit member wallet
        # --------------------------------------------------------------

        WalletBalanceService.debit(
            db,
            wallet,
            amount,
        )

        # --------------------------------------------------------------
        # Record member wallet debit
        # --------------------------------------------------------------

        WalletLedgerService.record_debit(
            db,
            wallet,
            amount,
            transaction.id,
        )

        # --------------------------------------------------------------
        # Record treasury credit
        # --------------------------------------------------------------

        TreasuryLedgerService.record_credit(
            db,
            treasury,
            amount,
            transaction.id,
        )

        # --------------------------------------------------------------
        # Complete transaction
        # --------------------------------------------------------------

        transaction.status = WalletTransactionStatus.COMPLETED

        db.flush()

        return transaction
