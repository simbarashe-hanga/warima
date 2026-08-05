from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String, DateTime, Enum
from app.models.enums import UserStatus
from app.db.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    first_name = Column(String, nullable=True)

    last_name = Column(String, nullable=True)

    display_name = Column(String, nullable=True)

    email = Column(
        String,
        unique=True,
        nullable=True,
    )

    language = Column(String, nullable=True)

    status = Column(
        String,
        nullable=True,
    )

    pin_hash = Column(String, nullable=True)

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

    identities = relationship(
        "UserIdentity",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    member_accounts = relationship(
        "MemberAccount",
        back_populates="user",
        cascade="all, delete-orphan",
    )

