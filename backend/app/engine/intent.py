# backend/app/engine/intent.py

from typing import Any, Dict, Optional


# ============================================================================
# PUBLIC API
# ============================================================================

def detect_intent(
    text: str,
    session: Any = None,
) -> Dict[str, Any]:
    """
    Detect the user's high-level intent.

    This layer ONLY determines what the user wants.

    It does NOT:
        - route requests
        - execute business logic
        - modify session state
        - access the database
        - perform transactions

    FlowRouter is responsible for routing the detected intent
    to the appropriate engine.
    """

    text = (text or "").strip().lower()

    if not text:
        return _unknown()

    # =========================================================================
    # CONVERSATION
    # =========================================================================

    if text in {
        "hi",
        "hello",
        "hey",
        "morning",
        "good morning",
        "good afternoon",
        "good evening",
        "ndeipi",
        "howzit",
        "how are you",
    }:
        return _intent(
            "conversation.greeting",
            "conversation",
            "greeting",
        )

    # -------------------------------------------------------------------------
    # HELP
    # -------------------------------------------------------------------------

    if text in {
        "help",
        "menu",
        "?",
        "commands",
        "options",
        "what can you do",
    }:
        return _intent(
            "conversation.help",
            "conversation",
            "help",
        )

    # -------------------------------------------------------------------------
    # GOODBYE
    # -------------------------------------------------------------------------

    if text in {
        "bye",
        "goodbye",
        "good bye",
        "see you",
        "see you later",
        "later",
        "thanks bye",
    }:
        return _intent(
            "conversation.goodbye",
            "conversation",
            "goodbye",
        )

    # =========================================================================
    # SUPPORT / HUMAN AGENT
    # =========================================================================

    if text in {
        "agent",
        "human",
        "support",
        "customer service",
        "customer support",
        "human agent",
        "speak to an agent",
        "talk to an agent",
        "talk to human",
        "talk to a human",
        "speak to human",
        "speak to a human",
    }:
        return _intent(
            "support.agent",
            "support",
            "agent",
        )

    if any(
        phrase in text
        for phrase in {
            "human agent",
            "speak to an agent",
            "talk to an agent",
            "customer service",
            "customer support",
            "talk to human",
            "speak to human",
        }
    ):
        return _intent(
            "support.agent",
            "support",
            "agent",
        )

    # =========================================================================
    # ACCOUNT / PROFILE
    # =========================================================================

    if text in {
        "profile",
        "my profile",
        "account",
        "my account",
        "account details",
        "account information",
        "my details",
        "personal details",
        "show profile",
        "show my profile",
        "show account",
        "show my account",
    }:
        return _intent(
            "account.profile",
            "account",
            "profile",
        )

    # -------------------------------------------------------------------------
    # ONBOARDING
    # -------------------------------------------------------------------------

    if text in {
        "onboard",
        "onboarding",
        "register",
        "registration",
        "sign up",
        "signup",
        "create account",
        "open account",
        "get started",
        "start account",
        "new account",
    }:
        return _intent(
            "account.onboard",
            "account",
            "onboard",
        )

    # =========================================================================
    # KYC
    # =========================================================================

    if text in {
        "kyc",
        "verify",
        "verify me",
        "verify my identity",
        "verify identity",
        "identity verification",
        "verification",
        "complete kyc",
        "start kyc",
    }:
        return _intent(
            "kyc.start",
            "kyc",
            "start",
        )

    if any(
        phrase in text
        for phrase in {
            "verify me",
            "verify my identity",
            "verify identity",
            "identity verification",
            "complete kyc",
            "start kyc",
        }
    ):
        return _intent(
            "kyc.start",
            "kyc",
            "start",
        )

    # =========================================================================
    # WALLET
    # =========================================================================

    # -------------------------------------------------------------------------
    # Wallet view
    # -------------------------------------------------------------------------

    if text in {
        "wallet",
        "my wallet",
        "show wallet",
        "open wallet",
        "wallet details",
        "wallet information",
        "wallet status",
    }:
        return _intent(
            "wallet.view",
            "wallet",
            "view",
        )

    # -------------------------------------------------------------------------
    # Explicit wallet creation
    # -------------------------------------------------------------------------

    if text in {
        "create wallet",
        "create my wallet",
        "new wallet",
    }:
        return _intent(
            "wallet.create",
            "wallet",
            "create",
        )

    # =========================================================================
    # CONTRIBUTIONS
    # =========================================================================

    if text in {
        "contribute",
        "contribution",
        "contributions",
        "make a contribution",
        "make contribution",
        "add contribution",
        "pay contribution",
        "make a payment",
        "make payment",
        "save money",
        "start saving",
        "save",
        "deposit",
    }:
        return _intent(
            "contribution.start",
            "contribution",
            "start",
        )

    # =========================================================================
    # STOKVEL
    # =========================================================================

    if text in {
        "stokvel",
        "stokvels",
        "my stokvel",
        "my stokvels",
        "show stokvel",
        "show stokvels",
        "show my stokvel",
        "show my stokvels",
        "view stokvel",
        "view stokvels",
    }:
        return _intent(
            "stokvel.view",
            "stokvel",
            "view",
        )

    # -------------------------------------------------------------------------
    # Create stokvel
    # -------------------------------------------------------------------------

    if text in {
        "create stokvel",
        "create a stokvel",
        "start stokvel",
        "start a stokvel",
        "new stokvel",
        "i want to create a stokvel",
        "i want to start a stokvel",
    }:
        return _intent(
            "stokvel.create",
            "stokvel",
            "create",
        )

    #----------------------------------------------------------------------------
    # Join stokvel
    #----------------------------------------------------------------------------

    if text in {
        "join",
        "how do i join",
        "i want to join",
        "i want to join a stokvel",
        "join stokvel",
        "join a stokvel",
        "how do i join a stokvel",
        "how can i join a stokvel",
    }:
        return _intent(
            "stokvel.join",
            "stokvel",
            "join",
        )

    # =========================================================================
    # PORTFOLIO
    # =========================================================================

    if text in {
        "portfolio",
        "my portfolio",
        "show portfolio",
        "view portfolio",
        "my investments",
        "my investment",
        "investment portfolio",
        "show investments",
        "show my investments",
        "investments",
    }:
        return _intent(
            "portfolio.view",
            "portfolio",
            "view",
        )

    #==========================================================================
    # BALANCE
    #==========================================================================

    if text in {
        "balance",
        "my balance",
        "check balance",
        "wallet balance",
    }:
        return {
            "intent": "wallet.balance",
            "domain": "wallet",
            "action": "balance",
            "parameters": {},
        }

    # =========================================================================
    # PIG / AGRICULTURAL INVESTMENT
    # =========================================================================

    # -------------------------------------------------------------------------
    # Buy pig
    # -------------------------------------------------------------------------

    if _starts_with_command(text, "buy"):
        return _intent(
            "pig.buy",
            "investment",
            "buy",
            amount=_extract_number(text),
        )

    # -------------------------------------------------------------------------
    # Sell pig
    # -------------------------------------------------------------------------

    if _starts_with_command(text, "sell"):
        return _intent(
            "pig.sell",
            "investment",
            "sell",
            pig_id=_extract_integer(text),
        )

    # -------------------------------------------------------------------------
    # Pig health
    # -------------------------------------------------------------------------

    if _starts_with_command(text, "health"):
        return _intent(
            "pig.health",
            "investment",
            "health",
            pig_id=_extract_integer(text),
        )

    # -------------------------------------------------------------------------
    # View pigs
    # -------------------------------------------------------------------------

    if text in {
        "pig",
        "pigs",
        "my pigs",
        "show pigs",
        "show my pigs",
        "view pigs",
        "pig portfolio",
    }:
        return _intent(
            "pig.view",
            "investment",
            "view",
        )

    # =========================================================================
    # CONFIRMATION
    # =========================================================================

    if text in {
        "1",
        "yes",
        "y",
        "confirm",
        "confirmed",
        "ok",
        "okay",
        "proceed",
        "continue",
    }:
        return _intent(
            "conversation.confirm",
            "conversation",
            "confirm",
        )

    # =========================================================================
    # CANCELLATION
    # =========================================================================

    if text in {
        "2",
        "no",
        "n",
        "cancel",
        "cancelled",
        "stop",
        "abort",
        "never mind",
        "nevermind",
    }:
        return _intent(
            "conversation.cancel",
            "conversation",
            "cancel",
        )

    # =========================================================================
    # NUMERIC VALUE INPUT
    # =========================================================================

    if text.isdigit():

        return _intent(
            "conversation.provide_value",
            "conversation",
            "provide_value",
            value=int(text),
        )

    # =========================================================================
    # DECIMAL VALUE INPUT
    # =========================================================================

    number = _extract_number(text)

    if number is not None and _looks_like_numeric_input(text):

        return _intent(
            "conversation.provide_value",
            "conversation",
            "provide_value",
            value=number,
        )

    # =========================================================================
    # UNKNOWN
    # =========================================================================

    return _unknown()


# ============================================================================
# INTENT BUILDER
# ============================================================================

def _intent(
    name: str,
    domain: str,
    action: str,
    **parameters: Any,
) -> Dict[str, Any]:
    """
    Create a normalized intent object.
    """

    return {
        "intent": name,
        "domain": domain,
        "action": action,
        "parameters": parameters,
    }


# ============================================================================
# UNKNOWN
# ============================================================================

def _unknown() -> Dict[str, Any]:
    """
    Return a normalized unknown intent.
    """

    return {
        "intent": "conversation.unknown",
        "domain": "conversation",
        "action": "unknown",
        "parameters": {},
    }


# ============================================================================
# COMMAND HELPERS
# ============================================================================

def _starts_with_command(
    text: str,
    command: str,
) -> bool:
    """
    Check whether the first word is a command.
    """

    parts = text.split()

    return bool(parts) and parts[0] == command


def _extract_integer(
    text: str,
) -> Optional[int]:
    """
    Extract the first integer from text.

    Example:

        'sell 12' -> 12
        'health 5' -> 5
    """

    for part in text.split():

        if part.isdigit():

            return int(part)

    return None


def _extract_number(
    text: str,
) -> Optional[float]:
    """
    Extract the first numeric value from text.

    Supports:

        100
        100.50
        R100
        R100.50
        1,000
        R1,000.50
    """

    cleaned_parts = []

    for part in text.split():

        cleaned = (
            part
            .replace("r", "")
            .replace("R", "")
            .replace(",", "")
        )

        try:

            value = float(cleaned)

            return value

        except ValueError:

            cleaned_parts.append(part)

    return None


def _looks_like_numeric_input(
    text: str,
) -> bool:
    """
    Determine whether the entire message is essentially
    a numeric value.

    This prevents normal sentences containing numbers
    from being interpreted as monetary input.
    """

    cleaned = (
        text
        .replace("r", "")
        .replace("R", "")
        .replace(",", "")
        .strip()
    )

    try:

        float(cleaned)

        return True

    except ValueError:

        return False
