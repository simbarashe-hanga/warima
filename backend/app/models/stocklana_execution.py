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

from app.models.enums import SettlementStatus


class StocklanaExecution(Base):
    """
    Records the blockchain execution associated with a
    Stocklana collective investment.

    StokvelInvestment remains the financial/business record.

    StocklanaExecution records the external blockchain
    execution/proof associated with that investment.
    """

    __tablename__ = "stocklana_executions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    investment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stokvel_investments.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    amount_sol = Column(
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

    investment = relationship(
        "StokvelInvestment",
        back_populates="stocklana_execution",
    )
