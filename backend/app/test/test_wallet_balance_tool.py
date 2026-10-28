import unittest
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.models.enums import WalletStatus
from app.services.ai.tools.wallet_balance_tool import (
    WalletBalanceTool,
)


class WalletBalanceToolTests(unittest.TestCase):

    def setUp(self):
        self.db = Mock()
        self.member_account = SimpleNamespace(
            id="member-123"
        )

    @patch(
        "app.services.ai.tools.wallet_balance_tool."
        "WalletBalanceService.get_balance"
    )
    @patch(
        "app.services.ai.tools.wallet_balance_tool."
        "WalletService.get_wallet"
    )
    def test_returns_authenticated_members_balance(
        self,
        get_wallet,
        get_balance,
    ):
        wallet = SimpleNamespace(
            id="wallet-123",
            member_account_id=self.member_account.id,
            balance=Decimal("125.50"),
            currency="ZAR",
            status=WalletStatus.ACTIVE,
        )
        get_wallet.return_value = wallet
        get_balance.return_value = Decimal("125.50")

        result = WalletBalanceTool.execute(
            self.db,
            self.member_account,
        )

        self.assertEqual(result["ok"], True)
        self.assertEqual(result["balance"], "125.50")
        self.assertEqual(result["currency"], "ZAR")

        get_wallet.assert_called_once_with(
            db=self.db,
            member_account=self.member_account,
        )
        get_balance.assert_called_once_with(wallet)

    @patch(
        "app.services.ai.tools.wallet_balance_tool."
        "WalletBalanceService.get_balance"
    )
    @patch(
        "app.services.ai.tools.wallet_balance_tool."
        "WalletService.get_wallet"
    )
    def test_missing_wallet_is_not_created(
        self,
        get_wallet,
        get_balance,
    ):
        get_wallet.return_value = None

        result = WalletBalanceTool.execute(
            self.db,
            self.member_account,
        )

        self.assertTrue(result["ok"])
        self.assertFalse(result["wallet_found"])
        get_balance.assert_not_called()

    @patch(
        "app.services.ai.tools.wallet_balance_tool."
        "WalletBalanceService.get_balance"
    )
    @patch(
        "app.services.ai.tools.wallet_balance_tool."
        "WalletService.get_wallet"
    )
    def test_inactive_wallet_balance_is_not_exposed(
        self,
        get_wallet,
        get_balance,
    ):
        get_wallet.return_value = SimpleNamespace(
            member_account_id=self.member_account.id,
            balance=Decimal("500.00"),
            currency="ZAR",
            status=WalletStatus.SUSPENDED,
        )

        result = WalletBalanceTool.execute(
            self.db,
            self.member_account,
        )

        self.assertFalse(result["ok"])
        self.assertNotIn("balance", result)
        get_balance.assert_not_called()

    @patch(
        "app.services.ai.tools.wallet_balance_tool."
        "WalletService.get_wallet"
    )
    def test_missing_member_account_is_rejected(
        self,
        get_wallet,
    ):
        result = WalletBalanceTool.execute(
            self.db,
            None,
        )

        self.assertFalse(result["ok"])
        get_wallet.assert_not_called()

    @patch(
        "app.services.ai.tools.wallet_balance_tool."
        "WalletService.get_wallet"
    )
    def test_unexpected_lookup_error_returns_safe_response(
        self,
        get_wallet,
    ):
        get_wallet.side_effect = RuntimeError(
            "Internal database details"
        )

        result = WalletBalanceTool.execute(
            self.db,
            self.member_account,
        )

        self.assertFalse(result["ok"])
        self.assertEqual(
            result["error"],
            "Unable to retrieve your wallet right now.",
        )
        self.assertNotIn("Internal database details", str(result))


if __name__ == "__main__":
    unittest.main()
