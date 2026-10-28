# backend/app/services/ai/agent_service.py

import re

from decimal import Decimal, InvalidOperation
from app.services.ai.tools.tool_registry import ToolRegistry

from app.services.ai.context_builder import ContextBuilder
from app.services.ai.llm_service import chat
from app.services.identity.session_manager import SessionManager


class AgentService:
    """
    Warima AI Agent service.

    Responsibilities:
        - Build trusted member context
        - Build the Warima system prompt
        - Maintain AI conversation history
        - Send messages to the configured LLM
        - Return a standardized response

    Non-responsibilities:
        - Intent detection
        - Flow routing
        - Database commits
        - WhatsApp communication
        - Payment processing
        - Blockchain operations
    """

    def __init__(self):
        """
        AgentService is intentionally stateless.

        User-specific state belongs to UserSession and is supplied
        to process().
        """
        pass

    @staticmethod
    def _detect_tool_intent(message: str) -> str | None:
        text = (message or "").lower().strip()
        text = re.sub(r"[^\w\s']", "", text)
        text = re.sub(r"\s+", " ", text)

        balance_phrases = {
            "balance",
            "my balance",
            "check balance",
            "check my balance",
            "show my balance",
            "show me my balance",
            "tell me my balance",
            "what is my balance",
            "what's my balance",
            "whats my balance",
            "what is my wallet balance",
            "what's my wallet balance",
            "whats my wallet balance",
            "how much money do i have",
            "how much do i have in my wallet",
            "how much is in my wallet",
            "what is in my wallet",
            "what's in my wallet",
            "whats in my wallet",
            "i want to check my balance",
            "i want to know my balance",
            "can you check my balance",
            "please check my balance",
        }

        if text in balance_phrases:
            return "wallet_balance"

        return None

    @staticmethod
    def _format_tool_response(tool_name: str, result: dict) -> str:
        if not result.get("ok"):
            return result.get(
                "error",
                "I couldn't retrieve that information right now.",
            )

        if tool_name == "wallet_balance":
            if not result.get("wallet_found"):
                return result.get(
                    "message",
                    "No wallet was found for your account.",
                )

            try:
                amount = Decimal(result["balance"])
                formatted_amount = f"{amount:,.2f}"
            except (KeyError, ValueError, TypeError, InvalidOperation):
                return "I couldn't retrieve your balance right now."

            currency = result.get("currency")

            if currency == "ZAR":
                return f"Your available wallet balance is R{formatted_amount}."

            if not currency:
                return "I couldn't retrieve your balance right now."

            return (
                f"Your available wallet balance is "
                f"{currency} {formatted_amount}."
            )

        return "I couldn't retrieve that information right now."

    # ==================================================================
    # PROCESS MESSAGE
    # ==================================================================

    async def process(
        self,
        user,
        identity,
        session,
        member_account,
        message: str,
        db=None,
    ) -> dict:

        # --------------------------------------------------------------
        # Ensure session context exists
        # --------------------------------------------------------------

        SessionManager.initialize(session)

        # --------------------------------------------------------------
        # Activate AI Agent mode
        # --------------------------------------------------------------

        SessionManager.update_context(
            session,
            {
                "agent": {
                    "active": True,
                    "step": "chatting",
                }
            },
        )

        # --------------------------------------------------------------
        # Build trusted member context
        # --------------------------------------------------------------

        system_prompt = await ContextBuilder.build_system_prompt(
            user=user,
            identity=identity,
            session=session,
            member_account=member_account,
        )

        # --------------------------------------------------------------
        # Get conversation history
        # --------------------------------------------------------------

        context = SessionManager.context(session)

        agent_context = context.get("agent") or {}

        history = agent_context.get(
            "history",
            [],
        )

        if not isinstance(history, list):
            history = []

        # --------------------------------------------------------------
        # Send message to LLM
        # --------------------------------------------------------------

        # --------------------------------------------------------------
        # Allowlisted tool dispatch
        # --------------------------------------------------------------

        tool_name = self._detect_tool_intent(message)

        if tool_name:
            tool_result = ToolRegistry.execute(
                tool_name,
                db=db,
                member_account=member_account,
            )

            response = self._format_tool_response(
                tool_name,
                tool_result,
            )

        else:
            # ----------------------------------------------------------
            # Ordinary conversation: use the configured LLM
            # ----------------------------------------------------------

            print("=" * 70)
            print("AI AGENT")
            print("MESSAGE:", message)
            print("HISTORY COUNT:", len(history))
            print("=" * 70)

            response = await chat(
                user_message=message,
                history=history,
                system_prompt=system_prompt,
            )

            response = (response or "").strip()

        # --------------------------------------------------------------
        # Fallback
        # --------------------------------------------------------------

        if not response:

            response = (
                "I'm sorry, I wasn't able to process that. "
                "Please try again."
            )

        # --------------------------------------------------------------
        # Add current exchange to history
        # --------------------------------------------------------------

        history.append(
            {
                "role": "user",
                "content": message,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        # --------------------------------------------------------------
        # Limit history
        # --------------------------------------------------------------

        history = history[-20:]

        # --------------------------------------------------------------
        # Persist agent context
        # --------------------------------------------------------------

        SessionManager.update_context(
            session,
            {
                "agent": {
                    "active": True,
                    "step": "chatting",
                    "history": history,
                }
            },
        )

        # --------------------------------------------------------------
        # Return standardized response
        # --------------------------------------------------------------

        return {
            "message": response,
            "type": "text",
            "context_update": {
                "agent": {
                    "active": True,
                    "step": "chatting",
                    "history": history,
                }
            },
        }

    # ==================================================================
    # EXIT AGENT
    # ==================================================================

    def exit(self, session):

        context = SessionManager.context(session)

        agent = dict(
            context.get("agent") or {}
        )

        agent["active"] = False
        agent["step"] = None

        SessionManager.update_context(
            session,
            {
                "agent": agent,
            },
        )

        return {
            "message": "You have left the Warima AI Agent.",
            "type": "text",
            "context_update": {
                "agent": agent,
            },
        }
