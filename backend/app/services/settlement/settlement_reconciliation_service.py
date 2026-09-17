from dataclasses import dataclass
from enum import Enum

from sqlalchemy.orm import Session

from app.models.wallet_transaction import WalletTransaction
from app.models.settlement import Settlement


class ReconciliationStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


@dataclass
class ReconciliationResult:
    status: ReconciliationStatus
    settlement_id: str | None = None
    external_reference: str | None = None
    message: str | None = None

    @property
    def confirmed(self) -> bool:
        return self.status == ReconciliationStatus.CONFIRMED

    @property
    def failed(self) -> bool:
        return self.status == ReconciliationStatus.FAILED

    @property
    def unknown(self) -> bool:
        return self.status == ReconciliationStatus.UNKNOWN


class SettlementReconciliationService:
    """
    Reconciles the state of an external settlement.

    This service does not:
    - execute a new settlement
    - retry a settlement
    - modify wallet balances
    - create ledger entries
    - commit database transactions

    If external execution cannot be proven, reconciliation
    returns UNKNOWN rather than guessing.
    """

    @staticmethod
    def reconcile(
        db: Session,
        transaction: WalletTransaction,
    ) -> ReconciliationResult:

        if transaction is None:
            raise ValueError(
                "Wallet transaction is required"
            )

        settlement = (
            db.query(Settlement)
            .filter(
                Settlement.wallet_transaction_id
                == transaction.id
            )
            .one_or_none()
        )

        if settlement is None:
            return ReconciliationResult(
                status=ReconciliationStatus.UNKNOWN,
                message=(
                    "No settlement record exists. "
                    "External execution cannot be verified."
                ),
            )

        if settlement.transaction_signature:
            return ReconciliationResult(
                status=ReconciliationStatus.CONFIRMED,
                settlement_id=str(settlement.id),
                external_reference=(
                    settlement.transaction_signature
                ),
                message=(
                    "External settlement reference exists. "
                    "Further rail-specific verification is required."
                ),
            )

        if settlement.status.value == "FAILED":
            return ReconciliationResult(
                status=ReconciliationStatus.FAILED,
                settlement_id=str(settlement.id),
                message=(
                    "Settlement is recorded as failed "
                    "and has no external transaction reference."
                ),
            )

        return ReconciliationResult(
            status=ReconciliationStatus.UNKNOWN,
            settlement_id=str(settlement.id),
            message=(
                "Settlement exists but external execution "
                "cannot be conclusively verified."
            ),
        )
