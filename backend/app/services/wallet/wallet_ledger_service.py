import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.wallet import Wallet
from app.models.wallet_ledger import WalletLedger
from app.models.enums import WalletLedgerEntryType


class WalletLedgerService:
    """
    Creates financial ledger entries

    This service does not commit transactions
    The caller owns the db transaction
    """

    @staticmethod
    def record_credit(
        db: Session,
        wallet: Wallet,
        amount,
        transaction_id,
    ) -> WalletLedger:

        if wallet is None:
            raise ValueError("Wallet is required")

        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Ledger credit amount must be greater than zero")

        entry = WalletLedger(
            id=uuid.uuid4(),
            wallet_id=wallet.id,
            transaction_id=transaction_id,
            entry_type=WalletLedgerEntryType.CREDIT,
            amount=amount,
            currency=wallet.currency,
        )

        db.add(entry)
        db.flush()

        return entry

    @staticmethod
    def record_debit(
        db: Session,
        wallet: Wallet,
        amount,
        transaction_id,
    ) -> WalletLedger:

        if wallet is None:
            raise ValueError("Wallet is required")

        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Ledger debit amount must be greater than zero")

        entry = WalletLedger(
            id=uuid.uuid4(),
            wallet_id=wallet.id,
            transaction_id=transaction_id,
            entry_type=WalletLedgerEntryType.DEBIT,
            amount=amount,
            currency=wallet.currency,
        )

        db.add(entry)
        db.flush()

        return entry
