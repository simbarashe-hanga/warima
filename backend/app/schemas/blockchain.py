# backend/app/schemas/blockchain
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PigMintRequest(BaseModel):
    breed: str
    farm_location: str
    metadata_uri: str
    tenant_id: str


class PigMintResponse(BaseModel):
    success: bool
    transaction_hash: Optional[str]
    token_id: Optional[int]
    error: Optional[str]


class PigDetailsResponse(BaseModel):
    token_id: int
    breed: str
    birth_date: datetime
    purchase_date: datetime
    farm_location: str
    health_status: str
    is_active: bool
    metadata_uri: str


class HealthEventRequest(BaseModel):
    token_id: int
    event_type: str
    description: str
    cost: float
    document_hash: str


class HealthEventResponse(BaseModel):
    success: bool
    transaction_hash: Optional[str]
    error: Optional[str]
