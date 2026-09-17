from typing import Dict

from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction

from app.core.config import settings

class SolanaService:
    """Service for Solana blockchain operations."""

    def __init__(self):
        self.rpc_url = settings.SOLANA_RPC_URL
        self.network = settings.SOLANA_NETWORK

    def get_treasury_keypair(self) -> Keypair:
        """Load the Warima Solana tresury keypair."""

        private_key = settings.SOLANA_TREASURY_PRIVATE_KEY

        if not private_key:
            raise RuntimeError(
                "SOLANA_TREASURY_PRIVATE_KEY is not configured"
            )

        return Keypair.from_base58_string(private_key)

    async def get_client(self) -> AsyncClient:
        """Create a Solana RPC client."""
        return AsyncClient(self.rpc_url)

    @staticmethod
    def generate_keypair() -> Keypair:
        """Generate a new Solana keypair."""
        return Keypair()

    async def get_balance(self, address: str) -> float:
        """Get SOL balance for an address."""

        client = await self.get_client()

        try:
            pubkey = Pubkey.from_string(address)
            response = await client.get_balance(pubkey)

            # Lamports -> SOL
            return response.value / 1_000_000_000

        finally:
            await client.close()

    async def get_signature_status(self, signature: str):
        """Get the on-chain status of an existing Solana transaction."""

        if not signature:
            raise ValueError(
                "Solana transaction signature is required"
            )

        from solders.signature import Signature

        client = await self.get_client()

        try:
            signature_obj = Signature.from_string(signature)

            response = await client.get_signature_statuses(
                [signature_obj],
                search_transaction_history=True,
            )

            if not response.value:
                return None

            return response.value[0]

        finally:
            await client.close()

    async def send_sol(
        self,
        sender: Keypair,
        recipient: str,
        amount_sol: float,
    ) -> Dict:
        """Send SOL from one Solana account to another."""

        client = await self.get_client()

        try:
            recipient_pubkey = Pubkey.from_string(recipient)

            # SOL uses lamports internally
            lamports = int(amount_sol * 1_000_000_000)

            transfer_instruction = transfer(
                TransferParams(
                    from_pubkey=sender.pubkey(),
                    to_pubkey=recipient_pubkey,
                    lamports=lamports,
                )
            )

            blockhash_response = await client.get_latest_blockhash()

            transaction = Transaction.new_signed_with_payer(
                [transfer_instruction],
                sender.pubkey(),
                [sender],
                blockhash_response.value.blockhash,
            )

            response = await client.send_transaction(
                transaction
            )

            return {
                "success": True,
                "signature": str(response.value),
                "amount_sol": amount_sol,
                "network": self.network,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

        finally:
            await client.close()
