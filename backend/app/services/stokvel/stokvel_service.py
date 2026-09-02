import uuid

from app.models.stokvel import Stokvel
from app.models.membership import Membership
from app.models.enums import (
    StokvelStatus,
    MembershipRole,
    MembershipStatus,
)


class StokvelService:
    """
    Business operations for stokvels

    This service manages:
    - stokvel creation
    - membership
    - membership lookup
    - stokvel retrieval

    Financial operations should remain in the wallet/ledger layer
    """

    def __init__(self, db: Session):
        self.db = db

    #-------------------------------------------------------------------
    # Create
    #-------------------------------------------------------------------

    def create_stokvel(
        self,
        name: str,
        description: str | None = None,
    ) -> Stokvel:

        stokvel = Stokvel(
            id=uuid.uuid4(),
            name=name,
            description=description,
            status=StokvelStatus.PENDING,
        )

        self.db.add(stokvel)
        self.db.commit()
        self.db.refresh(stokvel)

        return stokvel

    #-----------------------------------------------------------------------
    # Get
    #-----------------------------------------------------------------------

    def get_stokvel(
        self,
        stokvel_id,
    ) -> Stokvel | None:

        return (
            self.db.query(Stokvel)
            .filter(Stokvel.id == stokvel_id)
            .first()
        )

    #------------------------------------------------------------------------
    # Activate
    #------------------------------------------------------------------------

    def activate_stokvel(
        self,
        stokvel_id,
    ) -> Stokvel | None:

        stokvel = self.get_stokvel(stokvel_id)

        if not stokvel:
            return None

        stokvel.status = StokvelStatus.ACTIVE

        self.db.commit()
        self.db.refresh(stokvel)

        return stokvel

    #-------------------------------------------------------------------------
    # Add member
    #-------------------------------------------------------------------------

    def add_member(
        self,
        member_Account_id,
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
            id=uuid.uuid4(),
            memberaccount_id=member_account_id,
            stokvel_id=stokvel_id,
            role=role,
            status=MembershipStatus.ACTIVE,
        )

        self.db.add(membership)
        self.db.commit()
        self.db.refresh(membership)

        return membership

    #---------------------------------------------------------------------------
    # Get member's stokvels
    #---------------------------------------------------------------------------

    def get_member_stokvels(
        self,
        member_Account_id,
    ) -> list[Stokvel]:

        return (
            self.db.query(Stokvel)
            .join(
                Membership,
                Membership.stokvel_id == Stokvel.id,
            )
            .filter(
                Membership.member_account_id == member_account_id,
                Membershipt.status == MembershipStatus.ACTIVE,
            )
            .all()
        )

    #-----------------------------------------------------------------------------
    # Get membership
    #-----------------------------------------------------------------------------

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
