import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

from app.models.enums import (
    TreasuryDenomination,
    TreasuryRail,
    TreasuryStrategy,
    TreasuryReturnSource,
)


class StokvelTreasury(Base):
    __tablename__ = "stokvel_treasuries"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    stokvel_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stokvels.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    denomination = Column(
        Enum(TreasuryDenomination),
        nullable=False,
    )

    rail = Column(
        Enum(TreasuryRail),
        nullable=False,
    )

    network = Column(
        String(50),
        nullable=True,
    )

    blockchain_address = Column(
        String(100),
        nullable=True,
    )

    strategy = Column(
        Enum(TreasuryStrategy),
        nullable=False,
    )

    return_source = Column(
        Enum(TreasuryReturnSource),
        nullable=False,
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

    stokvel = relationship(
        "Stokvel",
        back_populates="treasury",
    )
