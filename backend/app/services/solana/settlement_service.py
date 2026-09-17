from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.models.enums import (
    SettlementAsset,
    SettlementStatus,
    WalletTransactionStatus,
)
from app.models.settlement import Settlement
from app.models.wallet_transaction import WalletTransaction

from app.services.solana.solana_service import SolanaService


class SettlementService:
    """
    Coordinates financial settlement with the Solana Treasury.

    Finance:
        WalletTransaction
            |
            v
    SettlementService
            |
            v
    SolanaService
            |
            v
    Solana Treasury

    WalletTransaction remains the financial record.

    Settlement records the actual external settlement
    performed through Solana.

    The caller owns the database transaction.
    """

    def __init__(
        self,
        solana_service: SolanaService | None = None,
    ):
        self.solana_service = (
            solana_service
            or SolanaService()
        )

    def validate_transaction(
        self,
        transaction: WalletTransaction,
    ) -> None:
        """
        Validate that a wallet transaction can be settled.
        """

        if transaction is None:
            raise ValueError(
                "Wallet transaction is required"
            )

        if transaction.status not in (
            WalletTransactionStatus.PENDING,
            WalletTransactionStatus.PROCESSING,
        ):
            raise ValueError(
                "Wallet transaction is not available for settlement"
            )

        if transaction.amount is None:
            raise ValueError(
                "Settlement amount is required"
            )

        amount = Decimal(
            str(transaction.amount)
        )

        if amount <= 0:
            raise ValueError(
                "Settlement amount must be greater than zero"
            )

    def get_existing_settlement(
        self,
        db: Session,
        transaction: WalletTransaction,
    ) -> Settlement | None:
        """
        Return the existing settlement for a wallet transaction.

        A wallet transaction may have only one settlement.
        """

        return (
            db.query(Settlement)
            .filter(
                Settlement.wallet_transaction_id
                == transaction.id
            )
            .one_or_none()
        )

    async def settle_to_solana(
        self,
        db: Session,
        transaction: WalletTransaction,
        destination: str,
        amount_sol: Decimal,
    ) -> dict[str, Any]:
        """
        Settle a financial transaction from the
        Warima Solana Treasury to a user's Solana wallet.

        The caller owns the database transaction.
        """

        self.validate_transaction(transaction)

        if not destination:
            raise ValueError(
                "Solana destination is required"
            )

        amount_sol = Decimal(
            str(amount_sol)
        )

        if amount_sol <= 0:
            raise ValueError(
                "SOL settlement amount must be greater than zero"
            )

        # --------------------------------------------------
        # Check for an existing settlement.
        # --------------------------------------------------

        settlement = self.get_existing_settlement(
            db,
            transaction,
        )

        if settlement is not None:

            if settlement.status == SettlementStatus.COMPLETED:
                return {
                    "success": True,
                    "transaction_id": str(
                        transaction.id
                    ),
                    "settlement_id": str(
                        settlement.id
                    ),
                    "signature": settlement.transaction_signature,
                    "amount_sol": str(
                        settlement.amount
                    ),
                    "network": settlement.network,
                    "already_settled": True,
                }

            if settlement.status in (
                SettlementStatus.PROCESSING,
                SettlementStatus.PENDING,
            ):
                raise ValueError(
                    "A settlement is already in progress "
                    "for this wallet transaction. "
                    "Reconciliation is required before retrying."
                )

            if settlement.status == SettlementStatus.FAILED:
                # A failed settlement can be retried.
                settlement.status = SettlementStatus.PENDING
                settlement.error_message = None

            elif settlement.status == SettlementStatus.CANCELLED:
                raise ValueError(
                    "Settlement has been cancelled"
                )

        # --------------------------------------------------
        # Create the settlement record if necessary.
        # --------------------------------------------------

        if settlement is None:
            settlement = Settlement(
                wallet_transaction_id=transaction.id,
                asset=SettlementAsset.SOL,
                amount=amount_sol,
                destination=destination,
                network=(
                    getattr(
                        self.solana_service,
                        "network",
                        None,
                    )
                    or "devnet"
                ),
                status=SettlementStatus.PENDING,
            )

            db.add(settlement)
            db.flush()

        else:
            settlement.amount = amount_sol
            settlement.destination = destination
            settlement.status = SettlementStatus.PENDING

            db.flush()

        # --------------------------------------------------
        # Mark both records as processing.
        # --------------------------------------------------

        transaction.status = (
            WalletTransactionStatus.PROCESSING
        )

        settlement.status = (
            SettlementStatus.PROCESSING
        )

        db.flush()

        # --------------------------------------------------
        # Load Warima's Solana Treasury signer.
        # --------------------------------------------------

        treasury = (
            self.solana_service
            .get_treasury_keypair()
        )

        # --------------------------------------------------
        # Execute the on-chain transfer.
        # --------------------------------------------------

        result = await self.solana_service.send_sol(
            sender=treasury,
            recipient=destination,
            amount_sol=float(amount_sol),
        )

        # --------------------------------------------------
        # Handle Solana failure.
        # --------------------------------------------------

        if not result.get("success"):

            error = result.get(
                "error",
                "Solana settlement failed",
            )

            settlement.status = (
                SettlementStatus.FAILED
            )

            settlement.error_message = str(
                error
            )[:500]

            transaction.status = (
                WalletTransactionStatus.FAILED
            )

            db.flush()

            return {
                "success": False,
                "transaction_id": str(
                    transaction.id
                ),
                "settlement_id": str(
                    settlement.id
                ),
                "error": error,
            }

        # --------------------------------------------------
        # Successful Solana settlement.
        # --------------------------------------------------

        signature = result.get("signature")

        if not signature:
            settlement.status = (
                SettlementStatus.FAILED
            )

            settlement.error_message = (
                "Solana transfer succeeded but "
                "no transaction signature was returned"
            )

            transaction.status = (
                WalletTransactionStatus.FAILED
            )

            db.flush()

            return {
                "success": False,
                "transaction_id": str(
                    transaction.id
                ),
                "settlement_id": str(
                    settlement.id
                ),
                "error": (
                    "No Solana transaction signature returned"
                ),
            }

        settlement.transaction_signature = signature
        settlement.status = SettlementStatus.COMPLETED
        settlement.error_message = None

        transaction.status = (
            WalletTransactionStatus.COMPLETED
        )

        db.flush()

        return {
            "success": True,
            "transaction_id": str(
                transaction.id
            ),
            "settlement_id": str(
                settlement.id
            ),
            "signature": signature,
            "amount_sol": str(
                amount_sol
            ),
            "network": result.get(
                "network",
                settlement.network,
            ),
            "already_settled": False,
        }
