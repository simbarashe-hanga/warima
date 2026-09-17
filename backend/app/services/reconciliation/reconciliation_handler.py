from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.models.settlement import Settlement
from app.services.settlement.settlement_reconciliation_service import (
    ReconciliationResult,
)


class ReconciliationHandler(ABC):
    """
    Generic external settlement reconciliation boundary.

    Concrete handlers implement rail-specific verification.

    The handler does not:
    - execute a new settlement
    - retry a settlement
    - modify wallet balances
    - create ledger entries
    - commit database transactions
    """

    @abstractmethod
    async def reconcile(
        self,
        db: Session,
        settlement: Settlement,
    ) -> ReconciliationResult:
        raise NotImplementedError
