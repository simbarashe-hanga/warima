
from app.services.ai.tools.wallet_balance_tool import WalletBalanceTool


class ToolRegistry:
    """Explicit allowlist for AI-agent tools."""

    _TOOLS = {
        "wallet_balance": "wallet_balance",
    }

    @classmethod
    def execute(
        cls,
        tool_name: str,
        *,
        db,
        member_account,
    ) -> dict:
        registered_tool = cls._TOOLS.get(tool_name)

        if registered_tool is None:
            return {
                "ok": False,
                "error": "Requested tool is not available.",
            }

        if registered_tool == "wallet_balance":
            return WalletBalanceTool.execute(
                db=db,
                member_account=member_account,
            )

        return {
            "ok": False,
            "error": "Requested tool is not available.",
        }
