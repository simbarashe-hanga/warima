import secrets
import string

from sqlalchemy.orm import Session, joinedload

from app.models.stokvel import Stokvel
from app.models.membership import Membership
from app.models.member_account import MemberAccount
from app.models.enums import (
    StokvelStatus,
    MembershipRole,
    MembershipStatus,
)


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
        description: str | None = None,
    ) -> Stokvel:

        stokvel = Stokvel(
            name=name.strip(),
            join_code=self._generate_join_code(),
            description=description.strip() if description else None,
            status=StokvelStatus.PENDING,
        )

        self.db.add(stokvel)
        self.db.flush()

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
