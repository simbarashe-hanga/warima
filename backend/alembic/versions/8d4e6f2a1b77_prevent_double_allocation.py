"""prevent double allocation of contribution transactions

Revision ID: 8d4e6f2a1b77
Revises: 7c2f9a1d4e61
"""

from alembic import op


revision = "8d4e6f2a1b77"
down_revision = "7c2f9a1d4e61"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        "uq_investment_allocation_contribution_transaction",
        "investment_allocations",
        ["contribution_transaction_id"],
    )


def downgrade():
    op.drop_constraint(
        "uq_investment_allocation_contribution_transaction",
        "investment_allocations",
        type_="unique",
    )
