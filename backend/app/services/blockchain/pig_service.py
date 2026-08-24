from typing import Dict, List, Optional
from web3 import Web3
from app.core.config import settings
from app.services.blockchain.contract_service import ContractService

class PigService:
    """Service for pig NFT operations"""
    
    def __init__(self):
        self.contract_service = ContractService()
        self.nft_contract = self.contract_service.get_contract('nft')
        self.w3 = self.contract_service.w3
    
    async def get_pig_details(self, token_id: int) -> Dict:
        """Get pig details by token ID"""
        try:
            pig_data = self.nft_contract.functions.pigs(token_id).call()
            return {
                'token_id': token_id,
                'breed': pig_data[1],
                'birth_date': pig_data[2],
                'purchase_date': pig_data[3],
                'farm_location': pig_data[4],
                'health_status': pig_data[5],
                'is_active': pig_data[8],
                'metadata_uri': pig_data[9]
            }
        except Exception as e:
            return {'error': str(e)}
    
    async def get_pig_value(self, token_id: int) -> float:
        """Get current value of a pig"""
        # Placeholder - implement actual valuation logic
        return 12500.0
    
    async def get_balance(self, address: str) -> int:
        """Get number of pigs owned by an address"""
        try:
            return self.nft_contract.functions.balanceOf(address).call()
        except Exception:
            return 0
    
    async def get_token_by_index(self, address: str, index: int) -> int:
        """Get token ID by index for an address"""
        try:
            return self.nft_contract.functions.tokenOfOwnerByIndex(address, index).call()
        except Exception:
            return 0
