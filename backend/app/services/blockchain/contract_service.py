# backend/app/service/blockchain/contract_service.py
import json
import os
from typing import Optional, Dict, Any
from web3 import Web3
from eth_account import Account
from app.core.config import settings


class ContractService:
    """Manages blockchain contract interactions"""

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))
        self.contracts = {}
        self._load_contracts()


    def _load_contracts(self):
        """Load contract ABIs and addresses"""
        # Load from environment or deployment files
        self.contracts = {
            'nft': {
                'address': settings.NFT_ADDRESS,
                'abi': self._load_abi('PigFarmingNFT')
            },
            'token': {
                'address': settings.TOKEN_ADDRESS,
                'abi': self._load_abi('StokvelPigShareToken')
            },
            'governance': {
                'address': settings.GOVERNANCE_ADDRESS,
                'abi': self._load_abi('StokvelGovernance')
            },
            'oracle': {
                'address': settings.ORACLE_ADDRESS,
                'abi': self._load.abi('PigPriceOracle')
            }
        }

    def _load_abi(self, contract_name: str) -> list:
        """Load contract ABI from file"""
        abi_path = os.path.join(
            settings.ABI_DIR,
            f'{contract_name}.json'
        )
        with open(abi_path, 'r') as f:
            return json.load(f)['abi']

    def get_contracts(self, name: str, address: Optional[str] = None):
        """Get contract instance"""
        contract_info = self.contracts.get(name)
        if not contract_info:
            raise ValueError(f"Contract {name} not found")

        addr = address or contract_info['address']
        return self.w3.eth.contract(
            address=addr,
            abi=contract_info['abi']
        )
