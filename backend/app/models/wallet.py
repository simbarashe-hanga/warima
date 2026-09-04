import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.enums import WalletStatus


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    member_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("member_accounts.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    currency = Column(
        String(3),
        nullable=False,
        default="ZAR",
    )

    balance = Column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    status = Column(
        Enum(WalletStatus),
        nullable=False,
        default=WalletStatus.ACTIVE,
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
        back_populates="wallet",
    )

    transactions = relationship(
        "WalletTransaction",
        back_populates="wallet",
        cascade="all, delete-orphan",
    )

    ledger_entries = relationship(
        "WalletLedger",
        back_populates="wallet",
        cascade="all, delete-orphan",
    )
