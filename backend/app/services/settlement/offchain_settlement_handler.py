from decimal import Decimal

from app.models.wallet_transaction import WalletTransaction

from app.services.settlement.settlement_handler import (
    SettlementHandler,
)
from app.services.settlement.settlement_result import (
    SettlementExecutionStatus,
    SettlementResult,
)


class OffChainSettlementHandler(SettlementHandler):
    """
    Settlement handler for traditional/off-chain
    treasuries.

    Real execution is intentionally not implemented yet.
    """

    async def settle(
        self,
        db,
        transaction: WalletTransaction,
        destination: str,
        amount: Decimal,
    ) -> SettlementResult:

        return SettlementResult(
            status=SettlementExecutionStatus.FAILED,
            error=(
                "Off-chain settlement execution "
                "is not implemented"
            ),
        )
