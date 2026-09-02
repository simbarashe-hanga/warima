from datetime import datetime
from typing import Dict

from app.services.identity.session_manager import SessionManager


class KYC:
    """
    Handles KYC conversation flow.

    Actual KYC verification and compliance checks belong
    in dedicated services.
    """

    @classmethod
    def process(
        cls,
        session: Dict,
        message: str,
    ) -> Dict:

        message_lower = (
            message.lower().strip()
        )

        context = SessionManager.context(session)
        kyc_context = context.get("kyc", {})

        if kyc_context.get("active"):
            return cls._handle_kyc_flow(
                session,
                message,
            )

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
                "🔐 *KYC Commands*\n\n"
                "• KYC - Start identity verification\n"
                "• KYC STATUS - Check your verification status\n\n"
                "We need to verify your identity for compliance."
            ),
            "context_update": {},
        }

    # ==================================================================
    # START
    # ==================================================================

    @classmethod
    def _start_kyc_flow(cls, session):

        SessionManager.start_kyc(
            session,
            step="full_name",
        )

        return {
            "message": (
                "🔐 *Identity Verification*\n\n"
                "Let's verify your identity. "
                "This is required for compliance.\n\n"
                "What is your full name as it appears on your ID?"
            ),
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
        message,
    ):

        context = SessionManager.context(session)
        kyc_context = context.get("kyc", {})

        step = kyc_context.get(
            "step",
            "full_name",
        )

        message_lower = message.lower().strip()

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
                    "KYC verification cancelled. "
                    "Type KYC to start again."
                ),
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

            SessionManager.update_kyc_context(
                session,
                {
                    "active": True,
                    "step": "id_number",
                    "full_name": message.strip(),
                },
            )

            return {
                "message": (
                    f"Thank you, {message}.\n\n"
                    "Please enter your ID number."
                ),
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

            SessionManager.update_kyc_context(
                session,
                {
                    "active": True,
                    "step": "phone",
                    "id_number": message.strip(),
                },
            )

            return {
                "message": (
                    "Please enter your phone number."
                ),
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

            SessionManager.update_kyc_context(
                session,
                {
                    "active": True,
                    "step": "confirm",
                    "phone": message.strip(),
                },
            )

            updated = SessionManager.context(session)
            data = updated["kyc"]

            return {
                "message": (
                    "✅ *Please confirm your details*\n\n"
                    f"Name: {data.get('full_name', '')}\n"
                    f"ID Number: {data.get('id_number', '')}\n"
                    f"Phone: {data.get('phone', '')}\n\n"
                    "Reply CONFIRM to submit or CANCEL to start over."
                ),
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
                "1",
            }:

                SessionManager.update_kyc_context(
                    session,
                    {
                        "active": False,
                        "step": None,
                        "verified": True,
                        "completed_at": (
                            datetime.now().isoformat()
                        ),
                    },
                )

                return {
                    "message": (
                        "🎉 *KYC Verification Complete!*\n\n"
                        "Your identity verification has been submitted "
                        "successfully."
                    ),
                    "context_update": {
                        "kyc": {
                            "active": False,
                            "verified": True,
                        }
                    },
                }

            SessionManager.start_kyc(
                session,
                step="full_name",
            )

            return {
                "message": (
                    "Let's start over.\n\n"
                    "What is your full name as it appears on your ID?"
                ),
                "context_update": {
                    "kyc": {
                        "active": True,
                        "step": "full_name",
                    }
                },
            }

        return {
            "message": (
                "I didn't understand that. "
                "Please follow the prompts."
            ),
            "context_update": {},
        }

    # ==================================================================
    # STATUS
    # ==================================================================

    @classmethod
    def _get_kyc_status(cls, session):

        context = SessionManager.context(session)
        kyc_context = context.get("kyc", {})

        if kyc_context.get("verified"):

            return {
                "message": (
                    "✅ *KYC Status: Verified*\n\n"
                    "Your identity has been verified.\n"
                    f"Verified on: "
                    f"{kyc_context.get('completed_at', 'Unknown')}"
                ),
                "context_update": {},
            }

        return {
            "message": (
                "⚠️ *KYC Status: Not Verified*\n\n"
                "Please complete KYC verification to access "
                "all features.\n"
                "Type KYC to start the verification process."
            ),
            "context_update": {},
        }
