import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

from app.models.enums import (
    MembershipRole,
    MembershipStatus,
)



class Membership(Base):
    __tablename__ = "memberships"

    __table_args__ = (
        UniqueConstraint(
            "member_account_id",
            "stokvel_id",
            name="uq_membership_member_stokvel",
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    member_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("member_accounts.id"),
        nullable=False,
    )

    stokvel_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stokvels.id"),
        nullable=False,
    )

    role = Column(
        Enum(MembershipRole),
        nullable=False,
        default=MembershipRole.MEMBER,
    )

    status = Column(
        Enum(MembershipStatus),
        nullable=False,
        default=MembershipStatus.PENDING,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    member_account = relationship(
        "MemberAccount",
        back_populates="memberships",
    )

    stokvel = relationship(
        "Stokvel",
        back_populates="memberships",
    )
