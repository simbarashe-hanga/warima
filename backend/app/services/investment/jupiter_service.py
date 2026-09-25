import base64

import httpx


class JupiterService:
    """
    Prepares Jupiter swap transactions.

    This service does not sign or broadcast transactions.
    The returned transaction must be signed by the designated
    Solana wallet before it can be executed on-chain.
    """

    BASE_URL = "https://lite-api.jup.ag/swap/v1"

    async def get_quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
        slippage_bps: int = 50,
    ) -> dict:
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount),
            "slippageBps": str(slippage_bps),
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/quote",
                params=params,
                headers={"Accept": "application/json"},
            )

            response.raise_for_status()
            return response.json()

    async def build_swap(
        self,
        quote: dict,
        user_public_key: str,
    ) -> dict:
        payload = {
            "quoteResponse": quote,
            "userPublicKey": user_public_key,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.BASE_URL}/swap",
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            response.raise_for_status()

            result = response.json()

            if not result.get("swapTransaction"):
                raise RuntimeError(
                    "Jupiter did not return a swap transaction"
                )

            return result

    @staticmethod
    def decode_transaction(transaction: str) -> bytes:
        return base64.b64decode(transaction)
