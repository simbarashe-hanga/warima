import unittest
from unittest.mock import AsyncMock, Mock, patch

from app.services.ai.agent_service import AgentService


class AgentToolDispatchTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.agent = AgentService()
        self.user = Mock()
        self.identity = Mock()
        self.session = Mock()
        self.member_account = Mock()
        self.db = Mock()

    async def _process(self, message):
        return await self.agent.process(
            user=self.user,
            identity=self.identity,
            session=self.session,
            member_account=self.member_account,
            message=message,
            db=self.db,
        )

    @patch(
        "app.services.ai.agent_service.SessionManager.update_context"
    )
    @patch(
        "app.services.ai.agent_service.SessionManager.context",
        return_value={"agent": {"history": []}},
    )
    @patch(
        "app.services.ai.agent_service.SessionManager.initialize"
    )
    @patch(
        "app.services.ai.agent_service.ContextBuilder.build_system_prompt",
        new_callable=AsyncMock,
        return_value="test system prompt",
    )
    @patch("app.services.ai.agent_service.ToolRegistry.execute")
    @patch("app.services.ai.agent_service.chat", new_callable=AsyncMock)
    async def test_balance_request_uses_allowlisted_tool(
        self,
        chat,
        execute,
        build_prompt,
        initialize,
        get_context,
        update_context,
    ):
        execute.return_value = {
            "ok": True,
            "wallet_found": True,
            "balance": "125.50",
            "currency": "ZAR",
        }

        result = await self._process("What is my wallet balance?")

        execute.assert_called_once_with(
            "wallet_balance",
            db=self.db,
            member_account=self.member_account,
        )
        chat.assert_not_called()
        self.assertEqual(
            result["message"],
            "Your available wallet balance is R125.50.",
        )
        self.assertEqual(result["type"], "text")

    @patch(
        "app.services.ai.agent_service.SessionManager.update_context"
    )
    @patch(
        "app.services.ai.agent_service.SessionManager.context",
        return_value={"agent": {"history": []}},
    )
    @patch(
        "app.services.ai.agent_service.SessionManager.initialize"
    )
    @patch(
        "app.services.ai.agent_service.ContextBuilder.build_system_prompt",
        new_callable=AsyncMock,
        return_value="test system prompt",
    )
    @patch("app.services.ai.agent_service.ToolRegistry.execute")
    @patch("app.services.ai.agent_service.chat", new_callable=AsyncMock)
    async def test_ordinary_message_uses_llm(
        self,
        chat,
        execute,
        build_prompt,
        initialize,
        get_context,
        update_context,
    ):
        chat.return_value = "Hello from the AI."

        result = await self._process("Hello, can you help me?")

        chat.assert_awaited_once()

        call_kwargs = chat.await_args.kwargs

        self.assertEqual(
            call_kwargs["user_message"],
            "Hello, can you help me?",
        )
        self.assertEqual(
            call_kwargs["system_prompt"],
            "test system prompt",
        )
        self.assertEqual(
            call_kwargs["history"],
            [
                {"role": "user", "content": "Hello, can you help me?"},
                {"role": "assistant", "content": "Hello from the AI."},
            ],
        )

        execute.assert_not_called()
        self.assertEqual(result["message"], "Hello from the AI.")

    @patch(
        "app.services.ai.agent_service.SessionManager.update_context"
    )
    @patch(
        "app.services.ai.agent_service.SessionManager.context",
        return_value={"agent": {"history": []}},
    )
    @patch(
        "app.services.ai.agent_service.SessionManager.initialize"
    )
    @patch(
        "app.services.ai.agent_service.ContextBuilder.build_system_prompt",
        new_callable=AsyncMock,
        return_value="test system prompt",
    )
    @patch("app.services.ai.agent_service.ToolRegistry.execute")
    @patch("app.services.ai.agent_service.chat", new_callable=AsyncMock)
    async def test_tool_failure_returns_safe_message(
        self,
        chat,
        execute,
        build_prompt,
        initialize,
        get_context,
        update_context,
    ):
        execute.return_value = {
            "ok": False,
            "error": "Unable to retrieve your wallet right now.",
        }

        result = await self._process("What is my balance?")

        self.assertEqual(
            result["message"],
            "Unable to retrieve your wallet right now.",
        )
        chat.assert_not_called()

    @patch(
        "app.services.ai.agent_service.SessionManager.update_context"
    )
    @patch(
        "app.services.ai.agent_service.SessionManager.context",
        return_value={"agent": {"history": []}},
    )
    @patch(
        "app.services.ai.agent_service.SessionManager.initialize"
    )
    @patch(
        "app.services.ai.agent_service.ContextBuilder.build_system_prompt",
        new_callable=AsyncMock,
        return_value="test system prompt",
    )
    @patch("app.services.ai.agent_service.ToolRegistry.execute")
    @patch("app.services.ai.agent_service.chat", new_callable=AsyncMock)
    async def test_balance_exchange_is_added_to_history(
        self,
        chat,
        execute,
        build_prompt,
        initialize,
        get_context,
        update_context,
    ):
        execute.return_value = {
            "ok": True,
            "wallet_found": True,
            "balance": "25.00",
            "currency": "ZAR",
        }

        result = await self._process("Check my balance")

        history = result["context_update"]["agent"]["history"]
        self.assertEqual(len(history), 2)
        self.assertEqual(
            history[0],
            {"role": "user", "content": "Check my balance"},
        )
        self.assertEqual(
            history[1],
            {
                "role": "assistant",
                "content": "Your available wallet balance is R25.00.",
            },
        )


if __name__ == "__main__":
    unittest.main()
