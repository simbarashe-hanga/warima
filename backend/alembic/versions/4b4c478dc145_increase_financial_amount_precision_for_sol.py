"""increase financial amount precision for sol

Revision ID: 4b4c478dc145
Revises: dffcd27c4118
Create Date: 2026-09-27
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4b4c478dc145"
down_revision = "dffcd27c4118"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "wallet_transactions",
        "amount",
        existing_type=sa.Numeric(18, 2),
        type_=sa.Numeric(18, 9),
        existing_nullable=False,
    )

    op.alter_column(
        "treasury_ledger",
        "amount",
        existing_type=sa.Numeric(18, 2),
        type_=sa.Numeric(18, 9),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "treasury_ledger",
        "amount",
        existing_type=sa.Numeric(18, 9),
        type_=sa.Numeric(18, 2),
        existing_nullable=False,
    )

    op.alter_column(
        "wallet_transactions",
        "amount",
        existing_type=sa.Numeric(18, 9),
        type_=sa.Numeric(18, 2),
        existing_nullable=False,
    )
