import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    JSON,
    Numeric,
    String,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.enums import PaymentStatus

class Payment(Base):
    """
    Represents an external payment attempt used to fund
    a Warima member walle

    Payment represents the interaction with an external
    payment provider

    It does not directly modify wallet balances
    """

    __tablename__ = "payments"

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

    provider = Column(
        String(50),
        nullable=False,
        index=True,
    )

    provider_payment_id = Column(
        String(200),
        nullable=True,
        index=True,
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
        Enum(PaymentStatus),
        nullable=False,
        default=PaymentStatus.CREATED,
    )

    reference = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    payment_url = Column(
        String(500),
        nullable=True,
    )

    provider_metadata = Column(
        JSON,
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

    member_account = relationship(
        "MemberAccount",
        back_populates="payments",
    )
