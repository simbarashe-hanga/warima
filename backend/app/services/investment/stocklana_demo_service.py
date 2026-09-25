from app.models.stokvel_investment import StokvelInvestment
from app.services.investment.stocklana_execution_service import (
    StocklanaExecutionService,
)


class StocklanaDemoService:
    """
    Demo-only bridge between a recorded Stocklana investment
    and the real Jupiter transaction-preparation boundary.

    The ZAR investment amount is NOT converted into SOL here.
    The SOL amount is an explicitly supplied execution-demo amount.
    """

    OPENAI_PRESTOCK_MINT = (
        "PreweJYECqtQwBtpxHL171nL2K6umo692gTm7Q3rpgF"
    )

    DEMO_WALLET = (
        "J1sDpy23voeqyB1yU7J7A8HGnehVL8BJ3LMNb2o8LSLN"
    )

    DEMO_SOL_LAMPORTS = 10_000_000  # 0.01 SOL

    def __init__(self):
        self.execution_service = StocklanaExecutionService()

    async def prepare(
        self,
        db,
        investment: StokvelInvestment,
    ):
        return await self.execution_service.prepare(
            db=db,
            investment=investment,
            output_mint=self.OPENAI_PRESTOCK_MINT,
            input_amount_lamports=self.DEMO_SOL_LAMPORTS,
            user_public_key=self.DEMO_WALLET,
            slippage_bps=50,
        )
