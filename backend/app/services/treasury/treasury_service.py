import uuid

from sqlalchemy.orm import Session

from app.models.stokvel import Stokvel
from app.models.stokvel_treasury import StokvelTreasury
from app.models.enums import (
    TreasuryDenomination,
    TreasuryRail,
    TreasuryStrategy,
    TreasuryReturnSource,
)


class TreasuryService:
    """
    Manages Stokvel treasury configuration.

    This service owns treasury persistence and validation.

    It does not:
    - commit database transactions
    - perform blockchain operations
    - move money
    - execute payment settlements

    The caller owns the database transaction.
    """

    @staticmethod
    def validate_configuration(
        denomination,
        rail,
        network,
        strategy,
        return_source,
    ):
        """
        Validate that the treasury configuration is internally consistent.
        """

        if isinstance(denomination, str):
            denomination = TreasuryDenomination(denomination)

        if isinstance(rail, str):
            rail = TreasuryRail(rail)

        if isinstance(strategy, str):
            strategy = TreasuryStrategy(strategy)

        if isinstance(return_source, str):
            return_source = TreasuryReturnSource(return_source)

        # --------------------------------------------------------
        # Solana / SOL
        # --------------------------------------------------------

        if denomination == TreasuryDenomination.SOL:

            if rail != TreasuryRail.SOLANA:
                raise ValueError(
                    "SOL treasury must use the SOLANA rail"
                )

            if not network:
                raise ValueError(
                    "SOL treasury requires a network"
                )

        # --------------------------------------------------------
        # WZAR / EVM
        # --------------------------------------------------------

        elif denomination == TreasuryDenomination.WZAR:

            if rail != TreasuryRail.EVM:
                raise ValueError(
                    "WZAR treasury must use the EVM rail"
                )

            if not network:
                raise ValueError(
                    "WZAR treasury requires a network"
                )

        # --------------------------------------------------------
        # ZAR / Off-chain
        # --------------------------------------------------------

        elif denomination == TreasuryDenomination.ZAR:

            if rail != TreasuryRail.OFF_CHAIN:
                raise ValueError(
                    "ZAR treasury must use the OFF_CHAIN rail"
                )

            if network is not None:
                raise ValueError(
                    "OFF_CHAIN treasury must not have a network"
                )

        # --------------------------------------------------------
        # Strategy / return source validation
        # --------------------------------------------------------

        if strategy == TreasuryStrategy.ON_CHAIN:

            if return_source != TreasuryReturnSource.ON_CHAIN:
                raise ValueError(
                    "ON_CHAIN strategy must use ON_CHAIN return source"
                )

        elif strategy == TreasuryStrategy.AGRICULTURE:

            if return_source != TreasuryReturnSource.MEAT_SALES:
                raise ValueError(
                    "AGRICULTURE strategy must use MEAT_SALES return source"
                )

        elif strategy == TreasuryStrategy.CASH:

            if return_source != TreasuryReturnSource.CASH_RETURNS:
                raise ValueError(
                    "CASH strategy must use CASH_RETURNS return source"
                )

        return True

    @staticmethod
    def create_treasury(
        db: Session,
        stokvel: Stokvel,
        denomination,
        rail,
        network,
        strategy,
        return_source,
    ) -> StokvelTreasury:

        if stokvel is None:
            raise ValueError("Stokvel is required")

        existing = (
            db.query(StokvelTreasury)
            .filter(
                StokvelTreasury.stokvel_id == stokvel.id
            )
            .first()
        )

        if existing:
            raise ValueError(
                "Stokvel already has a treasury"
            )

        TreasuryService.validate_configuration(
            denomination=denomination,
            rail=rail,
            network=network,
            strategy=strategy,
            return_source=return_source,
        )

        treasury = StokvelTreasury(
            id=uuid.uuid4(),
            stokvel_id=stokvel.id,
            denomination=(
                TreasuryDenomination(denomination)
                if isinstance(denomination, str)
                else denomination
            ),
            rail=(
                TreasuryRail(rail)
                if isinstance(rail, str)
                else rail
            ),
            network=network,
            strategy=(
                TreasuryStrategy(strategy)
                if isinstance(strategy, str)
                else strategy
            ),
            return_source=(
                TreasuryReturnSource(return_source)
                if isinstance(return_source, str)
                else return_source
            ),
        )

        db.add(treasury)
        db.flush()

        return treasury

    @staticmethod
    def get_treasury(
        db: Session,
        treasury_id,
    ) -> StokvelTreasury | None:

        return (
            db.query(StokvelTreasury)
            .filter(
                StokvelTreasury.id == treasury_id
            )
            .first()
        )

    @staticmethod
    def get_treasury_by_stokvel(
        db: Session,
        stokvel_id,
    ) -> StokvelTreasury | None:

        return (
            db.query(StokvelTreasury)
            .filter(
                StokvelTreasury.stokvel_id == stokvel_id
            )
            .first()
        )

    @staticmethod
    def update_treasury(
        db: Session,
        treasury: StokvelTreasury,
        denomination=None,
        rail=None,
        network=None,
        strategy=None,
        return_source=None,
    ) -> StokvelTreasury:

        if treasury is None:
            raise ValueError("Treasury is required")

        new_denomination = (
            denomination
            if denomination is not None
            else treasury.denomination
        )

        new_rail = (
            rail
            if rail is not None
            else treasury.rail
        )

        new_network = (
            network
            if network is not None
            else treasury.network
        )

        new_strategy = (
            strategy
            if strategy is not None
            else treasury.strategy
        )

        new_return_source = (
            return_source
            if return_source is not None
            else treasury.return_source
        )

        TreasuryService.validate_configuration(
            denomination=new_denomination,
            rail=new_rail,
            network=new_network,
            strategy=new_strategy,
            return_source=new_return_source,
        )

        treasury.denomination = (
            TreasuryDenomination(new_denomination)
            if isinstance(new_denomination, str)
            else new_denomination
        )

        treasury.rail = (
            TreasuryRail(new_rail)
            if isinstance(new_rail, str)
            else new_rail
        )

        treasury.network = new_network

        treasury.strategy = (
            TreasuryStrategy(new_strategy)
            if isinstance(new_strategy, str)
            else new_strategy
        )

        treasury.return_source = (
            TreasuryReturnSource(new_return_source)
            if isinstance(new_return_source, str)
            else new_return_source
        )

        db.flush()

        return treasury
