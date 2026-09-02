import uuid

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Pig(Base):
    __tablename__ = "pigs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    token_id = Column(
        Integer,
        unique=True,
        nullable=False,
    )

    breed = Column(
        String,
        nullable=False,
    )

    birth_date = Column(
        DateTime,
        nullable=False,
    )

    purchase_date = Column(
        DateTime,
        nullable=False,
    )

    farm_location = Column(
        String,
        nullable=False,
    )

    health_status = Column(
        String,
        nullable=False,
        default="Healthy",
    )

    current_owner = Column(
        String,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    metadata_uri = Column(
        String,
        nullable=True,
    )

    blockchain_data = Column(
        JSON,
        nullable=True,
        default=dict,
    )

    last_synced = Column(
        DateTime,
        nullable=True,
    )

    health_events = relationship(
        "HealthEvent",
        back_populates="pig",
        cascade="all, delete-orphan",
    )


class HealthEvent(Base):
    __tablename__ = "health_events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    pig_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pigs.id"),
        nullable=False,
    )

    event_type = Column(
        String,
        nullable=False,
    )

    description = Column(
        String,
        nullable=True,
    )

    performed_by = Column(
        String,
        nullable=True,
    )

    cost = Column(
        Float,
        nullable=True,
        default=0,
    )

    document_hash = Column(
        String,
        nullable=True,
    )

    transaction_hash = Column(
        String,
        nullable=True,
    )

    block_number = Column(
        Integer,
        nullable=True,
    )

    timestamp = Column(
        DateTime,
        nullable=False,
    )

    pig = relationship(
        "Pig",
        back_populates="health_events",
    )
