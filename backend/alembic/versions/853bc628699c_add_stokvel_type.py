"""add stokvel type

Revision ID: 853bc628699c
Revises: add_stokvel_treasury
Create Date: 2026-09-17 10:02:41.077864

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "853bc628699c"
down_revision: Union[str, Sequence[str], None] = "add_stokvel_treasury"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add user-facing stokvel type."""

    stokvel_type_enum = sa.Enum(
        "SAVINGS",
        "AGRICULTURE",
        "DIGITAL_ASSET",
        name="stokveltype",
    )

    stokvel_type_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "stokvels",
        sa.Column(
            "stokvel_type",
            stokvel_type_enum,
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE stokvels
        SET stokvel_type = 'SAVINGS'
        WHERE stokvel_type IS NULL
        """
    )

    op.alter_column(
        "stokvels",
        "stokvel_type",
        nullable=False,
        server_default="SAVINGS",
    )


def downgrade() -> None:
    """Remove user-facing stokvel type."""

    op.drop_column(
        "stokvels",
        "stokvel_type",
    )

    sa.Enum(
        "SAVINGS",
        "AGRICULTURE",
        "DIGITAL_ASSET",
        name="stokveltype",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )
