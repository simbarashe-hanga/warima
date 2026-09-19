import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

from app.models.enums import (
    BlockchainAccountStatus,
    BlockchainAccountType,
    BlockchainChain,
)


class BlockchainAccount(Base):
    __tablename__ = "blockchain_accounts"

    __table_args__ = (
        UniqueConstraint(
            "member_account_id",
            "chain",
            "network",
            name="uq_blockchain_account_member_chain_network",
        ),
    )

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

    chain = Column(
        Enum(BlockchainChain),
        nullable=False,
    )

    network = Column(
        String(50),
        nullable=False,
    )

    address = Column(
        String(100),
        nullable=False,
        index=True,
    )

    account_type = Column(
        Enum(BlockchainAccountType),
        nullable=False,
        default=BlockchainAccountType.MANAGED,
    )

    status = Column(
        Enum(BlockchainAccountStatus),
        nullable=False,
        default=BlockchainAccountStatus.ACTIVE,
    )

    signer_reference = Column(
        String(100),
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
        back_populates="blockchain_accounts",
    )
