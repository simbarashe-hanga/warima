#backend/app/models/pig.py
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base


class Pig(Base):
    __tablename__ = 'pigs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_id = Column(Integer, unique=True, nullable=False)
    tenant_id = Column(UUID, ForeignKey('tenants.id'), nullable=False)

    breed = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=False)
    purchase_date = Column(String, nullable=False)
    farm_location = Column(String, nullable=False)
    health_status = Column(String, default='Healthy')
    current_owner = Column(String) # Blockchain address
    is_active = Column(Boolean, default=True)
    metadat_uri = Column(String)

    #On-chain data
    blockchain_data = Column(JSON, default={})
    last_synced = Column(DateTime)

    # Relationships
    tenant = relationship("Tenant", back_populates="pigs")
    health_events = relationship("HealthEvent", back_populates="pigs")


class HealthEvent(Base):
    __tablename__ = 'health_events'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pig_id = Column(UUID, ForeignKey('pigs.id'), nullable=False)

    event_type = Column(String, nullable=False)
    description = Column(String)
    performed_by = Column(String) # Blockchain address
    cost = Column(Float, default=0)
    document_hash = Column(String)
    transaction_hash = Column(String)
    block_number = Column(Integer)
    timestamp = Column(DateTime, nullable=False)

    pig = relationship("Pig", back_populates="health_events")
