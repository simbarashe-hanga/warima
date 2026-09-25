"""add payment table

Revision ID: 635f0d94968a
Revises: add_settlement_source
Create Date: 2026-09-23 11:58:00.988630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "635f0d94968a"
down_revision: Union[str, Sequence[str], None] = "add_settlement_source"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the provider-neutral payments table."""

    op.create_table(
        "payments",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("member_account_id", sa.UUID(), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column(
            "provider_payment_id",
            sa.String(length=200),
            nullable=True,
        ),
        sa.Column(
            "amount",
            sa.Numeric(precision=18, scale=2),
            nullable=False,
        ),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "CREATED",
                "PENDING",
                "SUCCEEDED",
                "FAILED",
                "CANCELLED",
                "REFUNDED",
                name="paymentstatus",
            ),
            nullable=False,
        ),
        sa.Column("reference", sa.String(length=100), nullable=False),
        sa.Column("payment_url", sa.String(length=500), nullable=True),
        sa.Column(
            "provider_metadata",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["member_account_id"],
            ["member_accounts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_payments_member_account_id",
        "payments",
        ["member_account_id"],
        unique=False,
    )

    op.create_index(
        "ix_payments_provider",
        "payments",
        ["provider"],
        unique=False,
    )

    op.create_index(
        "ix_payments_provider_payment_id",
        "payments",
        ["provider_payment_id"],
        unique=False,
    )

    op.create_index(
        "ix_payments_reference",
        "payments",
        ["reference"],
        unique=True,
    )


def downgrade() -> None:
    """Remove the payments table."""

    op.drop_index(
        "ix_payments_reference",
        table_name="payments",
    )

    op.drop_index(
        "ix_payments_provider_payment_id",
        table_name="payments",
    )

    op.drop_index(
        "ix_payments_provider",
        table_name="payments",
    )

    op.drop_index(
        "ix_payments_member_account_id",
        table_name="payments",
    )

    op.drop_table("payments")
