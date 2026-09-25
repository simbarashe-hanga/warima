from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from uuid import UUID

from app.models.enums import PaymentStatus


@dataclass
class PaymentEvent:
    """
    Normalized payment event produced by a payment provider adapter.

    Provider-specific webhook/API payloads should be converted into
    this format before reaching PaymentService.
    """

    provider: str
    provider_payment_id: str
    reference: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    member_account_id: UUID | None = None
    raw_event: dict[str, Any] | None = None


@dataclass
class PaymentVerificationResult:
    """
    Normalized result of verifying a payment with a provider.
    """

    verified: bool
    provider_payment_id: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    reference: str | None = None
    member_account_id: UUID | None = None
    raw_response: dict[str, Any] | None = None
