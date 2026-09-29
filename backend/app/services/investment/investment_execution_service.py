from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import (
    SettlementStatus,
    StokvelInvestmentStatus,
)
from app.models.stokvel_investment import StokvelInvestment
from app.models.stocklana_execution import StocklanaExecution
from app.services.treasury.treasury_ledger_service import (
    TreasuryLedgerService,
)

from app.core.config import settings


class InvestmentExecutionService:
    """
    Coordinates the execution lifecycle of a StokvelInvestment.

    Investment creation is handled by StokvelInvestmentService.

    This service owns the boundary between:
        PENDING investment
            ->
        external execution
            ->
        ACTIVE investment

    It does not:
    - create investments
    - create contributions
    - create wallets
    - perform ZAR -> SOL conversion
    - commit the database transaction

    The caller owns the database transaction.
    """

    @staticmethod
    def finalize_stocklana_execution(
        db: Session,
        investment: StokvelInvestment,
        execution: StocklanaExecution,
    ) -> StokvelInvestment:

        if investment is None:
            raise ValueError(
                "Investment is required"
            )

        if execution is None:
            raise ValueError(
                "Stocklana execution is required"
            )

        if execution.investment_id != investment.id:
            raise ValueError(
                "Stocklana execution does not belong to investment"
            )

        # --------------------------------------------------------------
        # Idempotency
        # --------------------------------------------------------------
        #
        # If the investment is already ACTIVE, the external execution
        # has already been finalized from the investment perspective.
        #
        # Do not debit the treasury a second time.
        # --------------------------------------------------------------

        if investment.status == StokvelInvestmentStatus.ACTIVE:

            if execution.status != SettlementStatus.COMPLETED:
                raise ValueError(
                    "Active investment requires completed Stocklana execution"
                )

            return investment

        # --------------------------------------------------------------
        # Investment lifecycle validation
        # --------------------------------------------------------------

        if investment.status != StokvelInvestmentStatus.PENDING:
            raise ValueError(
                f"Investment cannot be finalized from status "
                f"{investment.status.value}"
            )

        # --------------------------------------------------------------
        # External execution validation
        # --------------------------------------------------------------

        if execution.status != SettlementStatus.COMPLETED:
            raise ValueError(
                "Stocklana execution must be COMPLETED "
                "before investment can be activated"
            )

        if not execution.transaction_signature:
            raise ValueError(
                "Completed Stocklana execution requires "
                "a transaction signature"
            )

        # --------------------------------------------------------------
        # Resolve stokvel treasury
        # --------------------------------------------------------------

        treasury = investment.stokvel.treasury

        if treasury is None:
            raise ValueError(
                "Investment stokvel does not have a treasury"
            )

        # --------------------------------------------------------------
        # Verify treasury balance again at execution boundary
        # --------------------------------------------------------------

        treasury_balance = TreasuryLedgerService.get_balance(
            db,
            treasury,
        )

        investment_amount = Decimal(
            str(investment.amount)
        )

        if treasury_balance < investment_amount:
            raise ValueError(
                f"Insufficient treasury balance for investment execution: "
                f"available={treasury_balance}, "
                f"required={investment_amount}"
            )

        # --------------------------------------------------------------
        # Record deployment of treasury funds
        # --------------------------------------------------------------

        TreasuryLedgerService.record_investment_debit(
            db,
            treasury,
            investment_amount,
            investment.id,
        )

        # --------------------------------------------------------------
        # Activate investment
        # --------------------------------------------------------------

        investment.status = StokvelInvestmentStatus.ACTIVE

        db.flush()

        return investment

    @staticmethod
    async def execute_stocklana_investment(
        db: Session,
        investment: StokvelInvestment,
        output_mint: str,
        input_amount_lamports: int,
        slippage_bps: int = 50,
    ) -> StokvelInvestment:
        """
        Execute a Stocklana investment from preparation through
        blockchain confirmation and final investment activation.

        Lifecycle:

            PENDING investment
                ->
            Jupiter preparation
                ->
            Solana mainnet execution
                ->
            StocklanaExecution COMPLETED
                ->
            Treasury investment debit
                ->
            Investment ACTIVE

        This method does not convert ZAR into SOL.

        input_amount_lamports is an explicit on-chain execution
        amount supplied by the caller.

        The configured Warima Solana treasury is the execution
        wallet.
        """

        if investment is None:
            raise ValueError(
                "Investment is required"
            )

        if investment.status != StokvelInvestmentStatus.PENDING:
            raise ValueError(
                f"Stocklana investment must be PENDING, "
                f"got {investment.status.value}"
            )

        if input_amount_lamports <= 0:
            raise ValueError(
                "Stocklana input amount must be positive"
            )

        from app.services.investment.stocklana_execution_service import (
            StocklanaExecutionService,
        )
        from app.services.solana.solana_service import (
            SolanaService,
        )

        solana_service = SolanaService(
            rpc_url=settings.STOCKLANA_SOLANA_RPC_URL,
            network=settings.STOCKLANA_SOLANA_NETWORK,
            treasury_keypair_file=(
                settings.STOCKLANA_SOLANA_TREASURY_KEYPAIR_FILE
            ),
        )

        treasury_address = (
            solana_service.get_treasury_address()
        )

        execution_service = StocklanaExecutionService(
            solana_service=solana_service,
        )

        prepared = await execution_service.prepare(
            db=db,
            investment=investment,
            output_mint=output_mint,
            input_amount_lamports=input_amount_lamports,
            user_public_key=treasury_address,
            slippage_bps=slippage_bps,
        )

        if prepared["status"] == "COMPLETED":
            execution = prepared["execution"]

        else:
            execution = await execution_service.execute(
                db=db,
                investment=investment,
                execution=prepared["execution"],
                swap_transaction=prepared["swap_transaction"],
            )

        return InvestmentExecutionService.finalize_stocklana_execution(
            db=db,
            investment=investment,
            execution=execution,
        )
