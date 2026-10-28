import secrets
import string

from sqlalchemy.orm import Session, joinedload

from app.models.stokvel import Stokvel
from app.models.membership import Membership
from app.models.member_account import MemberAccount
from app.models.enums import (
    StokvelStatus,
    StokvelType,
    MembershipRole,
    MembershipStatus,
    TreasuryDenomination,
    TreasuryRail,
    TreasuryStrategy,
    TreasuryReturnSource,
)

from app.services.treasury.treasury_service import TreasuryService

from app.models.wallet_transaction import WalletTransaction


class StokvelService:
    """
    Business operations for stokvels.

    Responsibilities:
    - Create stokvels
    - Generate unique join codes
    - Activate stokvels
    - Add members
    - Retrieve stokvels
    - Retrieve memberships

    Transaction ownership remains with the caller.
    This service uses flush() rather than commit().
    """

    JOIN_CODE_ALPHABET = string.ascii_uppercase + string.digits
    JOIN_CODE_LENGTH = 6

    def __init__(self, db: Session):
        self.db = db

    def _require_owner(
        self,
        member_account_id,
        stokvel_id,
    ) -> Membership:
        """
        Require an active owner membership for a stokvel.
        """

        membership = (
            self.db.query(Membership)
            .filter(
                Membership.member_account_id == member_account_id,
                Membership.stokvel_id == stokvel_id,
                Membership.status == MembershipStatus.ACTIVE,
                Membership.role == MembershipRole.OWNER,
            )
            .first()
        )

        if not membership:
            raise ValueError(
                "Only the stokvel owner can perform this action."
            )

        return membership

    def _generate_join_code(self) -> str:
        """
        Generate a unique human-friendly join code.
        """

        while True:
            code = "".join(
                secrets.choice(self.JOIN_CODE_ALPHABET)
                for _ in range(self.JOIN_CODE_LENGTH)
            )

            existing = (
                self.db.query(Stokvel)
                .filter(Stokvel.join_code == code)
                .first()
            )

            if not existing:
                return code

    def create_stokvel(
        self,
        name: str,
        stokvel_type: StokvelType = StokvelType.SAVINGS,
        description: str | None = None,
    ) -> Stokvel:
        """
        Create a stokvel together with its treasury configuration.

        The user-facing StokvelType determines the underlying
        treasury configuration. Callers should not need to know
        about denominations, rails, networks, or strategies.

        Treasury creation happens in the same database transaction
        as stokvel creation. The caller owns commit/rollback.
        """

        if not name or not name.strip():
            raise ValueError("Stokvel name is required")

        treasury_config = {
            StokvelType.SAVINGS: {
                "denomination": TreasuryDenomination.ZAR,
                "rail": TreasuryRail.OFF_CHAIN,
                "network": None,
                "strategy": TreasuryStrategy.CASH,
                "return_source": TreasuryReturnSource.CASH_RETURNS,
            },
            StokvelType.AGRICULTURE: {
                "denomination": TreasuryDenomination.WZAR,
                "rail": TreasuryRail.EVM,
                "network": "base-sepolia",
                "strategy": TreasuryStrategy.AGRICULTURE,
                "return_source": TreasuryReturnSource.MEAT_SALES,
            },
            StokvelType.DIGITAL_ASSET: {
                "denomination": TreasuryDenomination.SOL,
                "rail": TreasuryRail.SOLANA,
                "network": "devnet",
                "strategy": TreasuryStrategy.ON_CHAIN,
                "return_source": TreasuryReturnSource.ON_CHAIN,
            },
        }

        config = treasury_config.get(stokvel_type)

        if config is None:
            raise ValueError(
                f"Unsupported stokvel type: {stokvel_type}"
            )

        stokvel = Stokvel(
            name=name.strip(),
            join_code=self._generate_join_code(),
            description=description.strip() if description else None,
            stokvel_type=stokvel_type,
            status=StokvelStatus.PENDING,
        )

        self.db.add(stokvel)
        self.db.flush()

        TreasuryService.create_treasury(
            db=self.db,
            stokvel=stokvel,
            **config,
        )

        return stokvel


    def get_stokvel(
        self,
        stokvel_id,
    ) -> Stokvel | None:

        return (
            self.db.query(Stokvel)
            .filter(Stokvel.id == stokvel_id)
            .first()
        )

    def get_stokvel_by_join_code(
        self,
        join_code: str,
    ) -> Stokvel | None:

        code = join_code.strip().upper()

        return (
            self.db.query(Stokvel)
            .filter(Stokvel.join_code == code)
            .first()
        )

    def activate_stokvel(
        self,
        stokvel_id,
    ) -> Stokvel | None:

        stokvel = self.get_stokvel(stokvel_id)

        if not stokvel:
            return None

        stokvel.status = StokvelStatus.ACTIVE
        self.db.flush()

        return stokvel

    def delete_stokvel(
        self,
        member_account_id,
        stokvel_id,
    ) -> bool:
        """
        Permanent delete stokvel when it has no financial history

        A stokvel with any wallet transaction must never be
        physically deleted. Such a stokvel should be closed instead.

        Transaction ownership remains with the caller.
        """

        stokvel = self.get_stokvel(stokvel_id)

        if not stokvel:
            return False

        self._require_owner(
            member_account_id,
            stokvel_id,
        )

        financial_activity = (
            self.db.query(WalletTransaction.id)
            .filter(
                WalletTransaction.stokvel_id == stokvel_id
            )
            .first()
        )

        if financial_activity:
            raise ValueError(
                "Stokvel cannot be deleted because it has financial history. "
                "Close the stokvel instead"
            )

        self.db.delete(stokvel)
        self.db.flush()

        return True

    def suspend_stokvel(
        self,
        member_account_id,
        stokvel_id,
    ) -> Stokvel | None:
        """
        Suspend an active stokvel

        Transaction ownership remains with the caller
        """

        stokvel = self.get_stokvel(stokvel_id)

        self._require_owner(
            member_account_id,
            stokvel_id,
        )

        if not stokvel:
            return None

        if stokvel.status != StokvelStatus.ACTIVE:
            raise ValueError(
                "Only an active stokvel can be suspended."
            )

        stokvel.status = StokvelStatus.SUSPENDED
        self.db.flush()

        return stokvel

    def resume_stokvel(
        self,
        member_account_id,
        stokvel_id,
    ) -> Stokvel | None:
        """
        Resume a suspended stokvel.

        Transaction onwership remains with the caller
        """

        stokvel = self.get_stokvel(stokvel_id)

        self._require_owner(
            member_account_id,
            stokvel_id,
        )

        if not stokvel:
            return None

        if stokvel.status != StokvelStatus.SUSPENDED:
            raise ValueError(
                "Only a suspended stokvel can be resumed."
            )

        stokvel.status = StokvelStatus.ACTIVE
        self.db.flush()

        return stokvel

    def close_stokvel(
        self,
        member_account_id,
        stokvel_id,
    ) -> Stokvel | None:
        """
        Permanently close a stokvel while preserving its history.

        A closed stokvel cannot be reopened through this method
        """

        stokvel = self.get_stokvel(stokvel_id)

        self._require_owner(
            member_account_id,
            stokvel_id,
        )

        if not stokvel:
            return None

        if stokvel.status not in (
            StokvelStatus.ACTIVE,
            StokvelStatus.SUSPENDED,
        ):
            raise ValueError(
                "Only an active or suspended stokvel can be closed."
            )

        stokvel.status = StokvelStatus.CLOSED
        self.db.flush()

        return stokvel

    def add_member(
        self,
        member_account_id,
        stokvel_id,
        role: MembershipRole = MembershipRole.MEMBER,
    ) -> Membership:

        existing = (
            self.db.query(Membership)
            .filter(
                Membership.member_account_id == member_account_id,
                Membership.stokvel_id == stokvel_id,
            )
            .first()
        )

        if existing:
            return existing

        membership = Membership(
            member_account_id=member_account_id,
            stokvel_id=stokvel_id,
            role=role,
            status=MembershipStatus.ACTIVE,
        )

        self.db.add(membership)
        self.db.flush()

        return membership

    def get_member_stokvels(
        self,
        member_account_id,
    ) -> list[Stokvel]:

        return (
            self.db.query(Stokvel)
            .join(
                Membership,
                Membership.stokvel_id == Stokvel.id,
            )
            .filter(
                Membership.member_account_id == member_account_id,
                Membership.status == MembershipStatus.ACTIVE,
            )
            .all()
        )

    def get_membership(
        self,
        member_account_id,
        stokvel_id,
    ) -> Membership | None:

        return (
            self.db.query(Membership)
            .filter(
                Membership.member_account_id == member_account_id,
                Membership.stokvel_id == stokvel_id,
                Membership.status == MembershipStatus.ACTIVE,
            )
            .first()
        )

    def get_stokvel_members(self, stokvel_id) -> list[Membership]:
        """
        Return active memberships for a stokvel with member account
        and user information eagerly loaded.
        """
        return (
            self.db.query(Membership)
            .options(
                joinedload(Membership.member_account)
                .joinedload(MemberAccount.user)
            )
            .filter(
                Membership.stokvel_id == stokvel_id,
                Membership.status == MembershipStatus.ACTIVE,
            )
            .all()
        )
