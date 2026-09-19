from solders.keypair import Keypair


class SolanaAccountProvider:
    """
    Devnet signing provider.

    The public address is persisted in BlockchainAccount.

    Private signing keys remain in process memory only.

    This is intentionally a Devnet MVP implementation.
    Production custody should use encrypted/KMS/HSM-backed signing.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._accounts = {}

        return cls._instance

    def create_account(self) -> tuple[str, Keypair]:
        """
        Generate and register a new Solana account.
        """

        keypair = Keypair()
        address = str(keypair.pubkey())

        self._accounts[address] = keypair

        return address, keypair

    def get_signer(self, address: str) -> Keypair:
        """
        Return the in-memory signer for an address.
        """

        signer = self._accounts.get(address)

        if signer is None:
            raise ValueError(
                "No signer is available for this Solana account"
            )

        return signer
