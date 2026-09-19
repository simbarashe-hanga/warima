import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.enums import WalletLedgerEntryType


class TreasuryLedger(Base):
    __tablename__ = "treasury_ledger"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    treasury_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stokvel_treasuries.id"),
        nullable=False,
        index=True,
    )

    transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wallet_transactions.id"),
        nullable=False,
        index=True,
    )

    entry_type = Column(
        Enum(WalletLedgerEntryType),
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

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    treasury = relationship(
        "StokvelTreasury",
        back_populates="ledger_entries",
    )

    transaction = relationship(
        "WalletTransaction",
        back_populates="treasury_ledger_entries",
    )
