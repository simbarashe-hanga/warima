"""add source to settlements

Revision ID: add_settlement_source
Revises: 0f684ce2b2ce
"""

from alembic import op
import sqlalchemy as sa


revision = "add_settlement_source"
down_revision = "0f684ce2b2ce"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "settlements",
        sa.Column(
            "source",
            sa.String(length=100),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column(
        "settlements",
        "source",
    )
