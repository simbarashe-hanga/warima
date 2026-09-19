import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

from app.models.enums import (
    SettlementAsset,
    SettlementStatus,
)


class Settlement(Base):
    """
    Represents the settlement of a financial transaction
    through an external settlement rail such as Solana.

    WalletTransaction remains the source financial record.

    Settlement records how that financial obligation
    was actually settled.
    """

    __tablename__ = "settlements"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    wallet_transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wallet_transactions.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    asset = Column(
        Enum(SettlementAsset),
        nullable=False,
    )

    amount = Column(
        Numeric(36, 18),
        nullable=False,
    )

    destination = Column(
        String(100),
        nullable=False,
    )

    source = Column(
        String(100),
        nullable=True,
    )

    network = Column(
        String(50),
        nullable=False,
    )

    status = Column(
        Enum(SettlementStatus),
        nullable=False,
        default=SettlementStatus.PENDING,
    )

    transaction_signature = Column(
        String(200),
        nullable=True,
        unique=True,
    )

    error_message = Column(
        String(500),
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

    wallet_transaction = relationship(
        "WalletTransaction",
        back_populates="settlement",
    )
