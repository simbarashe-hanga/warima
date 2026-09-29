from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any
from uuid import UUID

from app.services.payments.payment_models import (
    PaymentEvent,
    PaymentVerificationResult,
)


class PaymentProvider(ABC):
    """
    Provider-neutral interface for external payment providers.

    Paystack, Ozow, and future providers implement this interface.
    """

    name: str

    @abstractmethod
    def create_payment(
        self,
        *,
        amount: Decimal,
        currency: str,
        reference: str,
        member_account_id: UUID,
        email: str,
    ) -> dict[str, Any]:
        """
        Create a payment with the external provider.

        The provider receives the customer's email explicitly.
        It must not query Warima's DB for identity data.
        """
        raise NotImplementedError

    @abstractmethod
    def get_payment(
        self,
        *,
        provider_payment_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve a payment from the external provider.
        """
        raise NotImplementedError

    @abstractmethod
    def verify_payment(
        self,
        *,
        reference: str,
    ) -> PaymentVerificationResult:
        """
        Verify payment status and amount with the provider.
        using the provider transaction reference.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_webhook(
        self,
        *,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> PaymentEvent:
        """
        Validate/normalize a provider webhook into PaymentEvent.

        Provider-specific webhook parsing stays inside the adapter.
        """
        raise NotImplementedError
