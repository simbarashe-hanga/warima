"""add contribution source to investment allocations

Revision ID: 7c2f9a1d4e61
Revises: b38496242397
Create Date: 2026-09-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "7c2f9a1d4e61"
down_revision: Union[str, Sequence[str], None] = "b38496242397"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "investment_allocations",
        sa.Column(
            "contribution_transaction_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_investment_allocations_contribution_transaction_id",
        "investment_allocations",
        ["contribution_transaction_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_investment_allocations_contribution_transaction_id",
        "investment_allocations",
        "wallet_transactions",
        ["contribution_transaction_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_investment_allocations_contribution_transaction_id",
        "investment_allocations",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_investment_allocations_contribution_transaction_id",
        table_name="investment_allocations",
    )

    op.drop_column(
        "investment_allocations",
        "contribution_transaction_id",
    )
