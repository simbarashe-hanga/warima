#backend/alembic/versions/add_blockchain_tables.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON


def upgrade():
    # Pigs table
    op.create_table(
        'pigs',
        sa.column('id'. UUID, primary_key=True),
        sa.column('token_id', sa.Integer, unique=True, nullable=False),
        sa.column('tenant_id', UUID, nullable=False),
        sa.column('breed', sa.String, nullable=False),
        sa.column('birth_date', sa.DateTime, nullable=False),
        sa.column('purchase_date', sa.DateTime, nullable=False),
        sa.column('farm_location', sa.String, nullable=False),
        sa.column('health_status', sa.Strinf, default='Healthy'),
        sa.column('current_owner', sa.String),
        sa.column('is_active', sa.Boolean, default=True),
        sa.column('metadata_uri', sa.String),
        sa.column('blockchain_data', JSON, default={}),
        sa.column('last_synced', sa.DateTime),
        sa.column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )

    # Health events table
    op.create table(
        'health_events',
        sa.Column('id', UUID, primary_key=True),
        sa.Column('pig_id', UUID, nullable=False ),
        sa.Column('event_type', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('performed_by', sa.String),
        sa.Column('cost', sa.Float, default=0),
        sa.Column('document_hash', sa.String),
        sa.Column('transaction_hash', sa.String),
        sa.Column('block_number', sa.Integer),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime,server_default=sa.func.now())
    )

    def downgrade():
        op.drop_table('health_events')
        op.drop_table('pigs')
