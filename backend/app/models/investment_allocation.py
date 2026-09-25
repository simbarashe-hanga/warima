import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class InvestmentAllocation(Base):

    __tablename__ = "investment_allocations"

    __table_args__ = (
        UniqueConstraint(
            "contribution_transaction_id",
            name="uq_investment_allocation_contribution_transaction",
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    investment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stokvel_investments.id"),
        nullable=False,
        index=True,
    )

    member_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("member_accounts.id"),
        nullable=False,
        index=True,
    )

    contribution_transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wallet_transactions.id"),
        nullable=False,
        index=True,
    )

    contributed_amount = Column(
        Numeric(18, 2),
        nullable=False,
    )

    participation_percentage = Column(
        Numeric(18, 8),
        nullable=False,
    )

    allocated_quantity = Column(
        Numeric(18, 8),
        nullable=False,
    )

    returned_amount = Column(
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

    investment = relationship(
        "StokvelInvestment",
        back_populates="allocations",
    )

    member_account = relationship(
        "MemberAccount",
        back_populates="investment_allocations",
    )

    contribution_transaction = relationship(
        "WalletTransaction",
    )
