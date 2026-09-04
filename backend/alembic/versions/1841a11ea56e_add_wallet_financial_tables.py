"""add wallet financial tables

Revision ID: 1841a11ea56e
Revises: dc7c57172e97
Create Date: 2026-08-xx
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "1841a11ea56e"
down_revision: Union[str, None] = "dc7c57172e97"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # PostgreSQL enums
    wallet_status = postgresql.ENUM(
        "ACTIVE",
        "SUSPENDED",
        "CLOSED",
        name="walletstatus",
    )

    wallet_transaction_type = postgresql.ENUM(
        "CONTRIBUTION",
        "DEPOSIT",
        "WITHDRAWAL",
        "TRANSFER",
        name="wallettransactiontype",
    )

    wallet_transaction_status = postgresql.ENUM(
        "PENDING",
        "PROCESSING",
        "COMPLETED",
        "FAILED",
        "CANCELLED",
        name="wallettransactionstatus",
    )

    wallet_ledger_entry_type = postgresql.ENUM(
        "CREDIT",
        "DEBIT",
        name="walletledgerentrytype",
    )

    wallet_status.create(op.get_bind(), checkfirst=True)
    wallet_transaction_type.create(op.get_bind(), checkfirst=True)
    wallet_transaction_status.create(op.get_bind(), checkfirst=True)
    wallet_ledger_entry_type.create(op.get_bind(), checkfirst=True)

    # Wallets
    op.create_table(
        "wallets",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "member_account_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "balance",
            sa.Numeric(precision=18, scale=2),
            nullable=False,
        ),
        sa.Column(
            "status",
            wallet_status,
            nullable=False,
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
            name="wallets_member_account_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_wallets_member_account_id",
        "wallets",
        ["member_account_id"],
        unique=True,
    )

    # Wallet transactions
    op.create_table(
        "wallet_transactions",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "wallet_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "transaction_type",
            wallet_transaction_type,
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.Numeric(precision=18, scale=2),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "status",
            wallet_transaction_status,
            nullable=False,
        ),
        sa.Column(
            "reference",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
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
            ["wallet_id"],
            ["wallets.id"],
            name="wallet_transactions_wallet_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_wallet_transactions_wallet_id",
        "wallet_transactions",
        ["wallet_id"],
        unique=False,
    )

    op.create_index(
        "ix_wallet_transactions_reference",
        "wallet_transactions",
        ["reference"],
        unique=True,
    )

    # Wallet ledger
    op.create_table(
        "wallet_ledger",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "wallet_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "transaction_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "entry_type",
            wallet_ledger_entry_type,
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.Numeric(precision=18, scale=2),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["wallet_id"],
            ["wallets.id"],
            name="wallet_ledger_wallet_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["transaction_id"],
            ["wallet_transactions.id"],
            name="wallet_ledger_transaction_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_wallet_ledger_wallet_id",
        "wallet_ledger",
        ["wallet_id"],
        unique=False,
    )

    op.create_index(
        "ix_wallet_ledger_transaction_id",
        "wallet_ledger",
        ["transaction_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_wallet_ledger_transaction_id",
        table_name="wallet_ledger",
    )

    op.drop_index(
        "ix_wallet_ledger_wallet_id",
        table_name="wallet_ledger",
    )

    op.drop_table("wallet_ledger")

    op.drop_index(
        "ix_wallet_transactions_reference",
        table_name="wallet_transactions",
    )

    op.drop_index(
        "ix_wallet_transactions_wallet_id",
        table_name="wallet_transactions",
    )

    op.drop_table("wallet_transactions")

    op.drop_index(
        "ix_wallets_member_account_id",
        table_name="wallets",
    )

    op.drop_table("wallets")

    op.execute("DROP TYPE IF EXISTS walletledgerentrytype")
    op.execute("DROP TYPE IF EXISTS wallettransactionstatus")
    op.execute("DROP TYPE IF EXISTS wallettransactiontype")
    op.execute("DROP TYPE IF EXISTS walletstatus")
