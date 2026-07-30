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

    user_id = Column(
        String,
        primary_key=True,
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

    last_seen = Column(
        String,
        nullable=True,
    )

    expires_at = Column(
        String,
        nullable=True,
    )
