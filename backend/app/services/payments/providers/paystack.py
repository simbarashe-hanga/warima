import hashlib
import hmac
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID

import httpx

from app.core.config import settings
from app.models.enums import PaymentStatus
from app.services.payments.payment_models import (
    PaymentEvent,
    PaymentVerificationResult,
)
from app.services.payments.payment_provider import PaymentProvider


class PaystackProvider(PaymentProvider):
    """
    Paystack implementation of the provider-neutral payment interface.

    This adapter is responsible only for communication with Paystack
    and normalization of Paystack responses/events.

    It does not:
    - access the database
    - modify wallets
    - create Payment records
    - commit database transactions
    - implement Warima business logic
    """

    name = "paystack"

    def __init__(
        self,
        *,
        secret_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.secret_key = (
            secret_key or settings.PAYSTACK_SECRET_KEY
        ).strip()

        self.base_url = (
            base_url or settings.PAYSTACK_BASE_URL
        ).rstrip("/")

        self.timeout = timeout

        if not self.secret_key:
            raise ValueError(
                "PAYSTACK_SECRET_KEY is not configured"
            )

    # ------------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------------

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _post(
        self,
        path: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"

        try:
            with httpx.Client(
                timeout=self.timeout,
                headers=self._headers(),
            ) as client:
                response = client.post(
                    url,
                    json=payload,
                )
        except httpx.HTTPError as exc:
            raise ValueError(
                f"Paystack request failed: {exc}"
            ) from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise ValueError(
                "Paystack returned an invalid JSON response"
            ) from exc

        if response.is_error:
            message = data.get(
                "message",
                response.text,
            )

            raise ValueError(
                f"Paystack API error: {message}"
            )

        return data

    def _get(
        self,
        path: str,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"

        try:
            with httpx.Client(
                timeout=self.timeout,
                headers=self._headers(),
            ) as client:
                response = client.get(url)
        except httpx.HTTPError as exc:
            raise ValueError(
                f"Paystack request failed: {exc}"
            ) from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise ValueError(
                "Paystack returned an invalid JSON response"
            ) from exc

        if response.is_error:
            message = data.get(
                "message",
                response.text,
            )

            raise ValueError(
                f"Paystack API error: {message}"
            )

        return data

    # ------------------------------------------------------------------
    # Amount conversion
    # ------------------------------------------------------------------

    @staticmethod
    def _to_subunit(amount: Decimal) -> int:
        """
        Convert a Warima decimal amount into the smallest
        currency unit expected by Paystack.

        Example:

            R100.50 -> 10050
        """

        try:
            amount = Decimal(str(amount))
        except (InvalidOperation, TypeError) as exc:
            raise ValueError(
                "Invalid payment amount"
            ) from exc

        if amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero"
            )

        subunit = amount * Decimal("100")

        if subunit != subunit.to_integral_value():
            raise ValueError(
                "Payment amount has more than two decimal places"
            )

        return int(subunit)

    # ------------------------------------------------------------------
    # Create payment
    # ------------------------------------------------------------------

    def create_payment(
        self,
        *,
        amount: Decimal,
        currency: str,
        reference: str,
        member_account_id: UUID,
        email: str,
    ) -> dict[str, Any]:
        if not email or not email.strip():
            raise ValueError(
                "Customer email is required for Paystack"
            )

        currency = currency.upper().strip()

        payload = {
            "email": email.strip().lower(),
            "amount": self._to_subunit(amount),
            "currency": currency,
            "reference": reference,
        }

        response = self._post(
            "/transaction/initialize",
            payload,
        )

        if response.get("status") is not True:
            raise ValueError(
                response.get(
                    "message",
                    "Paystack payment initialization failed",
                )
            )

        data = response.get("data") or {}

        provider_payment_id = data.get("reference")

        if not provider_payment_id:
            raise ValueError(
                "Paystack did not return a transaction reference"
            )

        authorization_url = data.get(
            "authorization_url"
        )

        return {
            "provider_payment_id": provider_payment_id,
            "payment_url": authorization_url,
            "reference": data.get(
                "reference",
                reference,
            ),
            "access_code": data.get("access_code"),
            "status": data.get("status"),
            "provider": self.name,
            "raw_response": response,
        }

    # ------------------------------------------------------------------
    # Get payment
    # ------------------------------------------------------------------

    def get_payment(
        self,
        *,
        provider_payment_id: str,
    ) -> dict[str, Any]:
        if not provider_payment_id:
            raise ValueError(
                "Paystack transaction reference is required"
            )

        response = self._get(
            f"/transaction/{provider_payment_id}"
        )

        if response.get("status") is not True:
            raise ValueError(
                response.get(
                    "message",
                    "Unable to retrieve Paystack transaction",
                )
            )

        return response

    # ------------------------------------------------------------------
    # Verify payment
    # ------------------------------------------------------------------

    def verify_payment(
        self,
        *,
        reference: str,
    ) -> PaymentVerificationResult:
        if not reference:
            raise ValueError(
                "Payment reference is required"
            )

        response = self._get(
            f"/transaction/verify/{reference}"
        )

        if response.get("status") is not True:
            raise ValueError(
                response.get(
                    "message",
                    "Paystack verification failed",
                )
            )

        data = response.get("data") or {}

        provider_payment_id = data.get(
            "reference"
        )

        if not provider_payment_id:
            raise ValueError(
                "Paystack verification did not return a reference"
            )

        amount = Decimal(
            str(data.get("amount", 0))
        ) / Decimal("100")

        currency = str(
            data.get("currency", "")
        ).upper()

        status = self._map_status(
            data.get("status")
        )

        verified = (
            status == PaymentStatus.SUCCEEDED
            and data.get("gateway_response") is not None
        )

        return PaymentVerificationResult(
            verified=verified,
            provider_payment_id=provider_payment_id,
            amount=amount,
            currency=currency,
            status=status,
            reference=data.get("reference"),
            member_account_id=None,
            raw_response=response,
        )

    # ------------------------------------------------------------------
    # Webhook
    # ------------------------------------------------------------------

    def parse_webhook(
        self,
        *,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> PaymentEvent:
        headers = headers or {}

        signature = self._get_signature(headers)

        if not signature:
            raise ValueError(
                "Missing Paystack webhook signature"
            )

        raw_body = payload.get("_raw_body")

        if raw_body is None:
            raise ValueError(
                "Raw webhook body is required for signature validation"
            )

        if isinstance(raw_body, str):
            raw_body = raw_body.encode("utf-8")

        expected_signature = hmac.new(
            self.secret_key.encode("utf-8"),
            raw_body,
            hashlib.sha512,
        ).hexdigest()

        if not hmac.compare_digest(
            expected_signature,
            signature,
        ):
            raise ValueError(
                "Invalid Paystack webhook signature"
            )

        event_name = payload.get("event")

        data = payload.get("data") or {}

        provider_payment_id = data.get(
            "reference"
        )

        if not provider_payment_id:
            raise ValueError(
                "Paystack webhook is missing transaction reference"
            )

        amount = Decimal(
            str(data.get("amount", 0))
        ) / Decimal("100")

        currency = str(
            data.get("currency", "")
        ).upper()

        # Keep the raw HTTP body for signature verification only.
        # It contains bytes and must not be persisted into JSON.
        raw_event = {
            key: value
            for key, value in payload.items()
            if key != "_raw_body"
        }

        return PaymentEvent(
            provider=self.name,
            provider_payment_id=provider_payment_id,
            reference=provider_payment_id,
            amount=amount,
            currency=currency,
            status=self._map_webhook_status(
                event_name,
                data.get("status"),
            ),
            member_account_id=None,
            raw_event=raw_event,
        )

    # ------------------------------------------------------------------
    # Status mapping
    # ------------------------------------------------------------------

    @staticmethod
    def _map_status(
        status: str | None,
    ) -> PaymentStatus:
        normalized = (
            str(status).lower().strip()
            if status is not None
            else ""
        )

        if normalized == "success":
            return PaymentStatus.SUCCEEDED

        if normalized in {
            "failed",
            "abandoned",
        }:
            return PaymentStatus.FAILED

        if normalized in {
            "reversed",
        }:
            return PaymentStatus.REFUNDED

        return PaymentStatus.PENDING

    @staticmethod
    def _map_webhook_status(
        event_name: str | None,
        transaction_status: str | None,
    ) -> PaymentStatus:
        event = (
            str(event_name).lower().strip()
            if event_name
            else ""
        )

        if event == "charge.success":
            return PaymentStatus.SUCCEEDED

        return PaystackProvider._map_status(
            transaction_status
        )

    @staticmethod
    def _get_signature(
        headers: dict[str, str],
    ) -> str | None:
        for key, value in headers.items():
            if key.lower() == "x-paystack-signature":
                return value.strip()

        return None
