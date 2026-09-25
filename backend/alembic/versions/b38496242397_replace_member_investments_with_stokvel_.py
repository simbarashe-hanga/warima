"""replace member investments with stokvel investments

Revision ID: b38496242397
Revises: 4788b17dff81
Create Date: 2026-09-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "b38496242397"
down_revision: Union[str, Sequence[str], None] = "4788b17dff81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Replace member-level investments with stokvel-level investments."""

    # ------------------------------------------------------------
    # 1. Remove the old member-level investment tables.
    #
    # These tables are empty in the current database.
    # investment_assets is intentionally preserved.
    # ------------------------------------------------------------

    op.drop_table("investment_holdings")
    op.drop_table("investment_orders")

    # ------------------------------------------------------------
    # 2. Create the new stokvel investment status enum.
    # ------------------------------------------------------------

    stokvel_investment_status = postgresql.ENUM(
        "PENDING",
        "ACTIVE",
        "MATURED",
        "COMPLETED",
        "FAILED",
        "CANCELLED",
        name="stokvelinvestmentstatus",
        create_type=False,
    )

    stokvel_investment_status.create(
        op.get_bind(),
        checkfirst=True,
    )

    # ------------------------------------------------------------
    # 3. Create stokvel_investments.
    #
    # One row represents one collective investment made by a
    # stokvel treasury.
    # ------------------------------------------------------------

    op.create_table(
        "stokvel_investments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "stokvel_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "investment_asset_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.Numeric(precision=18, scale=2),
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
            "currency",
            sa.String(length=3),
            server_default="ZAR",
            nullable=False,
        ),
        sa.Column(
            "term_start",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "maturity_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "status",
            stokvel_investment_status,
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
            ["stokvel_id"],
            ["stokvels.id"],
        ),
        sa.ForeignKeyConstraint(
            ["investment_asset_id"],
            ["investment_assets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_stokvel_investments_stokvel_id",
        "stokvel_investments",
        ["stokvel_id"],
        unique=False,
    )

    op.create_index(
        "ix_stokvel_investments_investment_asset_id",
        "stokvel_investments",
        ["investment_asset_id"],
        unique=False,
    )

    # ------------------------------------------------------------
    # 4. Create investment_allocations.
    #
    # One row represents one member's economic participation in
    # a collective stokvel investment.
    # ------------------------------------------------------------

    op.create_table(
        "investment_allocations",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "investment_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "member_account_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "contributed_amount",
            sa.Numeric(precision=18, scale=2),
            nullable=False,
        ),
        sa.Column(
            "participation_percentage",
            sa.Numeric(precision=18, scale=8),
            nullable=False,
        ),
        sa.Column(
            "allocated_quantity",
            sa.Numeric(precision=18, scale=8),
            nullable=False,
        ),
        sa.Column(
            "returned_amount",
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
            ["investment_id"],
            ["stokvel_investments.id"],
        ),
        sa.ForeignKeyConstraint(
            ["member_account_id"],
            ["member_accounts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_investment_allocations_investment_id",
        "investment_allocations",
        ["investment_id"],
        unique=False,
    )

    op.create_index(
        "ix_investment_allocations_member_account_id",
        "investment_allocations",
        ["member_account_id"],
        unique=False,
    )

    # ------------------------------------------------------------
    # 5. Extend treasury_ledger.
    #
    # Existing contribution entries continue to use
    # transaction_id.
    #
    # Investment deployment/return entries can use investment_id.
    # A distribution can use both.
    # ------------------------------------------------------------

    op.alter_column(
        "treasury_ledger",
        "transaction_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=True,
    )

    op.add_column(
        "treasury_ledger",
        sa.Column(
            "investment_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_treasury_ledger_investment_id",
        "treasury_ledger",
        ["investment_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_treasury_ledger_investment_id",
        "treasury_ledger",
        "stokvel_investments",
        ["investment_id"],
        ["id"],
    )

    op.create_check_constraint(
        "ck_treasury_ledger_has_source",
        "treasury_ledger",
        "transaction_id IS NOT NULL OR investment_id IS NOT NULL",
    )


def downgrade() -> None:
    """Restore the previous member-level investment schema."""

    # ------------------------------------------------------------
    # Reverse treasury ledger changes.
    # ------------------------------------------------------------

    op.drop_constraint(
        "ck_treasury_ledger_has_source",
        "treasury_ledger",
        type_="check",
    )

    op.drop_constraint(
        "fk_treasury_ledger_investment_id",
        "treasury_ledger",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_treasury_ledger_investment_id",
        table_name="treasury_ledger",
    )

    op.drop_column(
        "treasury_ledger",
        "investment_id",
    )

    op.alter_column(
        "treasury_ledger",
        "transaction_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=False,
    )

    # ------------------------------------------------------------
    # Remove new investment tables.
    # ------------------------------------------------------------

    op.drop_index(
        "ix_investment_allocations_member_account_id",
        table_name="investment_allocations",
    )

    op.drop_index(
        "ix_investment_allocations_investment_id",
        table_name="investment_allocations",
    )

    op.drop_table("investment_allocations")

    op.drop_index(
        "ix_stokvel_investments_investment_asset_id",
        table_name="stokvel_investments",
    )

    op.drop_index(
        "ix_stokvel_investments_stokvel_id",
        table_name="stokvel_investments",
    )

    op.drop_table("stokvel_investments")

    # ------------------------------------------------------------
    # Restore the old tables.
    # ------------------------------------------------------------

    investment_order_status = postgresql.ENUM(
        "PENDING",
        "PROCESSING",
        "COMPLETED",
        "FAILED",
        "CANCELLED",
        name="investmentorderstatus",
        create_type=False,
    )

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

    # The new enum is no longer needed after rollback.
    sa.Enum(
        name="stokvelinvestmentstatus",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )
