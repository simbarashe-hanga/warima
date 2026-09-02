# backend/app/services/ai/agent_service.py

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
