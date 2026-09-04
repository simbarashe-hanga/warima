import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.enums import (
    WalletTransactionStatus,
    WalletTransactionType,
)


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    wallet_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wallets.id"),
        nullable=False,
        index=True,
    )

    stokvel_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stokvels.id"),
        nullable=True,
        index=True,
    )

    transaction_type = Column(
        Enum(WalletTransactionType),
        nullable=False,
    )

    amount = Column(
        Numeric(18, 2),
        nullable=False,
    )

    currency = Column(
        String(3),
        nullable=False,
        default="ZAR",
    )

    status = Column(
        Enum(WalletTransactionStatus),
        nullable=False,
        default=WalletTransactionStatus.PENDING,
    )

    reference = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    description = Column(
        Text,
        nullable=True,
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

    wallet = relationship(
        "Wallet",
        back_populates="transactions",
    )

    stokvel = relationship("Stokvel")

    ledger_entries = relationship(
        "WalletLedger",
        back_populates="transaction",
    )
