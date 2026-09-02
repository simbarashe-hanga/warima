"""add health event pig foreign key

Revision ID: dc7c57172e97
Revises: a91c7e4d2b10
Create Date: 2026-08-24 22:25:31.760404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc7c57172e97'
down_revision: Union[str, Sequence[str], None] = 'a91c7e4d2b10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(
        "fk_health_events_pig_id",
        "health_events",
        "pigs",
        ["pig_id"],
        ["id"],
    )
 


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_health_events_pig_id",
        "health_events",
        type_="foreignkey",
    )
