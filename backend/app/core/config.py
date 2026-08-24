import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://warima_user:kGomoTso90@warima.cwz240eoqfjh.us-east-1.rds.amazonaws.com:5432/warima")
    RPC_URL: str = os.getenv("RPC_URL", "http://anvil:8545")
    CHAIN_ID: int = int(os.getenv("CHAIN_ID", "31337"))
    DEPLOYER_PRIVATE_KEY: str = os.getenv("DEPLOYER_PRIVATE_KEY", "")
    NFT_ADDRESS: str = os.getenv("NFT_ADDRESS", "")
    TOKEN_ADDRESS: str = os.getenv("TOKEN_ADDRESS", "")
    GOVERNANCE_ADDRESS: str = os.getenv("GOVERNANCE_ADDRESS", "")
    ORACLE_ADDRESS: str = os.getenv("ORACLE_ADDRESS", "")
    PAYMASTER_ADDRESS: str = os.getenv("PAYMASTER_ADDRESS", "")
    ENTRY_POINT_ADDRESS: str = os.getenv("ENTRY_POINT", "")
    ACCOUNT_FACTORY_ADDRESS: str = os.getenv("ACCOUNT_FACTORY_ADDRESS", "")
    ABI_DIR: str = "/app/app/abi"

settings = Settings()
