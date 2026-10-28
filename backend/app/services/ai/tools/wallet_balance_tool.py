import logging

from app.models.enums import WalletStatus
from app.services.wallet.wallet_balance_service import (
    WalletBalanceService,
)
from app.services.wallet.wallet_service import WalletService

logger = logging.getLogger(__name__)


class WalletBalanceTool:
    """Read-only access to the authenticated member's wallet balance."""

    @staticmethod
    def execute(db, member_account) -> dict:
        # Identity comes from the trusted routing context.
        # Never accept a member ID or wallet ID from the model.
        if member_account is None:
            return {
                "ok": False,
                "error": "Authenticated member account is required.",
            }

        try:
            wallet = WalletService.get_wallet(
                db=db,
                member_account=member_account,
            )
        except Exception:
            logger.exception("Wallet lookup failed")
            return {
                "ok": False,
                "error": "Unable to retrieve your wallet right now.",
            }

        if wallet is None:
            return {
                "ok": True,
                "wallet_found": False,
                "message": "No wallet was found for your account.",
            }

        if wallet.status != WalletStatus.ACTIVE:
            return {
                "ok": False,
                "wallet_found": True,
                "error": (
                    "Your wallet is not active. "
                    "I can't display its balance right now."
                ),
            }

        try:
            balance = WalletBalanceService.get_balance(wallet)
        except Exception:
            logger.exception("Wallet balance retrieval failed")
            return {
                "ok": False,
                "wallet_found": True,
                "error": "Unable to retrieve your balance right now.",
            }

        return {
            "ok": True,
            "wallet_found": True,
            "balance": str(balance),
            "currency": wallet.currency,
        }
