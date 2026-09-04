import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import  relationship
from sqlalchemy.sql import func

from app.db.base import Base

from app.models.enums import (
    MemberAccountStatus,
    MemberAccountType,
)


class MemberAccount(Base):
    __tablename__ = "member_accounts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    account_number = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    display_name = Column(
        String(120),
        nullable=True,
    )

    account_type = Column(
        Enum(MemberAccountType),
        nullable=False,
        default=MemberAccountType.PERSONAL,
    )

    status = Column(
        Enum(MemberAccountStatus),
        nullable=False,
        default=MemberAccountStatus.PENDING,
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

    #
    # Relationships
    #

    user = relationship(
        "User",
        back_populates="member_accounts",
    )

    memberships = relationship(
        "Membership",
        back_populates="member_account",
        cascade="all, delete-orphan",
    )

    wallet = relationship(
        "Wallet",
        back_populates="member_account",
        uselist=False,
        cascade="all, delete-orphan",
    )
