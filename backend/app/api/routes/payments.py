import json
import os
from decimal import Decimal, InvalidOperation
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
)
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.member_account import MemberAccount
from app.models.payment import Payment

from app.services.payments.payment_registry import (
    payment_provider_registry,
)
from app.services.payments.payment_service import (
    PaymentService,
)

from app.services.messaging.messaging_service import send_message
from app.models.enums import PaymentStatus, IdentityProvider

router = APIRouter()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


# ---------------------------------------------------------------------------
# Payment provider verification
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_class=PlainTextResponse,
)
async def verify_payments(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    if (
        hub_mode == "subscribe"
        and hub_verify_token == VERIFY_TOKEN
    ):
        return PlainTextResponse(hub_challenge)

    raise HTTPException(
        status_code=403,
        detail="Verification failed",
    )


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "payments",
    }


# ---------------------------------------------------------------------------
# Create payment
# ---------------------------------------------------------------------------

@router.post("")
async def create_payment(
    payload: dict,
    db: Session = Depends(get_db),
):
    """
    Initialize an external payment used to fund a member wallet.

    Expected payload:

    {
        "member_account_id": "...",
        "amount": 100.00,
        "currency": "ZAR",
        "provider": "paystack"
    }

    The member's canonical User.email is used for the
    external payment provider.
    """

    # ------------------------------------------------------------------
    # Validate member account ID
    # ------------------------------------------------------------------

    raw_member_account_id = payload.get(
        "member_account_id"
    )

    if not raw_member_account_id:
        raise HTTPException(
            status_code=400,
            detail="member_account_id is required",
        )

    try:
        member_account_id = UUID(
            str(raw_member_account_id)
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid member_account_id",
        )

    # ------------------------------------------------------------------
    # Validate amount
    # ------------------------------------------------------------------

    raw_amount = payload.get("amount")

    if raw_amount is None:
        raise HTTPException(
            status_code=400,
            detail="amount is required",
        )

    try:
        amount = Decimal(str(raw_amount))
    except (InvalidOperation, TypeError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid payment amount",
        )

    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Payment amount must be greater than zero",
        )

    # ------------------------------------------------------------------
    # Validate currency
    # ------------------------------------------------------------------

    currency = str(
        payload.get("currency", "ZAR")
    ).upper().strip()

    if len(currency) != 3:
        raise HTTPException(
            status_code=400,
            detail="Currency must be a 3-letter code",
        )

    # ------------------------------------------------------------------
    # Resolve provider
    # ------------------------------------------------------------------

    provider_name = str(
        payload.get("provider", "paystack")
    ).strip().lower()

    if not provider_name:
        raise HTTPException(
            status_code=400,
            detail="Payment provider is required",
        )

    try:
        provider = payment_provider_registry.get(
            provider_name
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    # ------------------------------------------------------------------
    # Load canonical MemberAccount
    # ------------------------------------------------------------------

    member_account = (
        db.query(MemberAccount)
        .filter(
            MemberAccount.id == member_account_id
        )
        .one_or_none()
    )

    if member_account is None:
        raise HTTPException(
            status_code=404,
            detail="Member account not found",
        )

    # ------------------------------------------------------------------
    # Require canonical User
    # ------------------------------------------------------------------

    user = member_account.user

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Member account user not found",
        )

    if not user.email or not user.email.strip():
        raise HTTPException(
            status_code=400,
            detail="User email is required before creating a payment",
        )

    # ------------------------------------------------------------------
    # Create payment
    # ------------------------------------------------------------------

    try:
        payment = PaymentService.create_payment(
            db=db,
            provider=provider,
            member_account=member_account,
            amount=amount,
            currency=currency,
        )

        db.commit()

    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to create payment",
        )

    # ------------------------------------------------------------------
    # Return checkout information
    # ------------------------------------------------------------------

    return {
        "status": payment.status.value,
        "payment_id": str(payment.id),
        "reference": payment.reference,
        "provider": payment.provider,
        "provider_payment_id": payment.provider_payment_id,
        "amount": str(payment.amount),
        "currency": payment.currency,
        "payment_url": payment.payment_url,
    }


# ---------------------------------------------------------------------------
# Get payment
# ---------------------------------------------------------------------------

@router.get("/{payment_id}")
def get_payment(
    payment_id: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve a Warima payment by ID.
    """

    try:
        payment_uuid = UUID(payment_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment_id",
        )

    payment = (
        db.query(Payment)
        .filter(
            Payment.id == payment_uuid
        )
        .one_or_none()
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    return {
        "payment_id": str(payment.id),
        "reference": payment.reference,
        "provider": payment.provider,
        "provider_payment_id": payment.provider_payment_id,
        "amount": str(payment.amount),
        "currency": payment.currency,
        "status": payment.status.value,
        "payment_url": payment.payment_url,
    }


# ---------------------------------------------------------------------------
# Payment webhook
# ---------------------------------------------------------------------------

@router.post("/webhook")
async def payment_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Process a provider payment webhook.

    The raw request body is preserved because Paystack webhook
    signatures are calculated from the exact HTTP request body.
    """

    raw_body = await request.body()

    if not raw_body:
        raise HTTPException(
            status_code=400,
            detail="Empty webhook body",
        )

    # ------------------------------------------------------------------
    # Parse JSON
    # ------------------------------------------------------------------

    try:
        payload = json.loads(
            raw_body.decode("utf-8")
        )
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise HTTPException(
            status_code=400,
            detail="Invalid webhook JSON",
        )

    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=400,
            detail="Webhook payload must be a JSON object",
        )

    # Preserve the exact raw body for Paystack signature verification.
    payload["_raw_body"] = raw_body

    # ------------------------------------------------------------------
    # Resolve provider
    # ------------------------------------------------------------------

    provider_name = "paystack"

    try:
        provider = payment_provider_registry.get(
            provider_name
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    # ------------------------------------------------------------------
    # Parse and verify provider webhook
    # ------------------------------------------------------------------

    try:
        event = provider.parse_webhook(
            payload=payload,
            headers=dict(request.headers),
        )
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    # ------------------------------------------------------------------
    # Process payment
    # ------------------------------------------------------------------

    try:
        existing_payment = (
            db.query(Payment)
            .filter(
                Payment.provider == event.provider,
                Payment.reference == event.reference,
            )
            .one_or_none()
        )

        already_succeeded = (
            existing_payment is not None
            and existing_payment.status == PaymentStatus.SUCCEEDED
        )

        payment = PaymentService.process_event(
            db=db,
            event=event,
        )

        # Capture notification information before commit.
        notification = None

        if (
            not already_succeeded
            and payment.status == PaymentStatus.SUCCEEDED
        ):
            member_account = payment.member_account

            if member_account is not None:
                user = member_account.user

                if user is not None:
                    whatsapp_identity = next(
                        (
                            identity
                            for identity in user.identities
                            if identity.provider
                            == IdentityProvider.WHATSAPP
                        ),
                        None,
                    )

                    if whatsapp_identity is not None:
                        wallet = member_account.wallet

                        notification = {
                            "wa_id": (
                                whatsapp_identity.provider_identifier
                            ),
                            "amount": payment.amount,
                            "currency": payment.currency,
                            "balance": (
                                wallet.balance
                                if wallet is not None
                                else None
                            ),
                        }

        # --------------------------------------------------------------
        # Commit financial state FIRST
        # --------------------------------------------------------------

        db.commit()

    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to process payment webhook",
        )

    # ------------------------------------------------------------------
    # Notify user AFTER successful database commit
    # ------------------------------------------------------------------

    if notification is not None:
        try:
            balance_text = (
                f"{notification['currency']} "
                f"{notification['balance']:,.2f}"
                if notification["balance"] is not None
                else "your updated balance"
            )

            await send_message(
                notification["wa_id"],
                (
                    f"Your {notification['currency']} "
                    f"{notification['amount']:,.2f} deposit "
                    "was successful.\n\n"
                    "Your wallet has been credited.\n"
                    f"New wallet balance: {balance_text}"
                ),
            )

        except Exception as exc:
            print(
                "PAYMENT WHATSAPP NOTIFICATION FAILED:",
                exc,
            )

    return {
        "status": "processed",
        "payment_id": str(payment.id),
        "reference": payment.reference,
        "payment_status": payment.status.value,
    }


# ---------------------------------------------------------------------------
# Refund
# ---------------------------------------------------------------------------

@router.post("/{payment_id}/refund")
async def refund_payment(
    payment_id: str,
    payload: dict,
    db: Session = Depends(get_db),
):
    """
    Refund a payment.
    """

    raise HTTPException(
        status_code=501,
        detail="Refunds not implemented.",
    )
