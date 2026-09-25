import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.enums import InvestmentOrderStatus


class InvestmentOrder(Base):
    __tablename__ = "investment_orders"

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

    wallet_transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wallet_transactions.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    quantity = Column(
        Numeric(18, 8),
        nullable=False,
    )

    unit_price = Column(
        Numeric(18, 2),
        nullable=False,
    )

    total_amount = Column(
        Numeric(18, 2),
        nullable=False,
    )

    currency = Column(
        String(3),
        nullable=False,
        default="ZAR",
    )

    status = Column(
        Enum(InvestmentOrderStatus),
        nullable=False,
        default=InvestmentOrderStatus.PENDING,
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
        back_populates="investment_orders",
    )

    investment_asset = relationship(
        "InvestmentAsset",
        back_populates="orders",
    )

    wallet_transaction = relationship(
        "WalletTransaction",
    )
