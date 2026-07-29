import uuid


from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.enums import SessionState


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_identity_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_identities.id"),
        nullable=False,
    )

    state = Column(
        Enum(SessionState),
        nullable=False,
        default=SessionState.START,
    )

    context = Column(
        JSON,
        nullable=False,
        default=dict,
    )

    expires_at = Column(DateTime(timezone=True))

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

    identity = relationship(
        "UserIdentity",
        back_populates="session",
    )
