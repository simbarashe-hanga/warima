from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.enums import WalletLedgerEntryType
from app.models.treasury_ledger import TreasuryLedger


class TreasuryBalanceService:
    """
    Provides read-only treasury balance calculations.

    Treasury balance is derived from the treasury ledger:

        CREDIT - DEBIT

    This service does not:
    - modify ledger entries
    - modify treasury configuration
    - move money
    - execute settlements
    - commit database transactions

    The caller owns the database transaction.
    """

    @staticmethod
    def get_balance(
        db: Session,
        treasury,
    ) -> Decimal:
        """
        Return the current derived balance for a treasury.
        """

        if treasury is None:
            raise ValueError("Treasury is required")

        credit_result = db.query(
            func.coalesce(
                func.sum(TreasuryLedger.amount),
                0,
            )
        ).filter(
            TreasuryLedger.treasury_id == treasury.id,
            TreasuryLedger.entry_type
            == WalletLedgerEntryType.CREDIT,
        ).scalar()

        debit_result = db.query(
            func.coalesce(
                func.sum(TreasuryLedger.amount),
                0,
            )
        ).filter(
            TreasuryLedger.treasury_id == treasury.id,
            TreasuryLedger.entry_type
            == WalletLedgerEntryType.DEBIT,
        ).scalar()

        credits = Decimal(str(credit_result or 0))
        debits = Decimal(str(debit_result or 0))

        return credits - debits
