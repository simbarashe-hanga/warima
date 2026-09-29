from app.services.payments.payment_provider import PaymentProvider
from app.services.payments.providers.paystack import PaystackProvider


class PaymentProviderRegistry:
    """
    Registry of configured payment providers.
    """

    def __init__(self) -> None:
        self._providers: dict[str, PaymentProvider] = {}

    def register(self, provider: PaymentProvider) -> None:
        name = provider.name.strip().lower()

        if not name:
            raise ValueError(
                "Payment provider must have a name"
            )

        self._providers[name] = provider

    def get(self, name: str) -> PaymentProvider:
        provider = self._providers.get(
            name.strip().lower()
        )

        if provider is None:
            raise ValueError(
                f"Payment provider not registered: {name}"
            )

        return provider

    def has(self, name: str) -> bool:
        return name.strip().lower() in self._providers


# ------------------------------------------------------------------
# Application payment provider registry
# ------------------------------------------------------------------

payment_provider_registry = PaymentProviderRegistry()

payment_provider_registry.register(
    PaystackProvider()
)
