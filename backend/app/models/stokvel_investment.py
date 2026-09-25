import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.enums import StokvelInvestmentStatus


class StokvelInvestment(Base):
    __tablename__ = "stokvel_investments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    stokvel_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stokvels.id"),
        nullable=False,
        index=True,
    )

    investment_asset_id = Column(
        UUID(as_uuid=True),
        ForeignKey("investment_assets.id"),
        nullable=False,
        index=True,
    )

    amount = Column(
        Numeric(18, 2),
        nullable=False,
    )

    quantity = Column(
        Numeric(18, 8),
        nullable=False,
    )

    unit_price = Column(
        Numeric(18, 2),
        nullable=False,
    )

    currency = Column(
        String(3),
        nullable=False,
        default="ZAR",
    )

    term_start = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    maturity_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    status = Column(
        Enum(StokvelInvestmentStatus),
        nullable=False,
        default=StokvelInvestmentStatus.PENDING,
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
        back_populates="investments",
    )

    investment_asset = relationship(
        "InvestmentAsset",
        back_populates="investments",
    )

    allocations = relationship(
        "InvestmentAllocation",
        back_populates="investment",
        cascade="all, delete-orphan",
    )

    treasury_ledger_entries = relationship(
        "TreasuryLedger",
        back_populates="investment",
    )
