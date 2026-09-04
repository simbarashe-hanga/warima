import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    String,
    Text,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

from app.models.enums import StokvelStatus


class Stokvel(Base):
    __tablename__="stokvels"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name = Column(
        String(120),
        nullable=False,
    )

    join_code = Column(
        String(12),
        nullable=False,
        unique=True,
        index=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    status = Column(
        Enum(StokvelStatus),
        nullable=False,
        default=StokvelStatus.PENDING,
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

    memberships = relationship(
        "Membership",
        back_populates="stokvel",
        cascade="all, delete-orphan",
    )
    
