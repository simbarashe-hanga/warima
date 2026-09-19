"""add treasury ledger

Revision ID: 0f684ce2b2ce
Revises: 905a950944c5
Create Date: 2026-09-19 16:08:30.658687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "0f684ce2b2ce"
down_revision: Union[str, Sequence[str], None] = "905a950944c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    entry_type_enum = postgresql.ENUM(
        "CREDIT",
        "DEBIT",
        name="walletledgerentrytype",
        create_type=False,
    )

    op.create_table(
        "treasury_ledger",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "treasury_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "transaction_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "entry_type",
            entry_type_enum,
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.Numeric(18, 2),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["transaction_id"],
            ["wallet_transactions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["treasury_id"],
            ["stokvel_treasuries.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_treasury_ledger_treasury_id"),
        "treasury_ledger",
        ["treasury_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_treasury_ledger_transaction_id"),
        "treasury_ledger",
        ["transaction_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_treasury_ledger_transaction_id"),
        table_name="treasury_ledger",
    )

    op.drop_index(
        op.f("ix_treasury_ledger_treasury_id"),
        table_name="treasury_ledger",
    )

    op.drop_table("treasury_ledger")
