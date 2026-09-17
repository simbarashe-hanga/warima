"""add settlement table

Revision ID: cfccc61935d0
Revises: add_stokvel_id_wallet_tx
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "cfccc61935d0"
down_revision = "add_stokvel_id_wallet_tx"
branch_labels = None
depends_on = None


def upgrade():
    # Create PostgreSQL enum types first.
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_type
                WHERE typname = 'settlementasset'
            ) THEN
                CREATE TYPE settlementasset AS ENUM ('SOL');
            END IF;
        END
        $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_type
                WHERE typname = 'settlementstatus'
            ) THEN
                CREATE TYPE settlementstatus AS ENUM (
                    'PENDING',
                    'PROCESSING',
                    'COMPLETED',
                    'FAILED',
                    'CANCELLED'
                );
            END IF;
        END
        $$;
    """)

    op.create_table(
        "settlements",

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "wallet_transaction_id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "asset",
            postgresql.ENUM(
                "SOL",
                name="settlementasset",
                create_type=False,
            ),
            nullable=False,
        ),

        sa.Column(
            "amount",
            sa.Numeric(36, 18),
            nullable=False,
        ),

        sa.Column(
            "destination",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "network",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "status",
            postgresql.ENUM(
                "PENDING",
                "PROCESSING",
                "COMPLETED",
                "FAILED",
                "CANCELLED",
                name="settlementstatus",
                create_type=False,
            ),
            nullable=False,
        ),

        sa.Column(
            "transaction_signature",
            sa.String(length=200),
            nullable=True,
        ),

        sa.Column(
            "error_message",
            sa.String(length=500),
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
            ["wallet_transaction_id"],
            ["wallet_transactions.id"],
            name="fk_settlements_wallet_transaction_id",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_settlements_wallet_transaction_id",
        "settlements",
        ["wallet_transaction_id"],
        unique=True,
    )

    op.create_index(
        "ix_settlements_transaction_signature",
        "settlements",
        ["transaction_signature"],
        unique=True,
    )


def downgrade():
    op.drop_index(
        "ix_settlements_transaction_signature",
        table_name="settlements",
    )

    op.drop_index(
        "ix_settlements_wallet_transaction_id",
        table_name="settlements",
    )

    op.drop_table("settlements")

    op.execute("DROP TYPE IF EXISTS settlementasset")
    op.execute("DROP TYPE IF EXISTS settlementstatus")
