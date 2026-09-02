"""add stokvel and membership tables

Revision ID: c37f8a91b624
Revises: 28fb57b58835
Create Date: 2026-08-25
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision = "c37f8a91b624"
down_revision = "28fb57b58835"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ---------------------------------------------------------
    # Stokvels
    # ---------------------------------------------------------

    op.create_table(
        "stokvels",

        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(length=120),
            nullable=False,
        ),

        sa.Column(
            "description",
            sa.Text,
            nullable=True,
        ),

        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "ACTIVE",
                "SUSPENDED",
                "CLOSED",
                name="stokvelstatus",
            ),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


    # ---------------------------------------------------------
    # Memberships
    # ---------------------------------------------------------

    op.create_table(
        "memberships",

        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "member_account_id",
            UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "stokvel_id",
            UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "role",
            sa.Enum(
                "OWNER",
                "ADMIN",
                "TREASURER",
                "SECRETARY",
                "MEMBER",
                name="membershiprole",
            ),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "ACTIVE",
                "SUSPENDED",
                "LEFT",
                name="membershipstatus",
            ),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["member_account_id"],
            ["member_accounts.id"],
        ),

        sa.ForeignKeyConstraint(
            ["stokvel_id"],
            ["stokvels.id"],
        ),
    )


def downgrade() -> None:

    op.drop_table("memberships")
    op.drop_table("stokvels")

    op.execute(
        "DROP TYPE IF EXISTS membershipstatus"
    )

    op.execute(
        "DROP TYPE IF EXISTS membershiprole"
    )

    op.execute(
        "DROP TYPE IF EXISTS stokvelstatus"
    )
