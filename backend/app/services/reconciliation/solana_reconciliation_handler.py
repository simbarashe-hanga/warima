from sqlalchemy.orm import Session

from app.models.settlement import Settlement
from app.services.reconciliation.reconciliation_handler import (
    ReconciliationHandler,
)
from app.services.settlement.settlement_reconciliation_service import (
    ReconciliationResult,
    ReconciliationStatus,
)
from app.services.solana.solana_service import SolanaService


class SolanaReconciliationHandler(ReconciliationHandler):
    """
    Solana-specific external settlement reconciliation.

    This handler verifies an existing Solana settlement.
    It does not:
    - send SOL
    - retry a settlement
    - create a new settlement
    - modify wallet balances
    - create ledger entries
    - commit database transactions
    """

    def __init__(
        self,
        solana_service: SolanaService | None = None,
    ):
        self.solana_service = (
            solana_service or SolanaService()
        )

    async def reconcile(
        self,
        db: Session,
        settlement: Settlement,
    ) -> ReconciliationResult:
        if settlement is None:
            raise ValueError("Settlement is required")

        if not settlement.transaction_signature:
            return ReconciliationResult(
                status=ReconciliationStatus.UNKNOWN,
                settlement_id=str(settlement.id),
                message=(
                    "Settlement has no Solana transaction signature. "
                    "External execution cannot be verified."
                ),
            )

        status = await self.solana_service.get_signature_status(
            settlement.transaction_signature
        )

        if status is None:
            return ReconciliationResult(
                status=ReconciliationStatus.UNKNOWN,
                settlement_id=str(settlement.id),
                external_reference=(
                    settlement.transaction_signature
                ),
                message=(
                    "Solana transaction could not be found "
                    "in transaction history."
                ),
            )

        if status.err is not None:
            return ReconciliationResult(
                status=ReconciliationStatus.FAILED,
                settlement_id=str(settlement.id),
                external_reference=(
                    settlement.transaction_signature
                ),
                message=(
                    "Solana transaction exists but "
                    "reported an execution error."
                ),
            )

        confirmation_status = status.confirmation_status

        if confirmation_status is None:
            return ReconciliationResult(
                status=ReconciliationStatus.UNKNOWN,
                settlement_id=str(settlement.id),
                external_reference=(
                    settlement.transaction_signature
                ),
                message=(
                    "Solana transaction exists but has "
                    "no confirmation status."
                ),
            )

        if str(confirmation_status).endswith(
            "Finalized"
        ):
            return ReconciliationResult(
                status=ReconciliationStatus.CONFIRMED,
                settlement_id=str(settlement.id),
                external_reference=(
                    settlement.transaction_signature
                ),
                message=(
                    "Solana transaction is finalized "
                    "with no execution error."
                ),
            )

        return ReconciliationResult(
            status=ReconciliationStatus.UNKNOWN,
            settlement_id=str(settlement.id),
            external_reference=(
                settlement.transaction_signature
            ),
            message=(
                "Solana transaction exists but is not "
                "yet finalized."
            ),
        )
