"""add join code to stokvels

Revision ID: add_stokvel_join_code
Revises: 1841a11ea56e
"""

from alembic import op
import sqlalchemy as sa


revision = "add_stokvel_join_code"
down_revision = "1841a11ea56e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "stokvels",
        sa.Column("join_code", sa.String(length=12), nullable=False),
    )

    op.create_unique_constraint(
        "uq_stokvels_join_code",
        "stokvels",
        ["join_code"],
    )


def downgrade():
    op.drop_constraint(
        "uq_stokvels_join_code",
        "stokvels",
        type_="unique",
    )

    op.drop_column("stokvels", "join_code")
