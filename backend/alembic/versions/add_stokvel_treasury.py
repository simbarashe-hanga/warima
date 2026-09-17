"""add stokvel treasury

Revision ID: add_stokvel_treasury
Revises: cfccc61935d0
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "add_stokvel_treasury"
down_revision = "cfccc61935d0"
branch_labels = None
depends_on = None


def upgrade():
    # ============================================================
    # PostgreSQL enum types
    # ============================================================

    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_type
                WHERE typname = 'treasurydenomination'
            ) THEN
                CREATE TYPE treasurydenomination AS ENUM (
                    'SOL',
                    'WZAR',
                    'ZAR'
                );
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
                WHERE typname = 'treasuryrail'
            ) THEN
                CREATE TYPE treasuryrail AS ENUM (
                    'SOLANA',
                    'EVM',
                    'OFF_CHAIN'
                );
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
                WHERE typname = 'treasurystrategy'
            ) THEN
                CREATE TYPE treasurystrategy AS ENUM (
                    'ON_CHAIN',
                    'AGRICULTURE',
                    'CASH'
                );
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
                WHERE typname = 'treasuryreturnsource'
            ) THEN
                CREATE TYPE treasuryreturnsource AS ENUM (
                    'ON_CHAIN',
                    'MEAT_SALES',
                    'CASH_RETURNS'
                );
            END IF;
        END
        $$;
    """)

    # ============================================================
    # Stokvel treasury table
    # ============================================================

    op.create_table(
        "stokvel_treasuries",

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "stokvel_id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "denomination",
            postgresql.ENUM(
                "SOL",
                "WZAR",
                "ZAR",
                name="treasurydenomination",
                create_type=False,
            ),
            nullable=False,
        ),

        sa.Column(
            "rail",
            postgresql.ENUM(
                "SOLANA",
                "EVM",
                "OFF_CHAIN",
                name="treasuryrail",
                create_type=False,
            ),
            nullable=False,
        ),

        sa.Column(
            "network",
            sa.String(length=50),
            nullable=True,
        ),

        sa.Column(
            "strategy",
            postgresql.ENUM(
                "ON_CHAIN",
                "AGRICULTURE",
                "CASH",
                name="treasurystrategy",
                create_type=False,
            ),
            nullable=False,
        ),

        sa.Column(
            "return_source",
            postgresql.ENUM(
                "ON_CHAIN",
                "MEAT_SALES",
                "CASH_RETURNS",
                name="treasuryreturnsource",
                create_type=False,
            ),
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
            name="fk_stokvel_treasuries_stokvel_id",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    # One treasury per stokvel.
    op.create_index(
        "ix_stokvel_treasuries_stokvel_id",
        "stokvel_treasuries",
        ["stokvel_id"],
        unique=True,
    )


def downgrade():
    op.drop_index(
        "ix_stokvel_treasuries_stokvel_id",
        table_name="stokvel_treasuries",
    )

    op.drop_table("stokvel_treasuries")

    op.execute(
        "DROP TYPE IF EXISTS treasuryreturnsource"
    )

    op.execute(
        "DROP TYPE IF EXISTS treasurystrategy"
    )

    op.execute(
        "DROP TYPE IF EXISTS treasuryrail"
    )

    op.execute(
        "DROP TYPE IF EXISTS treasurydenomination"
    )
