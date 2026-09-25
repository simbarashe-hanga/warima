import uuid

from sqlalchemy import Column, DateTime, Enum, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.enums import (
    InvestmentAssetStatus,
    InvestmentAssetType,
)


class InvestmentAsset(Base):
    __tablename__ = "investment_assets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    symbol = Column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    name = Column(
        String(120),
        nullable=False,
    )

    asset_type = Column(
        Enum(InvestmentAssetType),
        nullable=False,
    )

    price = Column(
        Numeric(18, 2),
        nullable=False,
    )

    currency = Column(
        String(3),
        nullable=False,
        default="ZAR",
    )

    status = Column(
        Enum(InvestmentAssetStatus),
        nullable=False,
        default=InvestmentAssetStatus.ACTIVE,
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

    investments = relationship(
        "StokvelInvestment",
        back_populates="investment_asset",
        cascade="all, delete-orphan",
    )
