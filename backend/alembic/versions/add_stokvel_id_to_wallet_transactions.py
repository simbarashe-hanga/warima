"""add stokvel id to wallet transactions

Revision ID: add_stokvel_id_wallet_tx
Revises: add_stokvel_join_code
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "add_stokvel_id_wallet_tx"
down_revision = "add_stokvel_join_code"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "wallet_transactions",
        sa.Column(
            "stokvel_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_wallet_transactions_stokvel_id",
        "wallet_transactions",
        ["stokvel_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_wallet_transactions_stokvel_id",
        "wallet_transactions",
        "stokvels",
        ["stokvel_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint(
        "fk_wallet_transactions_stokvel_id",
        "wallet_transactions",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_wallet_transactions_stokvel_id",
        table_name="wallet_transactions",
    )

    op.drop_column(
        "wallet_transactions",
        "stokvel_id",
    )
