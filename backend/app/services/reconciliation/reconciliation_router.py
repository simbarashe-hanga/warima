from app.models.enums import TreasuryRail
from app.models.stokvel_treasury import StokvelTreasury

from app.services.reconciliation.reconciliation_handler import (
    ReconciliationHandler,
)


class ReconciliationRouter:
    """
    Selects the reconciliation handler for a treasury rail.

    This router does not:
    - execute settlements
    - query external networks
    - modify settlement state
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
                "Treasury reconciliation rail is not configured"
            )

        if isinstance(treasury.rail, str):
            return TreasuryRail(treasury.rail)

        return treasury.rail

    @staticmethod
    def resolve_handler(
        treasury: StokvelTreasury,
    ) -> ReconciliationHandler:

        rail = ReconciliationRouter.resolve_rail(
            treasury
        )

        if rail == TreasuryRail.SOLANA:
            raise NotImplementedError(
                "Solana reconciliation handler is not implemented yet"
            )

        if rail == TreasuryRail.EVM:
            raise NotImplementedError(
                "EVM reconciliation handler is not implemented yet"
            )

        if rail == TreasuryRail.OFF_CHAIN:
            raise NotImplementedError(
                "Off-chain reconciliation handler is not implemented yet"
            )

        raise ValueError(
            f"Unsupported reconciliation rail: {rail}"
        )
