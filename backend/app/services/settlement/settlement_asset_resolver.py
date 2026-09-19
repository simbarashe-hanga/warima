from dataclasses import dataclass
from decimal import Decimal

from app.models.enums import (
    SettlementAsset,
    TreasuryDenomination,
)
from app.models.stokvel_treasury import StokvelTreasury
from app.models.wallet_transaction import WalletTransaction


@dataclass(frozen=True)
class SettlementAssetResolution:
    source_currency: str
    source_amount: Decimal
    target_asset: SettlementAsset
    target_amount: Decimal | None
    conversion_required: bool


class SettlementAssetResolver:
    """
    Resolves the target settlement asset for a wallet transaction.

    WalletTransaction represents the source financial obligation.

    Settlement represents the target asset actually used
    by the settlement rail.

    This resolver does NOT perform FX/token conversion.
    """

    @staticmethod
    def resolve(
        transaction: WalletTransaction,
        treasury: StokvelTreasury,
    ) -> SettlementAssetResolution:

        if transaction is None:
            raise ValueError(
                "Wallet transaction is required"
            )

        if treasury is None:
            raise ValueError(
                "Treasury is required"
            )

        if transaction.amount is None:
            raise ValueError(
                "Wallet transaction amount is required"
            )

        source_currency = str(
            transaction.currency
        ).upper()

        source_amount = Decimal(
            str(transaction.amount)
        )

        if source_amount <= 0:
            raise ValueError(
                "Wallet transaction amount must be "
                "greater than zero"
            )

        denomination = treasury.denomination

        if isinstance(denomination, str):
            denomination = TreasuryDenomination(
                denomination
            )

        if denomination == TreasuryDenomination.ZAR:
            return SettlementAssetResolution(
                source_currency=source_currency,
                source_amount=source_amount,
                target_asset=SettlementAsset.ZAR,
                target_amount=source_amount,
                conversion_required=(
                    source_currency != "ZAR"
                ),
            )

        if denomination == TreasuryDenomination.WZAR:
            return SettlementAssetResolution(
                source_currency=source_currency,
                source_amount=source_amount,
                target_asset=SettlementAsset.WZAR,
                target_amount=None,
                conversion_required=True,
            )

        if denomination == TreasuryDenomination.SOL:
            return SettlementAssetResolution(
                source_currency=source_currency,
                source_amount=source_amount,
                target_asset=SettlementAsset.SOL,
                target_amount=(
                    source_amount
                    if source_currency == "SOL"
                    else None
                ),
                conversion_required=(
                    source_currency != "SOL"
                ),
            )

        raise ValueError(
            f"Unsupported treasury denomination: "
            f"{denomination}"
        )
