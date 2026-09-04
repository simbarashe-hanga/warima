import uuid
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction
from app.models.stokvel import Stokvel
from app.models.membership import Membership

from app.models.enums import (
    WalletStatus,
    WalletTransactionStatus,
    WalletTransactionType,
    StokvelStatus,
    MembershipStatus,
)


class WalletService:
    """
    Wallet persistence and financial-operation boundary.

    This service does not commit transactions.
    The worker owns the transaction boundary.
    """

    @staticmethod
    def create_contribution(
        db: Session,
        member_account: Any,
        amount,
        stokvel_id=None,
    ) -> WalletTransaction:
        """
        Create a pending contribution request.

        if stokvel_id is provided:
        - stokvel must exist
        - stokvel must be active
        - member must have an active membershio

        This does NOT:
        - increase wallet balance
        - create ledger entries
        - mark payment as completed
        - execute blockchain transactions

        The worker is responsible for commit/rollback.
        """

        if member_account is None:
            raise ValueError("Member account is required")

        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Contribution amount must be greater than zero")

        #--------------------------------------------------------------------
        # Validate stokvel contribution
        #--------------------------------------------------------------------

        if stokvel_id is not None:
            stokvel = (
                db.query(Stokvel)
                .filter(Stokvel.id == stokvel_id)
                .one_or_none()
            )

            if stokvel is None:
                raise ValueError(
                    "Selected stokvel is not active"
                )

            membership = (
                db.query(Memebrship)
                .filter(
                    Membership.member_account_id == member_account.id,
                    Membership.stokvel_id == stokvel.id,
                    Membership.status == MembershipStatus.ACTIVE,
                )
                .one_or_more()
            )

            if membership is None:
                raise ValueError(
                    "You are not an active member of this stokvel"
                )

        #----------------------------------------------------------------------
        # Get or create wallet
        #----------------------------------------------------------------------

        wallet = (
            db.query(Wallet)
            .filter(
                Wallet.member_account_id == member_account.id,
            )
            .one_or_none()
        )

        if wallet is None:
            wallet = Wallet(
                member_account_id=member_account.id,
                currency="ZAR",
                balance=Decimal("0.00"),
                status=WalletStatus.ACTIVE,
            )

            db.add(wallet)
            db.flush()

        if wallet.status != WalletStatus.ACTIVE:
            raise ValueError("Wallet is not active")

        #----------------------------------------------------------------------
        # Create transaction
        #----------------------------------------------------------------------

        reference = f"CON-{uuid.uuid4().hex[:12].upper()}"

        transaction = WalletTransaction(
            wallet_id=wallet.id,
            stokvel_id=stokvel_id,
            transaction_type=WalletTransactionType.CONTRIBUTION,
            amount=amount,
            currency="ZAR",
            status=WalletTransactionStatus.PENDING,
            reference=reference,
            description="Community savings contribution request",
        )

        db.add(transaction)
        db.flush()

        return transaction

    @staticmethod
    def get_wallet(
        db: Session,
        member_account: Any,
    ) -> Wallet | None:
        """
        Retrieve the wallet belonging to a member account.

        This is a read-only operation.
        """

        if member_account is None:
            raise ValueError("Member account is required")

        return (
            db.query(Wallet)
            .filter(
                Wallet.member_account_id == member_account.id,
            )
            .one_or_none()
        )
