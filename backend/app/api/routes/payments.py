from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "payments",
    }


@router.post("")
async def create_payment(
        payload: dict,
        db: Session = Depends(get_db),
):
    """
    Create a new payment.

    Expected payload (example):

    { 
        "user_id": "...",
        "group_id": "...",
        "amount": 1000.00,
        "currency": "ZAR",
        "provider": "meta"
    }
    """

    # TODO:
    # - Validate payload
    # - Create payment record
    # - Generate payment request
    # - Return checkout/payment information

    return {
        "status": "pending",
        "message": "Payment creation not yet implemented.",
        "payload": payload,
    }


@router.get("/{payment_id}")
def get_payment(
    payment_id: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve payment status
    """

    # TODO:
    # Query payment from database

    return {
        "payment_id": payment_id,
        "status": "npt_implemented",
    }


@router.post("/webhook")
async def payment_webhook(
    payload: dict,
    db : Session = Depends(get_db),
):
    """
    Endpoint for payment provider callbacks.

    Meta, Ozow, Paystack, Stripe, SOLnova.
    """

    # TODO:
    # Verify webhoo signature
    # Check idempotency
    # Update payment status
    # Queue downstream processing

    print("PAYMENT WEBHOOK:", payload)

    return {
        "status": "received",
    }


@router.post("/{payment_id}/refund")
async def refund_payment(
    payment_id: str,
    payload: dict,
    db: Session = Depends(get_db),
):
    """
    Refund a payment.
    """

    # TODO:
    # Process refund through provider

    raise HTTPException(
        status_code=501,
        detail="Refunds not implemented.",
    )
