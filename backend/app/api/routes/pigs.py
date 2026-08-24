# backend/app/api/routes/pigs.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.blockchain import (
    PigMintRequest, PigMintResponse,
    PigDetailsResponse, HealthEventRequest,
    HealthEventResponse
)
from app.services.blockchain.pig_service import PigService
from app.services.identity.auth import get_current_user
from app.models.user import User
from app.repositories.pig_repository import PigRepository


router = APIRouter(prefix="/api/v1/pigs", tags=["pigs"])

@router.post("/mint", response_model=PigResponse)
async def mint_pig(
    request: PigMintRequest,
    current_user: User = Depends(get_current_user)
):
    """Mint a new pig on the blockchain"""
    pig_service = PigService()

    #Check if user has breeder role
    has_role = await check_breeder_role(current_user.wallet_address)
    if not has_role:
        raise HTTPException(403, "User does not have breeder role")

    result = pig_service.mint_pig(
        breed=request.breed,
        farm_location=request.farm_location,
        metadata_uri=request.metadat_uri,
        private_key=current_user.private_key
    )

    if result['success']:
        # Save to database
        await PigRepository.create({
            'token_id': result['token_id'],
            'tenant_id': request.tenant_id,
            'breed': request.breed,
            'farm_location': request.farm_location,
            'metadata_uri': current_user.wallet_address,
            'blockchain_data': result
        })

    return result

@router.get("/{token_id}", response_model=PigDetailResponse)
async def get_pig(
    token_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get pig details from blockchain"""
    pig_service = PigService()
    result = pig_service.get_pig_details(token_id)

    if 'error' in result:
        raise HTTPException(404, result['error'])

    return result

@router.post("/health", response_model=HealthEventResponse)
async def record_health_event(
    request: HealthEventRequest,
    current_user: User = Depends(get_current_user)
):
    """Record a health event for a pig"""
    pig_service = PigService()

    #Check if user has vet role
    has_role = await check_vet_role(current_user.wallet_address)
    if not has_role:
        raise HTTPException(403, "User does not have vet role")

    result = pig_service.record_health_event(
        token_id=request.token_id,
        event_type=request.event_type,
        description=request.description,
        cost=request.cost,
        document_hash=request.document_hash,
        private_key=current_user.private_key
    )

    if result['success']:
        # Save health event to database
        await HealthEventRepository.create({
            'pig_id': request.token_id,
            'event_type': request.event_type,
            'description': request.description,
            'cost': request.cost,
            'document_hash': request.document_hash,
            'transaction_hash':result['transaction_hash'],
            'block_number': result['block_number'],
            'timestamp': datetime.utcnow()
        })

    return result
