"""add investment models

Revision ID: 4788b17dff81
Revises: 635f0d94968a
Create Date: 2026-09-25

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "4788b17dff81"
down_revision: Union[str, Sequence[str], None] = "635f0d94968a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create investment assets, orders, and holdings."""

    # Extend the existing wallet transaction enum.
    # This is intentionally done with ALTER TYPE rather than recreating
    # the existing PostgreSQL enum.
    op.execute(
        "ALTER TYPE wallettransactiontype "
        "ADD VALUE IF NOT EXISTS 'INVESTMENT'"
    )

    investment_asset_type = postgresql.ENUM(
        "TOKENIZED_STOCK",
        name="investmentassettype",
        create_type=False,
    )

    investment_asset_status = postgresql.ENUM(
        "ACTIVE",
        "INACTIVE",
        name="investmentassetstatus",
        create_type=False,
    )

    investment_order_status = postgresql.ENUM(
        "PENDING",
        "PROCESSING",
        "COMPLETED",
        "FAILED",
        "CANCELLED",
        name="investmentorderstatus",
        create_type=False,
    )

    investment_asset_type.create(op.get_bind(), checkfirst=True)
    investment_asset_status.create(op.get_bind(), checkfirst=True)
    investment_order_status.create(op.get_bind(), checkfirst=True)

    # Investment assets
    op.create_table(
        "investment_assets",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "symbol",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=120),
            nullable=False,
        ),
        sa.Column(
            "asset_type",
            investment_asset_type,
            nullable=False,
        ),
        sa.Column(
            "price",
            sa.Numeric(precision=18, scale=2),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            server_default="ZAR",
            nullable=False,
        ),
        sa.Column(
            "status",
            investment_asset_status,
            nullable=False,
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
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_investment_assets_symbol",
        "investment_assets",
        ["symbol"],
        unique=True,
    )

    # Investment orders
    op.create_table(
        "investment_orders",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "member_account_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "investment_asset_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "wallet_transaction_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "quantity",
            sa.Numeric(precision=18, scale=8),
            nullable=False,
        ),
        sa.Column(
            "unit_price",
            sa.Numeric(precision=18, scale=2),
            nullable=False,
        ),
        sa.Column(
            "total_amount",
            sa.Numeric(precision=18, scale=2),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "status",
            investment_order_status,
            nullable=False,
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
        sa.ForeignKeyConstraint(
            ["investment_asset_id"],
            ["investment_assets.id"],
        ),
        sa.ForeignKeyConstraint(
            ["wallet_transaction_id"],
            ["wallet_transactions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_investment_orders_member_account_id",
        "investment_orders",
        ["member_account_id"],
        unique=False,
    )

    op.create_index(
        "ix_investment_orders_investment_asset_id",
        "investment_orders",
        ["investment_asset_id"],
        unique=False,
    )

    op.create_index(
        "ix_investment_orders_wallet_transaction_id",
        "investment_orders",
        ["wallet_transaction_id"],
        unique=True,
    )

    # Investment holdings
    op.create_table(
        "investment_holdings",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "member_account_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "investment_asset_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "quantity",
            sa.Numeric(precision=18, scale=8),
            server_default="0",
            nullable=False,
        ),
        sa.Column(
            "average_price",
            sa.Numeric(precision=18, scale=2),
            server_default="0",
            nullable=False,
        ),
        sa.Column(
            "total_cost",
            sa.Numeric(precision=18, scale=2),
            server_default="0",
            nullable=False,
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
        sa.ForeignKeyConstraint(
            ["investment_asset_id"],
            ["investment_assets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_investment_holdings_member_account_id",
        "investment_holdings",
        ["member_account_id"],
        unique=False,
    )

    op.create_index(
        "ix_investment_holdings_investment_asset_id",
        "investment_holdings",
        ["investment_asset_id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove investment tables and investment-specific enum types."""

    op.drop_index(
        "ix_investment_holdings_investment_asset_id",
        table_name="investment_holdings",
    )

    op.drop_index(
        "ix_investment_holdings_member_account_id",
        table_name="investment_holdings",
    )

    op.drop_table("investment_holdings")

    op.drop_index(
        "ix_investment_orders_wallet_transaction_id",
        table_name="investment_orders",
    )

    op.drop_index(
        "ix_investment_orders_investment_asset_id",
        table_name="investment_orders",
    )

    op.drop_index(
        "ix_investment_orders_member_account_id",
        table_name="investment_orders",
    )

    op.drop_table("investment_orders")

    op.drop_index(
        "ix_investment_assets_symbol",
        table_name="investment_assets",
    )

    op.drop_table("investment_assets")

    op.execute("DROP TYPE IF EXISTS investmentorderstatus")
    op.execute("DROP TYPE IF EXISTS investmentassetstatus")
    op.execute("DROP TYPE IF EXISTS investmentassettype")

    # We intentionally do not remove INVESTMENT from
    # wallettransactiontype because PostgreSQL does not support
    # safely removing an individual enum value.
