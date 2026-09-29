import json
from pathlib import Path

from solders.keypair import Keypair


class SolanaAccountProvider:
    """
    Devnet signing provider.

    BlockchainAccount persists the public blockchain identity.

    Private signing keys are persisted outside the database in
    the configured local signer directory.

    This is intentionally a Devnet MVP implementation.
    Production custody should use encrypted/KMS/HSM-backed signing.
    """

    DEFAULT_SIGNER_DIRECTORY = "/opt/warima/secrets/solana-member-accounts"

    _instance = None

    def __new__(cls, signer_directory: str | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance._signer_directory = Path(
                signer_directory or cls.DEFAULT_SIGNER_DIRECTORY
            )

            cls._instance._signer_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            cls._instance._accounts = {}

        return cls._instance

    def _keypair_path(self, address: str) -> Path:
        return self._signer_directory / f"{address}.json"

    def create_account(self) -> tuple[str, Keypair]:
        """
        Generate a new Solana account and persist its signer.
        """

        keypair = Keypair()
        address = str(keypair.pubkey())

        path = self._keypair_path(address)

        with open(path, "w") as f:
            json.dump(list(bytes(keypair)), f)

        self._accounts[address] = keypair

        return address, keypair

    def get_signer(self, address: str) -> Keypair:
        """
        Return a signer from memory or persistent storage.
        """

        signer = self._accounts.get(address)

        if signer is not None:
            return signer

        path = self._keypair_path(address)

        if not path.exists():
            raise ValueError(
                "No signer is available for this Solana account"
            )

        try:
            with open(path) as f:
                secret = bytes(json.load(f))

            signer = Keypair.from_bytes(secret)

        except Exception as exc:
            raise ValueError(
                "Failed to load signer for this Solana account"
            ) from exc

        if str(signer.pubkey()) != address:
            raise ValueError(
                "Stored signer does not match the Solana account address"
            )

        self._accounts[address] = signer

        return signer
