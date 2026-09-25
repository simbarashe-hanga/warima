import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class InvestmentHolding(Base):
    __tablename__ = "investment_holdings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    member_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("member_accounts.id"),
        nullable=False,
        index=True,
    )

    investment_asset_id = Column(
        UUID(as_uuid=True),
        ForeignKey("investment_assets.id"),
        nullable=False,
        index=True,
    )

    quantity = Column(
        Numeric(18, 8),
        nullable=False,
        default=0,
    )

    average_price = Column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    total_cost = Column(
        Numeric(18, 2),
        nullable=False,
        default=0,
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

    member_account = relationship(
        "MemberAccount",
        back_populates="investment_holdings",
    )

    investment_asset = relationship(
        "InvestmentAsset",
        back_populates="holdings",
    )
