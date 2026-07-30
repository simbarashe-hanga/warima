import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Index,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.enums import IdentityProvider


class UserIdentity(Base):
    __tablename__ = "user_identities"

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_identifier",
            name="uq_provider_identifier",
        ),
        Index(
            "ix_provider_identifier",
            "provider",
            "provider_identifier",
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
    )

    provider = Column(
        Enum(IdentityProvider),
        nullable=False,
    )

    provider_identifier = Column(
        String,
        nullable=False,
    )

    verified = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="identities",
    )

    session = relationship(
        "UserSession",
        back_populates="identity",
        uselist=False,
        cascade="all, delete-orphan",
    )
