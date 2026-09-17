from abc import ABC, abstractmethod
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.wallet_transaction import WalletTransaction

from app.services.settlement.settlement_result import (
    SettlementResult,
)


class SettlementHandler(ABC):
    """
    Generic settlement execution boundary.

    Concrete handlers implement rail-specific settlement
    execution.

    The handler does not commit the database transaction.
    """

    @abstractmethod
    async def settle(
        self,
        db: Session,
        transaction: WalletTransaction,
        destination: str,
        amount: Decimal,
    ) -> SettlementResult:
        """
        Execute settlement for a wallet transaction.
        """
        raise NotImplementedError
