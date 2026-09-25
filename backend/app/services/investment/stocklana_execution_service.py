from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import SettlementStatus
from app.models.stokvel_investment import StokvelInvestment
from app.models.stocklana_execution import StocklanaExecution
from app.services.investment.jupiter_service import JupiterService


class StocklanaExecutionService:
    """
    Prepares the on-chain execution associated with a
    Stocklana collective investment.

    StokvelInvestment remains the ZAR accounting/business record.

    This service prepares a real Jupiter swap transaction but does
    not sign or broadcast it. Signing and broadcasting require a
    funded Solana execution wallet.
    """

    SOL_MINT = "So11111111111111111111111111111111111111112"

    def __init__(self, jupiter_service: JupiterService | None = None):
        self.jupiter_service = jupiter_service or JupiterService()

    async def prepare(
        self,
        db: Session,
        investment: StokvelInvestment,
        output_mint: str,
        input_amount_lamports: int,
        user_public_key: str,
        slippage_bps: int = 50,
    ) -> dict:

        if not output_mint:
            raise ValueError(
                "Stocklana output mint is required"
            )

        if input_amount_lamports <= 0:
            raise ValueError(
                "Stocklana input amount must be positive"
            )

        if not user_public_key:
            raise ValueError(
                "Stocklana execution wallet is required"
            )

        existing = (
            db.query(StocklanaExecution)
            .filter(
                StocklanaExecution.investment_id == investment.id
            )
            .first()
        )

        if existing:
            if existing.status == SettlementStatus.COMPLETED:
                return {
                    "status": "COMPLETED",
                    "execution": existing,
                    "already_executed": True,
                }

            if existing.status == SettlementStatus.PROCESSING:
                raise ValueError(
                    "Stocklana execution is already processing"
                )

        quote = await self.jupiter_service.get_quote(
            input_mint=self.SOL_MINT,
            output_mint=output_mint,
            amount=input_amount_lamports,
            slippage_bps=slippage_bps,
        )

        swap = await self.jupiter_service.build_swap(
            quote=quote,
            user_public_key=user_public_key,
        )

        if existing:
            execution = existing
            execution.status = SettlementStatus.PENDING
            execution.error_message = None
        else:
            execution = StocklanaExecution(
                investment_id=investment.id,
                amount_sol=Decimal(input_amount_lamports) / Decimal(1_000_000_000),
                destination=output_mint,
                source=user_public_key,
                network="mainnet",
                status=SettlementStatus.PENDING,
            )
            db.add(execution)

        db.flush()

        return {
            "status": "READY",
            "execution": execution,
            "quote": quote,
            "swap_transaction": swap["swapTransaction"],
            "last_valid_block_height": swap.get(
                "lastValidBlockHeight"
            ),
            "simulation_error": swap.get(
                "simulationError"
            ),
        }
