"""add blockchain address to stokvel treasury

Revision ID: a40df3fd3349
Revises: 853bc628699c
Create Date: 2026-09-17

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a40df3fd3349"
down_revision: Union[str, Sequence[str], None] = "853bc628699c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add blockchain address to stokvel treasuries."""

    op.add_column(
        "stokvel_treasuries",
        sa.Column(
            "blockchain_address",
            sa.String(length=100),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove blockchain address from stokvel treasuries."""

    op.drop_column(
        "stokvel_treasuries",
        "blockchain_address",
    )
