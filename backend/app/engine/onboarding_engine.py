from typing import Any, Dict

from app.engine.onboarding_steps import OnboardingStep
from app.engine import onboarding_messages as msg

from app.schemas.onboarding import OnboardingResult
from app.services.identity.session_manager import SessionManager



class OnboardingEngine:
    """
    Handles the onboarding conversation flow.

    User persistance belongs outside this engine.
    The engine only coordinates onboarding state and user fields.
    """


    @classmethod
    async def handle(
        cls,
        message: str,
        intent: Dict[str, Any],
        session: Dict[str, Any],
        member_context: Dict[str, Any],
    ) -> OnboardingResult:

        context = SessionManager.context(session)

        onboarding = context["onboarding"]

        step = onboarding.get(
            "step",
            OnboardingStep.WELCOME,
        )

        print("=" * 70)
        print("ONBOARDING ENGINE")
        print("STEP:", step)
        print("MESSAGE:", message)
        print("=" * 70)

        if step == OnboardingStep.WELCOME:
            return cls._welcome(session)

        if step == OnboardingStep.FIRST_NAME:
            return cls._first_name(session, message)

        if step == OnboardingStep.LAST_NAME:
            return cls._last_name(session, message)

        if step == OnboardingStep.DISPLAY_NAME:
            return cls._display_name(session, message)

        if step == OnboardingStep.LANGUAGE:
            return cls._language(session, message)

        if step == OnboardingStep.EMAIL:
            return cls._email(session, message)

        if step == OnboardingStep.CONFIRM:
            return cls._confirm(session, message)

        #-------------------------------------------------------------------------
        # UNKNOWN STATE
        #-------------------------------------------------------------------------

        print(
            "ONBOARDING ENGINE: "
            "Unknown onboarding step:",
            step,
        )

        cls._reset_onboarding(session)

        return OnboardingResult(
            message=(
                "Let's start again.\n\n"
                + msg.FIRST_NAME
            ),
            completed=False,
            next_step=OnboardingStep.FIRST_NAME,
        )

    @staticmethod
    def _welcome(session) -> OnboardingResult:

        context = SessionManager.context(session)

        onboarding = context["onboarding"]

        onboarding["active"] = True

        onboarding["step"] = OnboardingStep.FIRST_NAME

        return OnboardingResult(
            message=msg.WELCOME + "\n\n" + msg.FIRST_NAME,
            completed=False,
            next_step=OnboardingStep.FIRST_NAME,
        )

    @staticmethod
    def _first_name(
        session,
        message: str,
    ) -> OnboardingResult:

        value = message.strip()

        if not value:
            return OnboardingResult(
                message="Please enter your first name.",
                completed=False,
                next_step=OnboardingStep.FIRST_NAME,
            )

        context = SessionManager.context(session)

        onboarding = context["onboarding"]

        onboarding["first_name"] = value

        SessionManager.set_onboarding_step(
            session,
            OnboardingStep.LAST_NAME,
        )

        return OnboardingResult(
            message=msg.LAST_NAME,
            completed=False,
            next_step=OnboardingStep.LAST_NAME,
        )

    @staticmethod
    def _last_name(
        session,
        message: str,
    ) -> OnboardingResult:

        value = message.strip()

        if not value:
            return OnboardingResult(
                message="Please enter your surname.",
                completed=False,
                next_step=OnboardingStep.LAST_NAME,
            )

        context = SessionManager.context(session)

        onboarding = context["onboarding"]

        onboarding["last_name"] = value

        SessionManager.set_onboarding_step(
            session,
            OnboardingStep.DISPLAY_NAME,
        )

        return OnboardingResult(
            message=msg.DISPLAY_NAME,
            completed=False,
            next_step=OnboardingStep.DISPLAY_NAME,
        )

    @staticmethod
    def _display_name(
        session,
        message: str,
    ) -> OnboardingResult:

        value = message.strip()

        if not value:
            return OnboardingResult(
                message="Please enter the name you'd like us to use.",
                completed=False,
                next_step=OnboardingStep.DISPLAY_NAME,
            )

        context = SessionManager.context(session)

        onboarding = context["onboarding"]

        onboarding["display_name"] = value

        SessionManager.set_onboarding_step(
            session,
            OnboardingStep.LANGUAGE,
        )

        return OnboardingResult(
            message=msg.LANGUAGE,
            completed=False,
            next_step=OnboardingStep.LANGUAGE,
        )

    @staticmethod
    def _language(
        session,
        message: str,
    ) -> OnboardingResult:

        value = message.strip()

        if not value:
            return OnboardingResult(
                message="Please enter your preferred language."
                completed=False,
                next_step=OnboardingStep.LANGUAGE,
            )

        context = SessionManager.context(session)

        onboarding = context["onboarding"]

        onboarding["language"] = value

        SessionManager.set_onboarding_step(
            session,
            OnboardingStep.EMAIL,
        )

        return OnboardingResult(
            message=msg.EMAIL,
            completed=False,
            next_step=OnboardingStep.EMAIL,
        )

    @staticmethod
    def _email(
        session,
        message: str,
    ) -> OnboardingResult:

        email = message.strip()

        context = SessionManager.context(session)

        onboarding = context["onboarding"]

        if email.lower() == "skip":
            onboarding["email"] = None

        else:

            if "@" not in email:
                return OnboardingResult(
                    message="Please enter a valid email or reply SKIP.",
                    completed=False,
                    next_step=OnboardingStep.EMAIL,
                )

            onboarding["email"] = email

        SessionManager.set_onboarding_step(
            session,
            OnboardingStep.CONFIRM,
        )

        first_name = onboarding.get("first_name") or "Not Provided"
        last_name = onboarding.get("last_name") or "Not Provided"
        display_name = onboarding.get("display_name")  or "Not Provided"
        language = onboarding.get("language") or "Not Provided"
        user_email = onboarding.get("email") or "Not Provided"

        summary = (
            f"Please confirm your details:\n\n"
            f"First Name: {first_name}\n"
            f"Surname: {last_name}\n"
            f"Display Name: {display_name}\n"
            f"Language: {language}\n"
            f"Email: {email or 'Not Provided'}\n\n"
            "Reply YES to continue or NO to restart."
        )

        return OnboardingResult(
            message=summary,
            completed=False,
            next_step=OnboardingStep.CONFIRM,
        )

    @staticmethod
    def _confirm(
        session,
        message: str,
    ) -> OnboardingResult:

        answer = message.strip().lower()

        if answer not in {
            "yes",
            "y",
            "1"
        }:

            OnboardingEngine._reset_onboarding(
                session
            )

            return OnboardingResult(
                message=(
                    "Okay, let's start again.\n\n"
                    + msg.FIRST_NAME
                ),
                completed=False,
                next_step=OnboardingStep.FIRST_NAME,
            )

            context = SessionManager.context(session)

            onboarding = context["onboarding"]

            display_name = (
                onboarding.get("display_name")
                or onboarding.get("first_name")
                or "Warima Member"
            )

            SessionManager.complete_onboarding(session)

            return OnboardingResult(
                message=(
                    f"Welcome {display_name}! \n\n"
                    "Your Warima profile has been created successfully."
                ),
                completed=True,
                next_step=OnboardingStep.COMPLETE,
                create_wallets=True,
            )


        @staticmethod
        def _reset_onboarding(session):

            context = SessionManager.context(session)

            context["onboarding"] = {
                "active": True,
                "step": OnboardingStep.FIRST_NAME,
            }
