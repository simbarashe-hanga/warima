import asyncio
import base64
from decimal import Decimal

from solana.rpc.async_api import AsyncClient
from sqlalchemy.orm import Session
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction

from app.core.config import settings
from app.models.enums import SettlementStatus
from app.models.stokvel_investment import StokvelInvestment
from app.models.stocklana_execution import StocklanaExecution
from app.services.investment.jupiter_service import JupiterService
from app.services.solana.solana_service import SolanaService


class StocklanaExecutionService:
    """
    Prepares and executes the on-chain transaction associated with
    a Stocklana collective investment.

    StokvelInvestment remains the ZAR accounting/business record.

    StocklanaExecution records the external Solana execution.

    The execution wallet is the configured Warima Solana treasury
    wallet.

    This service does not:
    - create investments
    - create contributions
    - modify the treasury ledger
    - convert ZAR into SOL
    - activate the StokvelInvestment

    Investment activation and treasury accounting are handled by
    InvestmentExecutionService after successful blockchain execution.
    """

    SOL_MINT = "So11111111111111111111111111111111111111112"

    def __init__(
        self,
        jupiter_service: JupiterService | None = None,
        solana_service: SolanaService | None = None,
    ):
        self.jupiter_service = (
            jupiter_service or JupiterService()
        )
        self.solana_service = (
            solana_service or SolanaService()
        )

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
                amount_sol=(
                    Decimal(input_amount_lamports)
                    / Decimal(1_000_000_000)
                ),
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

    @staticmethod
    def inspect_transaction_signers(
        swap_transaction: str,
    ) -> dict:
        """
        Decode a Jupiter transaction and inspect its required signers

        This method does not sign or broadcast the transaction.
        """

        if not swap_transaction:
            raise ValueError(
                "Jupiter swap transaction is required"
            )

        raw_transaction = base64.b64decode(
            swap_transaction
        )

        transaction = VersionedTransaction.from_bytes(
            raw_transaction
        )

        message = transaction.message
        account_keys = message.account_keys
        header = message.header

        required_signer_count = (
            header.num_required_signatures
        )

        required_signers = [
            str(account_keys[index])
            for index in range(required_signer_count)
        ]

        return {
            "required_signer_count": required_signer_count,
            "required_signers": required_signers,
            "account_count": len(account_keys),
        }

    async def execute(
        self,
        db: Session,
        investment: StokvelInvestment,
        execution: StocklanaExecution,
        swap_transaction: str,
    ) -> StocklanaExecution:

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

        if execution.status == SettlementStatus.COMPLETED:
            return execution

        if execution.status not in (
            SettlementStatus.PENDING,
            SettlementStatus.FAILED,
        ):
            raise ValueError(
                f"Stocklana execution cannot start from status "
                f"{execution.status.value}"
            )

        if not swap_transaction:
            raise ValueError(
                "Jupiter swap transaction is required"
            )

        treasury_keypair = (
            self.solana_service.get_treasury_keypair()
        )

        treasury_address = str(
            treasury_keypair.pubkey()
        )

        if execution.source != treasury_address:
            raise ValueError(
                "Stocklana execution source does not match "
                "the configured Warima Solana treasury"
            )

        if self.solana_service.network != "mainnet":
            raise ValueError(
                "Stocklana execution requires Solana mainnet"
            )

        execution.status = SettlementStatus.PROCESSING
        execution.error_message = None
        db.flush()

        try:
            raw_transaction = base64.b64decode(
                swap_transaction
            )

            unsigned_transaction = (
                VersionedTransaction.from_bytes(
                    raw_transaction
                )
            )

            message = unsigned_transaction.message
            account_keys = message.account_keys
            required_signer_count = (
                message.header.num_required_signatures
            )

            required_signers = [
                str(account_keys[index])
                for index in range(required_signer_count)
            ]

            if required_signer_count != 1:
                raise ValueError(
                    "Unexpected Jupiter transaction signer count: "
                    f"{required_signer_count}"
                )

            if required_signers[0] != treasury_address:
                raise ValueError(
                    "Warima treasury is not the required signer "
                    "of the Jupiter transaction"
                )

            signed_transaction = VersionedTransaction(
                message,
                [treasury_keypair],
            )

            client = await self.solana_service.get_client()

            try:
                response = await client.send_raw_transaction(
                    bytes(signed_transaction)
                )

                signature = str(response.value)

                execution.transaction_signature = signature

                confirmed = False

                for _ in range(30):
                    status_response = (
                        await client.get_signature_statuses(
                            [response.value],
                            search_transaction_history=True,
                        )
                    )

                    if status_response.value:
                        status = status_response.value[0]

                        if status is not None:
                            if status.err is not None:
                                raise RuntimeError(
                                    f"Stocklana transaction failed: "
                                    f"{status.err}"
                                )

                            if status.confirmation_status is not None:
                                confirmed = True
                                break

                    await asyncio.sleep(2)

                if not confirmed:
                    raise RuntimeError(
                        "Stocklana transaction was submitted but "
                        "confirmation was not observed"
                    )

            finally:
                await client.close()

            execution.status = SettlementStatus.COMPLETED
            execution.error_message = None

            db.flush()

            return execution

        except Exception as exc:
            execution.status = SettlementStatus.FAILED
            execution.error_message = str(exc)[:500]

            db.flush()

            raise
