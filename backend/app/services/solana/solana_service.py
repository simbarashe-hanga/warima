import json
from typing import Dict

from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction

from app.core.config import settings

class SolanaService:
    """Service for Solana blockchain operations."""

    def __init__(
        self,
        rpc_url: str | None = None,
        network: str | None = None,
        treasury_private_key: str | None = None,
        treasury_keypair_file: str | None = None,
    ):
        self.rpc_url = (
            rpc_url
            if rpc_url is not None
            else settings.SOLANA_RPC_URL
        )

        self.network = (
            network
            if network is not None
            else settings.SOLANA_NETWORK
        )

        self.treasury_private_key = (
            treasury_private_key
            if treasury_private_key is not None
            else settings.SOLANA_TREASURY_PRIVATE_KEY
        )

        self.treasury_keypair_file = treasury_keypair_file

    def get_treasury_keypair(self) -> Keypair:
        """Load the configured Warima Solana treasury keypair."""

        if self.treasury_keypair_file:
            try:
                with open(self.treasury_keypair_file) as f:
                    secret = bytes(json.load(f))

                return Keypair.from_bytes(secret)

            except Exception as exc:
                raise RuntimeError(
                    "Failed to load Solana treasury keypair file"
                ) from exc

        private_key = self.treasury_private_key

        if not private_key:
            raise RuntimeError(
                "Solana treasury private key is not configured"
            )

        return Keypair.from_base58_string(private_key)

    def get_treasury_address(self) -> str:
        """Return the public address of the Warima Solana treasury."""

        return str(
            self.get_treasury_keypair().pubkey()
        )

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
