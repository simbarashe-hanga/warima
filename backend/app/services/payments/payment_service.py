import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.enums import PaymentStatus

from app.services.payments.payment_provider import PaymentProvider
from app.services.payments.payment_models import PaymentEvent, PaymentVerificationResult
from app.services.wallet.wallet_service import WalletService


class PaymentService:
    """
    Provider neutral payment orchastration service

    Responsibilities:
    - create payment record
    - communitcate with payment providers through PaymentProvider
    - process normalized payment events
    - enforce payment idempotency
    - verify payment amount/currency
    - fund member wallet after verified success

    This service does not commit.
    The caller owns the database transaction boundary
    """

    @staticmethod
    def create_payment(
        db: Session,
        provider: PaymentProvider,
        member_account,
        amount,
        currency: str = "ZAR",
    ) -> Payment:
        """
        Create a Warima payment and initialize it with provider
        """

        if member_account is None:
            raise ValueError("Member account is required")

        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Payment must be greater than zero")

        currency = currency.upper().strip()

        if len(currency) != 3:
            raise ValueError("Currency must be a 3-letter code")

        reference = (f"PAY-{uuid.uuid4().hex[:12].upper()}")

        payment = Payment(
            member_account_id=member_account.id,
            provider=provider.name,
            amount=amount,
            currency=currency,
            status=PaymentStatus.CREATED,
            reference=reference,
        )

        db.add(payment)
        db.flush()

        try:
            provider_result = provider.create_payment(
                amount=amount,
                currency=currency,
                reference=reference,
                member_account_id=member_account.id,
            )

            provider_payment_id = provider_result.get(
                "provider_payment_id"
            )

            if not provider_payment_id:
                raise ValueError(
                    "Payment provider did not return a payment ID"
                )

            payment.provider_payment_id = provider_payment_id

            payment.payment_url = provider_result.get(
                "payment_url"
            )

            payment.provider_metadata = provider_result

            payment.status = PaymentStatus.PENDING

            db.flush()

            return payment

        except Exception:
            payment.status = PaymentStatus.FAILED
            db.flush()
            raise

    @staticmethod
    def process_event(
        db: Session,
        event: PaymentEvent,
    ) -> Payment:
        """
        Process a normalized provider payment event.

        A successful event results in wallet funding.

        Repeated successful event are idempotent:
        once the payment has funded the wallet, subsequent events
        do not create another wallet deposit
        """

        payment = (
            db.query(Payment)
            .filter(
                Payment.provider == event.provider,
                Payment.reference == event.reference,
            )
            .one_or_none()
        )

        if payment is None:
            raise ValueError(
                f"Payment not found for reference: "
                f"{event.reference}"
            )

        # -------------------------------------------------------------------------------
        # Idempotency
        # -------------------------------------------------------------------------------

        if payment.status == PaymentStatus.SUCCEEDED:
            return payment

        # -------------------------------------------------------------------------------
        # Validate provider payment ID
        # -------------------------------------------------------------------------------

        if (
            payment.provider_payment_id is not None
            and payment.provider_payment_id
            != event.provider_payment_id
        ):
            raise ValueError(
                "Provider payment ID does not match payment record"
            )

        # ------------------------------------------------------------------------------
        # Validate amount
        # ------------------------------------------------------------------------------
        
        event_amount = Decimal(str(event.amount))

        if event_amount != Decimal(str(payment.amount)):
            raise ValueError(
                "Payment amount does not match payment record"
            )

        # -------------------------------------------------------------------------------
        # Validate currency
        # -------------------------------------------------------------------------------

        if event.currency.upper() != payment.currency.upper():
            raise ValueError(
                "Payment currency does not match payment record"
            )

        # -------------------------------------------------------------------------------
        # Store provider payment ID if not already known
        # -------------------------------------------------------------------------------

        if payment.provider_payment_id is None:
            payment.provider_payment_id = (
                event.provider_payment_id
            )

        # ------------------------------------------------------------------------------
        # Store provider event
        # ------------------------------------------------------------------------------

        payment.provider_metadata = event.raw_event

        # ------------------------------------------------------------------------------
        # Handle successful payment
        #-------------------------------------------------------------------------------

        if event.status == PaymentStatus.SUCCEEDED:
            PaymentService._complete_successful_payment(
                db,
                payment,
            )

            return payment

        # -----------------------------------------------------------------------------
        # Handle non-success states
        # -----------------------------------------------------------------------------
        if event.status == PaymentStatus.FAILED:
            payment.status = PaymentStatus.FAILED

        elif event.status == PaymentStatus.CANCELLED:
            payment.status = PaymentStatus.CANCELLED

        elif event.status == PaymentStatus.REFUNDED:
            payment.status = PaymentStatus.REFUNDED

        elif event.status == PaymentStatus.PENDING:
            payment.status = PaymentStatus.PENDING

        elif event.status == PaymentStatus.CREATED:
            payment.status = PaymentStatus.CREATED

        else:
            raise ValueError(
                f"Unsupported payment status: {event.status}"
            )

        db.flush()

        return payment


    @staticmethod
    def process_verification(
        db: Session,
        payment: Payment,
        verification: PaymentVerificationResult,
    ) -> Payment:
        """
        Process a provider verification result

        This is useful when Warima verifies a payment directly with
        the provider instead of relying soley on a webhook.
        """

        if payment.status == PaymentStatus.SUCCEEDED:
            return payment

        if (
            payment.provider_payment_id is not None
            and payment.provider_payment_id
            != verification.provider_payment_id
        ):
            raise ValueError(
                "Provider payment ID does not match payment record"
            )

        verified_amount = Decimal(
            str(verification.amount)
        )

        if verified_amount != Decimal(str(payment.amount)):
            raise ValueError(
                "Verified payment amount does not match payment"
            )

        if (
            verification.currency.upper()
            != payment.currency.upper()
        ):
            raise ValueError(
                "Verified payment currency does not match payment"
            )

        payment.provider_payment_id = (
            verification.provider_payment_id
        )

        payment.provider_metadata = (
            verification.raw_response
        )

        if not verification.verified:
            payment.status = verification.status
            db.flush()
            return payment

        if verification.status != PaymentStatus.SUCCEEDED:
            raise ValueError(
                "Payment verification is not successful"
            )

        PaymentService._complete_successful_payment(
            db,
            payment,
        )

        return payment

    @staticmethod
    def _complete_successful_payment(
        db : Session,
        payment: Payment,
    ) -> None:
        """
        Convert a verified external payment into wallet funds.

        This method is deliberately the only place in PaymentService
        where a successful payment crosses into the wallet layer
        """

        if payment.status == PaymentStatus.SUCCEEDED:
            return

        member_account = payment.member_account

        if member_account is None:
            raise ValueError(
                "Payment member account could not be loaded"
            )

        WalletService.deposit(
            db,
            member_account,
            payment.amount,
            reference=f"PAY-{payment.reference}",
            description=(
                f"External payment via {payment.provider}"
            ),
        )

        payment.status = PaymentStatus.SUCCEEDED

        db.flush()
