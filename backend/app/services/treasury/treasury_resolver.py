from sqlalchemy.orm import Session

from app.models.wallet_transaction import WalletTransaction
from app.services.treasury.treasury_service import TreasuryService


class TreasuryResolver:
    """
    Resolves the treasury configuration governing a wallet transaction.

    This resolver does not:
    - move money
    - execute blockchain transactions
    - execute payment settlements
    - modify wallet balances
    - commit database transactions

    It only resolves:

        WalletTransaction
            -> Stokvel
            -> StokvelTreasury
    """

    @staticmethod
    def resolve(
        db: Session,
        wallet_transaction: WalletTransaction,
    ):
        if wallet_transaction is None:
            raise ValueError(
                "Wallet transaction is required"
            )

        if wallet_transaction.stokvel_id is None:
            raise ValueError(
                "Wallet transaction is not associated with a stokvel"
            )

        treasury = TreasuryService.get_treasury_by_stokvel(
            db=db,
            stokvel_id=wallet_transaction.stokvel_id,
        )

        if treasury is None:
            raise ValueError(
                "Stokvel does not have a treasury"
            )

        return treasury
