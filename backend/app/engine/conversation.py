# backend/app/engine/conversation.py

from typing import Any, Dict


class ConversationManager:
    """
    Handles conversation-level intents.

    Responsibilities:
        - Greeting
        - Help / menu
        - Goodbye
        - Unknown commands
        - Generic conversation responses

    This class does NOT:
        - modify session state
        - access the database
        - execute transactions
        - manage wallets
        - manage stokvels
        - manage investments
        - manage KYC

    FlowRouter is responsible for deciding which engine should
    handle stateful actions such as confirm/cancel.
    """

    # ========================================================================
    # MAIN HANDLER
    # ========================================================================

    @classmethod
    async def handle(
        self,
        message: str,
        intent: Dict[str, Any],
        session_context: Dict[str, Any],
        member_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Handle a conversation intent.

        Returns a normalized engine response:

            {
                "message": "...",
                "type": "text",
                "context_update": {}
            }
        """

        intent_name = intent.get("intent")

        # --------------------------------------------------------------------
        # Greeting
        # --------------------------------------------------------------------

        if intent_name == "conversation.greeting":
            return cls.greeting()

        # --------------------------------------------------------------------
        # Help
        # --------------------------------------------------------------------

        if intent_name == "conversation.help":
            return cls.help()

        # --------------------------------------------------------------------
        # Goodbye
        # --------------------------------------------------------------------

        if intent_name == "conversation.goodbye":
            return cls.goodbye()

        # --------------------------------------------------------------------
        # Unknown
        # --------------------------------------------------------------------

        if intent_name == "conversation.unknown":
            return cls.unknown(message)

        # --------------------------------------------------------------------
        # Confirmation
        #
        # Confirmation is intentionally NOT executed here.
        #
        # FlowRouter should determine which active engine owns the
        # confirmation.
        # --------------------------------------------------------------------

        if intent_name == "conversation.confirm":
            return cls.confirm()

        # --------------------------------------------------------------------
        # Cancellation
        #
        # Cancellation is also intentionally NOT executed here.
        #
        # FlowRouter should determine which active engine owns the
        # cancellation.
        # --------------------------------------------------------------------

        if intent_name == "conversation.cancel":
            return cls.cancel()

        # --------------------------------------------------------------------
        # Value input without an active flow
        # --------------------------------------------------------------------

        if intent_name == "conversation.provide_value":
            return cls.provide_value(intent)

        # --------------------------------------------------------------------
        # Fallback
        # --------------------------------------------------------------------

        return cls.unknown(message)

    # ========================================================================
    # GREETING
    # ========================================================================

    @staticmethod
    def greeting() -> Dict[str, Any]:
        """
        Handle a greeting.
        """

        return {
            "message": (
                "Hi! 👋 Welcome to Warima.\n\n"
                "I can help you save, manage your wallet, "
                "manage stokvels and invest.\n\n"
                "Type *Help* to see what you can do."
            ),
            "type": "text",
            "context_update": {},
        }

    # ========================================================================
    # HELP
    # ========================================================================

    @staticmethod
    def help() -> Dict[str, Any]:
        """
        Display available Warima commands.
        """

        return {
            "message": (
                "*Warima Help*\n\n"

                "*Wallet & Saving*\n"
                "• Wallet\n"
                "• Balance\n"
                "• Contribute\n\n"

                "*Stokvel*\n"
                "• Stokvel\n"
                "• Create stokvel\n"
                "• Join stokvel\n\n"

                "*Investments*\n"
                "• Portfolio\n"
                "• Pigs\n"
                "• Buy 1500\n"
                "• Sell 1\n"
                "• Health 1\n\n"

                "*Account*\n"
                "• Profile\n"
                "• KYC\n\n"

                "*Support*\n"
                "• Agent\n\n"

                "*Other*\n"
                "• Cancel\n"
                "• Help"
            ),
            "type": "text",
            "context_update": {},
        }

    # ========================================================================
    # GOODBYE
    # ========================================================================

    @staticmethod
    def goodbye() -> Dict[str, Any]:
        """
        Handle goodbye messages.
        """

        return {
            "message": (
                "Goodbye! 👋\n\n"
                "I'll be here whenever you're ready."
            ),
            "type": "text",
            "context_update": {},
        }

    # ========================================================================
    # CONFIRM
    # ========================================================================

    @staticmethod
    def confirm() -> Dict[str, Any]:
        """
        Generic confirmation fallback.

        A confirmation should normally be intercepted by FlowRouter
        and sent to the active engine.

        This response is only used when there is no active flow.
        """

        return {
            "message": (
                "There is nothing waiting for confirmation.\n\n"
                "Type *Help* to see what you can do."
            ),
            "type": "text",
            "context_update": {},
        }

    # ========================================================================
    # CANCEL
    # ========================================================================

    @staticmethod
    def cancel() -> Dict[str, Any]:
        """
        Generic cancellation fallback.

        A cancellation should normally be intercepted by FlowRouter
        and sent to the active engine.

        This response is only used when there is no active flow.
        """

        return {
            "message": (
                "There is nothing to cancel.\n\n"
                "Type *Help* to see what you can do."
            ),
            "type": "text",
            "context_update": {},
        }

    # ========================================================================
    # VALUE INPUT
    # ========================================================================

    @staticmethod
    def provide_value(
        intent: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Handle a numeric value when no active flow has claimed it.

        Example:

            User: 100

        If the wallet engine is active, FlowRouter should send this
        to WalletEngine instead.

        If no flow is active, this method provides the fallback.
        """

        parameters = intent.get(
            "parameters",
            {},
        )

        value = parameters.get("value")

        if value is None:

            return {
                "message": (
                    "Please enter a valid number."
                ),
                "type": "text",
                "context_update": {},
            }

        return {
            "message": (
                f"I received *R{value:,.2f}*, but there is no "
                "active contribution.\n\n"
                "Type *Contribute* to start a contribution."
            ),
            "type": "text",
            "context_update": {},
        }

    # ========================================================================
    # UNKNOWN
    # ========================================================================

    @staticmethod
    def unknown(
        message: str = "",
    ) -> Dict[str, Any]:
        """
        Handle an unknown command.
        """

        message = (message or "").strip()

        if message:

            response = (
                f"I didn't understand *{message}*.\n\n"
                "Type *Help* to see available commands."
            )

        else:

            response = (
                "I didn't understand that.\n\n"
                "Type *Help* to see available commands."
            )

        return {
            "message": response,
            "type": "text",
            "context_update": {},
        }

    # ========================================================================
    # STATIC CONTEXT UPDATE
    # ========================================================================

    @staticmethod
    def no_context_update() -> Dict[str, Any]:
        """
        Standard empty context update.

        Useful when another engine expects a normalized response.
        """

        return {
            "context_update": {},
        }
