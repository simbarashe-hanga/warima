from decimal import Decimal

from app.models.enums import WalletLedgerEntryType
from app.models.treasury_ledger import TreasuryLedger


class TreasuryLedgerService:

    @staticmethod
    def record_credit(
        db,
        treasury,
        amount,
        transaction_id,
    ):
        if treasury is None:
            raise ValueError("Treasury is required")

        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        entry = TreasuryLedger(
            treasury_id=treasury.id,
            transaction_id=transaction_id,
            entry_type=WalletLedgerEntryType.CREDIT,
            amount=amount,
            currency=treasury.denomination.value,
        )

        db.add(entry)
        db.flush()

        return entry

    @staticmethod
    def record_debit(
        db,
        treasury,
        amount,
        transaction_id,
    ):
        if treasury is None:
            raise ValueError("Treasury is required")

        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        entry = TreasuryLedger(
            treasury_id=treasury.id,
            transaction_id=transaction_id,
            entry_type=WalletLedgerEntryType.DEBIT,
            amount=amount,
            currency=treasury.denomination.value,
        )

        db.add(entry)
        db.flush()

        return entry
