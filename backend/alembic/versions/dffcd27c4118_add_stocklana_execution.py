"""add stocklana execution

Revision ID: dffcd27c4118
Revises: 8d4e6f2a1b77
Create Date: 2026-09-25

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "dffcd27c4118"
down_revision = "8d4e6f2a1b77"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "stocklana_executions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("investment_id", sa.UUID(), nullable=False),
        sa.Column("amount_sol", sa.Numeric(36, 18), nullable=False),
        sa.Column("destination", sa.String(length=100), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("network", sa.String(length=50), nullable=False),
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
            ["investment_id"],
            ["stokvel_investments.id"],
            name="fk_stocklana_executions_investment_id",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_stocklana_executions_investment_id",
        "stocklana_executions",
        ["investment_id"],
        unique=True,
    )

    op.create_index(
        "ix_stocklana_executions_transaction_signature",
        "stocklana_executions",
        ["transaction_signature"],
        unique=True,
    )


def downgrade():
    op.drop_index(
        "ix_stocklana_executions_transaction_signature",
        table_name="stocklana_executions",
    )

    op.drop_index(
        "ix_stocklana_executions_investment_id",
        table_name="stocklana_executions",
    )

    op.drop_table("stocklana_executions")
