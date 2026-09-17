from app.models.stokvel_treasury import StokvelTreasury
from app.models.enums import TreasuryRail

from app.services.settlement.settlement_handler import SettlementHandler
from app.services.settlement.solana_settlement_handler import (
    SolanaSettlementHandler,
)
from app.services.settlement.evm_settlement_handler import (
    EVMSettlementHandler,
)
from app.services.settlement.offchain_settlement_handler import (
    OffChainSettlementHandler,
)


class SettlementRouter:
    """
    Selects the settlement handler for a treasury.

    This router does not:
    - move money
    - execute settlements
    - call blockchain services
    - call payment providers
    - modify wallet balances
    - commit database transactions
    """

    @staticmethod
    def resolve_rail(
        treasury: StokvelTreasury,
    ) -> TreasuryRail:

        if treasury is None:
            raise ValueError(
                "Treasury is required"
            )

        if treasury.rail is None:
            raise ValueError(
                "Treasury settlement rail is not configured"
            )

        if isinstance(treasury.rail, str):
            return TreasuryRail(treasury.rail)

        return treasury.rail

    @staticmethod
    def resolve_handler(
        treasury: StokvelTreasury,
    ) -> SettlementHandler:

        rail = SettlementRouter.resolve_rail(
            treasury
        )

        if rail == TreasuryRail.SOLANA:
            return SolanaSettlementHandler()

        if rail == TreasuryRail.EVM:
            return EVMSettlementHandler()

        if rail == TreasuryRail.OFF_CHAIN:
            return OffChainSettlementHandler()

        raise ValueError(
            f"Unsupported settlement rail: {rail}"
        )
