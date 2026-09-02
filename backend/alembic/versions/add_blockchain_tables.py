"""add blockchain tables

Revision ID: a91c7e4d2b10
Revises: 28fb57b58835
Create Date: 2026-08-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


revision = "a91c7e4d2b10"
down_revision = "c37f8a91b624"
branch_labels = None
depends_on = None

def upgrade():
    # Pigs table
    op.create_table(
        "pigs",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "token_id",
            sa.Integer,
            unique=True,
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "breed",
            sa.String,
            nullable=False,
        ),
        sa.Column(
            "birth_date",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "purchase_date",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "farm_location",
            sa.String,
            nullable=False,
        ),
        sa.Column(
            "health_status",
            sa.String,
            nullable=False,
            server_default="Healthy",
        ),
        sa.Column(
            "current_owner",
            sa.String,
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean,
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "metadata_uri",
            sa.String,
            nullable=True,
        ),
        sa.Column(
            "blockchain_data",
            JSONB,
            nullable=True,
        ),
        sa.Column(
            "last_synced",
            sa.DateTime(timezone=True),
            nullable=True,
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

    # Health events table
    op.create_table(
        "health_events",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "pig_id",
            UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "event_type",
            sa.String,
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String,
            nullable=True,
        ),
        sa.Column(
            "performed_by",
            sa.String,
            nullable=True,
        ),
        sa.Column(
            "cost",
            sa.Float,
            nullable=True,
            server_default="0",
        ),
        sa.Column(
            "document_hash",
            sa.String,
            nullable=True,
        ),
        sa.Column(
            "transaction_hash",
            sa.String,
            nullable=True,
        ),
        sa.Column(
            "block_number",
            sa.Integer,
            nullable=True,
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("health_events")
    op.drop_table("pigs")
