import unittest
from unittest.mock import Mock, patch

from app.services.ai.tools.tool_registry import ToolRegistry


class ToolRegistryTests(unittest.TestCase):

    @patch(
        "app.services.ai.tools.tool_registry.WalletBalanceTool.execute"
    )
    def test_wallet_balance_is_allowlisted(self, execute):
        db = Mock()
        member_account = Mock()
        execute.return_value = {
            "ok": True,
            "wallet_found": True,
            "balance": "125.50",
            "currency": "ZAR",
        }

        result = ToolRegistry.execute(
            "wallet_balance",
            db=db,
            member_account=member_account,
        )

        self.assertEqual(result["balance"], "125.50")
        execute.assert_called_once_with(
            db=db,
            member_account=member_account,
        )

    @patch(
        "app.services.ai.tools.tool_registry.WalletBalanceTool.execute"
    )
    def test_unknown_tool_is_rejected(self, execute):
        result = ToolRegistry.execute(
            "arbitrary_tool",
            db=Mock(),
            member_account=Mock(),
        )

        self.assertFalse(result["ok"])
        self.assertEqual(
            result["error"],
            "Requested tool is not available.",
        )
        execute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
