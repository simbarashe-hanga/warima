"""add member blockchain accounts

Revision ID: 905a950944c5
Revises: 853bc628699c
Create Date: 2026-09-18

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "905a950944c5"
down_revision: Union[str, Sequence[str], None] = "a40df3fd3349"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create blockchain accounts for member accounts."""

    op.create_table(
        "blockchain_accounts",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "member_account_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "chain",
            sa.Enum(
                "SOLANA",
                "EVM",
                name="blockchainchain",
            ),
            nullable=False,
        ),
        sa.Column(
            "network",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "address",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "account_type",
            sa.Enum(
                "MANAGED",
                "EXTERNAL",
                name="blockchainaccounttype",
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE",
                "SUSPENDED",
                "CLOSED",
                name="blockchainaccountstatus",
            ),
            nullable=False,
        ),
        sa.Column(
            "signer_reference",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["member_account_id"],
            ["member_accounts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "member_account_id",
            "chain",
            "network",
            name="uq_blockchain_account_member_chain_network",
        ),
    )

    op.create_index(
        "ix_blockchain_accounts_member_account_id",
        "blockchain_accounts",
        ["member_account_id"],
        unique=False,
    )

    op.create_index(
        "ix_blockchain_accounts_address",
        "blockchain_accounts",
        ["address"],
        unique=False,
    )


def downgrade() -> None:
    """Remove blockchain accounts."""

    op.drop_index(
        "ix_blockchain_accounts_address",
        table_name="blockchain_accounts",
    )

    op.drop_index(
        "ix_blockchain_accounts_member_account_id",
        table_name="blockchain_accounts",
    )

    op.drop_table("blockchain_accounts")

    op.execute("DROP TYPE IF EXISTS blockchainaccountstatus")
    op.execute("DROP TYPE IF EXISTS blockchainaccounttype")
    op.execute("DROP TYPE IF EXISTS blockchainchain")
