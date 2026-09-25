from decimal import Decimal

from app.models.wallet_transaction import WalletTransaction

from app.services.settlement.settlement_handler import (
    SettlementHandler,
)
from app.services.settlement.settlement_result import (
    SettlementExecutionStatus,
    SettlementResult,
)
from app.services.solana.settlement_service import (
    SettlementService,
)


class SolanaSettlementHandler(SettlementHandler):
    """
    Adapter between the generic settlement architecture
    and the existing Solana settlement service.

    This handler does not implement Solana settlement
    logic itself. It delegates execution to the existing
    SettlementService.
    """

    def __init__(
        self,
        settlement_service: SettlementService | None = None,
    ):
        self.settlement_service = (
            settlement_service
            or SettlementService()
        )

    async def settle(
        self,
        db,
        transaction: WalletTransaction,
        destination: str,
        amount: Decimal,
    ) -> SettlementResult:
        """
        Execute a Solana settlement through the existing
        Solana SettlementService.
        """

        result = await self.settlement_service.settle_to_solana(
            db=db,
            transaction=transaction,
            destination=destination,
            amount_sol=amount,
        )

        if result.get("success"):
            status = (
                SettlementExecutionStatus.COMPLETED
            )
        else:
            status = (
                SettlementExecutionStatus.FAILED
            )

        return SettlementResult(
            status=status,
            settlement_id=result.get(
                "settlement_id"
            ),
            external_reference=result.get(
                "signature"
            ),
            error=result.get("error"),
            metadata={
                "transaction_id": result.get(
                    "transaction_id"
                ),
                "amount_sol": result.get(
                    "amount_sol"
                ),
                "network": result.get(
                    "network"
                ),
                "already_settled": result.get(
                    "already_settled",
                    False,
                ),
            },
        )
