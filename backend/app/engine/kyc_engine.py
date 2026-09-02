from datetime import datetime
from typing import Dict, Any

from app.services.identity.session_manager import SessionManager


class KYC:
    """
    Handles KYC conversation flow.

    Session state is managed exclusively through SessionManager.
    Actual identity verification/compliance belongs in services.
    """

    @classmethod
    async def handle(
        self,
        message: str,
        intent: Dict[str, Any],
        session_context: Dict[str, Any],
        member_context: Dict[str, Any],
    ) -> Dict[str, Any]:

        message_lower = (message or "").lower().strip()

        context = SessionManager.context(session)
        kyc_context = context.get("kyc") or {}

        # --------------------------------------------------------------
        # ACTIVE KYC FLOW
        # --------------------------------------------------------------

        if kyc_context.get("active"):
            return cls._handle_kyc_flow(
                session,
                message,
            )

        # --------------------------------------------------------------
        # KYC COMMANDS
        # --------------------------------------------------------------

        if message_lower in {
            "kyc",
            "verify",
            "identity",
        }:
            return cls._start_kyc_flow(session)

        if message_lower == "kyc status":
            return cls._get_kyc_status(session)

        return {
            "message": (
                "*KYC Commands*\n\n"
                "• KYC - Start identity verification\n"
                "• KYC STATUS - Check your verification status\n\n"
                "We need to verify your identity for compliance."
            ),
            "type": "text",
            "context_update": {},
        }

    # ==================================================================
    # START
    # ==================================================================

    @classmethod
    def _start_kyc_flow(cls, session) -> Dict[str, Any]:

        SessionManager.start_kyc(
            session,
            step="full_name",
        )

        SessionManager.update_context(
            session,
            {
                "kyc": {
                    "active": True,
                    "step": "full_name",
                    "verified": False,
                }
            },
        )

        return {
            "message": (
                "*Identity Verification*\n\n"
                "Let's verify your identity. "
                "This is required for compliance.\n\n"
                "What is your full name as it appears on your ID?"
            ),
            "type": "text",
            "context_update": {
                "kyc": {
                    "active": True,
                    "step": "full_name",
                }
            },
        }

    # ==================================================================
    # ACTIVE FLOW
    # ==================================================================

    @classmethod
    def _handle_kyc_flow(
        cls,
        session,
        message: str,
    ) -> Dict[str, Any]:

        context = SessionManager.context(session)
        kyc_context = context.get("kyc") or {}

        step = kyc_context.get("step", "full_name")

        message = (message or "").strip()
        message_lower = message.lower()

        # --------------------------------------------------------------
        # CANCEL
        # --------------------------------------------------------------

        if message_lower in {
            "back",
            "exit",
            "cancel",
        }:

            SessionManager.finish_kyc(session)

            return {
                "message": (
                    "KYC verification cancelled.\n\n"
                    "Type *KYC* to start again."
                ),
                "type": "text",
                "context_update": {
                    "kyc": {
                        "active": False,
                    }
                },
            }

        # --------------------------------------------------------------
        # FULL NAME
        # --------------------------------------------------------------

        if step == "full_name":

            if not message:
                return {
                    "message": (
                        "Please enter your full name "
                        "as it appears on your ID."
                    ),
                    "type": "text",
                    "context_update": {},
                }

            SessionManager.update_context(
                session,
                {
                    "kyc": {
                        "active": True,
                        "step": "id_number",
                        "full_name": message,
                    }
                },
            )

            return {
                "message": (
                    f"Thank you, {message}.\n\n"
                    "Please enter your ID number "
                    "(e.g., 9201025671082):"
                ),
                "type": "text",
                "context_update": {
                    "kyc": {
                        "active": True,
                        "step": "id_number",
                    }
                },
            }

        # --------------------------------------------------------------
        # ID NUMBER
        # --------------------------------------------------------------

        if step == "id_number":

            if not message:
                return {
                    "message": "Please enter your ID number.",
                    "type": "text",
                    "context_update": {},
                }

            SessionManager.update_context(
                session,
                {
                    "kyc": {
                        "active": True,
                        "step": "phone",
                        "id_number": message,
                    }
                },
            )

            return {
                "message": (
                    "Please enter your phone number "
                    "(e.g., 0712345678):"
                ),
                "type": "text",
                "context_update": {
                    "kyc": {
                        "active": True,
                        "step": "phone",
                    }
                },
            }

        # --------------------------------------------------------------
        # PHONE
        # --------------------------------------------------------------

        if step == "phone":

            if not message:
                return {
                    "message": "Please enter your phone number.",
                    "type": "text",
                    "context_update": {},
                }

            SessionManager.update_context(
                session,
                {
                    "kyc": {
                        "active": True,
                        "step": "confirm",
                        "phone": message,
                    }
                },
            )

            context = SessionManager.context(session)
            kyc_context = context.get("kyc") or {}

            return {
                "message": (
                    "*Please confirm your details*\n\n"
                    f"Name: {kyc_context.get('full_name', '')}\n"
                    f"ID Number: {kyc_context.get('id_number', '')}\n"
                    f"Phone: {kyc_context.get('phone', '')}\n\n"
                    "Reply *CONFIRM* to submit "
                    "or *CANCEL* to start over."
                ),
                "type": "text",
                "context_update": {
                    "kyc": {
                        "active": True,
                        "step": "confirm",
                    }
                },
            }

        # --------------------------------------------------------------
        # CONFIRM
        # --------------------------------------------------------------

        if step == "confirm":

            if message_lower in {
                "confirm",
                "yes",
                "y",
                "1",
            }:

                completed_at = datetime.utcnow().isoformat()

                SessionManager.update_context(
                    session,
                    {
                        "kyc": {
                            "active": False,
                            "step": None,
                            "verified": True,
                            "completed_at": completed_at,
                        }
                    },
                )

                return {
                    "message": (
                        "*KYC Verification Complete!*\n\n"
                        "Your identity has been submitted successfully.\n"
                        "You now have access to features requiring "
                        "identity verification."
                    ),
                    "type": "text",
                    "context_update": {
                        "kyc": {
                            "active": False,
                            "verified": True,
                        }
                    },
                }

            if message_lower in {
                "cancel",
                "no",
                "n",
                "2",
            }:

                SessionManager.update_context(
                    session,
                    {
                        "kyc": {
                            "active": True,
                            "step": "full_name",
                            "full_name": None,
                            "id_number": None,
                            "phone": None,
                        }
                    },
                )

                return {
                    "message": (
                        "Let's start over.\n\n"
                        "What is your full name as it appears "
                        "on your ID?"
                    ),
                    "type": "text",
                    "context_update": {
                        "kyc": {
                            "active": True,
                            "step": "full_name",
                        }
                    },
                }

            return {
                "message": (
                    "Please reply *CONFIRM* to submit "
                    "or *CANCEL* to start over."
                ),
                "type": "text",
                "context_update": {},
            }

        # --------------------------------------------------------------
        # UNKNOWN STEP
        # --------------------------------------------------------------

        SessionManager.start_kyc(
            session,
            step="full_name",
        )

        return {
            "message": (
                "Let's restart your KYC verification.\n\n"
                "What is your full name as it appears on your ID?"
            ),
            "type": "text",
            "context_update": {
                "kyc": {
                    "active": True,
                    "step": "full_name",
                }
            },
        }

    # ==================================================================
    # STATUS
    # ==================================================================

    @classmethod
    def _get_kyc_status(cls, session) -> Dict[str, Any]:

        context = SessionManager.context(session)
        kyc_context = context.get("kyc") or {}

        if kyc_context.get("verified"):

            return {
                "message": (
                    "*KYC Status: Verified*\n\n"
                    "Your identity has been verified.\n"
                    f"Verified on: "
                    f"{kyc_context.get('completed_at', 'Unknown')}"
                ),
                "type": "text",
                "context_update": {},
            }

        return {
            "message": (
                "*KYC Status: Not Verified*\n\n"
                "Please complete KYC verification "
                "to access all features.\n\n"
                "Type *KYC* to start the verification process."
            ),
            "type": "text",
            "context_update": {},
        }
