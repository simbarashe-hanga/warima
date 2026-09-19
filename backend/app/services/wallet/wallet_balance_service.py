from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import WalletStatus
from app.models.wallet import Wallet


class WalletBalanceService:
    """
    Manages wallet balance changes.

    This service does not create ledger entries.
    This service does not commit transactions.

    The caller owns the database transaction.
    """


    @staticmethod
    def get_balance(
        wallet: Wallet,
    ) -> Decimal:
        """
        Return the current wallet balance.

        This is a read-only operation.
        """

        if wallet is None:
            raise ValueError("Wallet is required")

        return Decimal(
            str(wallet.balance or 0)
        )

    @staticmethod
    def credit(
        db: Session,
        wallet: Wallet,
        amount,
    ) -> Wallet:

        if wallet is None:
            raise ValueError("Wallet is required")

        if wallet.status != WalletStatus.ACTIVE:
            raise ValueError(
                "Wallet is not active"
            )

        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError(
                "Credit amount must be greater than zero"
            )

        current_balance = Decimal(
            str(wallet.balance or 0)
        )

        wallet.balance = current_balance + amount

        db.flush()

        return wallet

    @staticmethod
    def debit(
        db: Session,
        wallet: Wallet,
        amount,
    ) -> Wallet:

        if wallet is None:
            raise ValueError("Wallet is required")

        if wallet.status != WalletStatus.ACTIVE:
            raise ValueError(
                "Wallet is not active"
            )

        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError(
                "Debit amount must be greater than zero"
            )

        current_balance = Decimal(
            str(wallet.balance or 0)
        )

        if amount > current_balance:
            raise ValueError(
                "Insufficient wallet balance"
            )

        wallet.balance = current_balance - amount

        db.flush()

        return wallet
