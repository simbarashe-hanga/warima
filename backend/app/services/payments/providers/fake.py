from decimal import Decimal
from typing import Any
from uuid import UUID

from app.models.enums import PaymentStatus
from app.services.payments.payment_models import (
    PaymentEvent,
    PaymentVerificationResult,
)
from app.services.payments.payment_provider import PaymentProvider


class FakePaymentProvider(PaymentProvider):
    """
    Development-only payment provider.

    This provider does not move real money.
    It allows us to exercise the complete Warima payment flow.
    """

    name = "fake"

    def __init__(self) -> None:
        self.payments: dict[str, dict[str, Any]] = {}

    def create_payment(
        self,
        *,
        amount: Decimal,
        currency: str,
        reference: str,
        member_account_id: UUID,
    ) -> dict[str, Any]:
        provider_payment_id = f"fake_{reference}"

        # Keep provider state JSON-safe.
        payment = {
            "provider_payment_id": provider_payment_id,
            "reference": reference,
            "member_account_id": str(member_account_id),
            "amount": str(amount),
            "currency": currency,
            "status": PaymentStatus.PENDING.value,
            "payment_url": (
                f"https://fake.warima.local/pay/{provider_payment_id}"
            ),
        }

        self.payments[provider_payment_id] = payment

        return payment

    def get_payment(
        self,
        *,
        provider_payment_id: str,
    ) -> dict[str, Any]:
        payment = self.payments.get(provider_payment_id)

        if payment is None:
            raise ValueError(
                f"Fake payment not found: {provider_payment_id}"
            )

        return payment

    def verify_payment(
        self,
        *,
        provider_payment_id: str,
    ) -> PaymentVerificationResult:
        payment = self.get_payment(
            provider_payment_id=provider_payment_id
        )

        return PaymentVerificationResult(
            verified=(
                payment["status"]
                == PaymentStatus.SUCCEEDED.value
            ),
            provider_payment_id=provider_payment_id,
            amount=Decimal(payment["amount"]),
            currency=payment["currency"],
            status=PaymentStatus(payment["status"]),
            reference=payment["reference"],
            member_account_id=UUID(payment["member_account_id"]),
            raw_response=payment,
        )

    def parse_webhook(
        self,
        *,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> PaymentEvent:
        return PaymentEvent(
            provider=self.name,
            provider_payment_id=payload["provider_payment_id"],
            reference=payload["reference"],
            member_account_id=(
                UUID(payload["member_account_id"])
                if payload.get("member_account_id")
                else None
            ),
            amount=Decimal(str(payload["amount"])),
            currency=payload["currency"],
            status=PaymentStatus(payload["status"]),
            raw_event=payload,
        )

    def mark_succeeded(
        self,
        *,
        provider_payment_id: str,
    ) -> dict[str, Any]:
        payment = self.get_payment(
            provider_payment_id=provider_payment_id
        )

        payment["status"] = PaymentStatus.SUCCEEDED.value

        return payment

    def mark_failed(
        self,
        *,
        provider_payment_id: str,
    ) -> dict[str, Any]:
        payment = self.get_payment(
            provider_payment_id=provider_payment_id
        )

        payment["status"] = PaymentStatus.FAILED.value

        return payment
