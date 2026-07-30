import uuid


from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    JSON,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_identity_id = Column(
        String,
        ForeignKey("user_identities.id"),
        nullable=False,
    )

    state = Column(
        String,
        nullable=True,
    )

    context = Column(
        JSON,
        nullable=True,
        default=dict,
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

    expires_at = Column(
        String,
        nullable=True,
    )

    user_identity = relationship(
        "UserIdentity",
        back_populates="session",
    )
