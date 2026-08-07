from app.engine.onboarding_steps import OnboardingStep
from app.engine import onboarding_messages as msg

from app.schemas.onboarding import OnboardingResult
from app.services.identity.session_manager import SessionManager


class OnboardingEngine:

    @classmethod
    def handle(
        cls,
        user,
        session,
        message: str,
    ) -> OnboardingResult:

        step = SessionManager.onboarding_step(session)

        if step == OnboardingStep.WELCOME:
            return cls._welcome(session)

        elif step == OnboardingStep.FIRST_NAME:
            return cls._first_name(user, session, message)

        elif step == OnboardingStep.LAST_NAME:
            return cls._last_name(user, session, message)

        elif step == OnboardingStep.DISPLAY_NAME:
            return cls._display_name(user, session, message)

        elif step == OnboardingStep.LANGUAGE:
            return cls._language(user, session, message)

        elif step == OnboardingStep.EMAIL:
            return cls._email(user, session, message)

        elif step == OnboardingStep.CONFIRM:
            return cls._confirm(user, session, message)

        return OnboardingResult(
            message="Let's start again.",
            completed=False,
            next_step=OnboardingStep.WELCOME,
        )

    @staticmethod
    def _welcome(session):
        SessionManager.set_onboarding_step(
            session,
            OnboardingStep.FIRST_NAME,
        )
        print(session.context)

        return OnboardingResult(
            message=msg.WELCOME + "\n\n" + msg.FIRST_NAME,
            completed=False,
            next_step=OnboardingStep.FIRST_NAME,
        )

    @staticmethod
    def _first_name(
        user,
        session,
        message,
    ):
        user.first_name = message.strip()
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
        user,
        session,
        message,
    ):
        user.last_name = message.strip()
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
        user,
        session,
        message,
    ):
        user.display_name = message.strip()
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
            user,
            session,
            message,
    ):
        user.language = message.strip()
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
        user,
        session,
        message,
    ):
        email = message.strip()

        if email.lower() != "skip":
            if "@" not in email:
                return OnboardingResult(
                    message="Please enter a valid email or reply SKIP.",
                    completed=False,
                    next_step=OnboardingStep.EMAIL,
                )

            user.email = email

        SessionManager.set_onboarding_step(
            session,
            OnboardingStep.CONFIRM,
        )

        summary = (
            f"Please confirm your details:\n\n"
            f"First Name: {user.first_name}\n"
            f"Surname: {user.last_name}\n"
            f"Display Name: {user.display_name}\n"
            f"Language: {user.language}\n"
            f"Email: {user.email or 'Not Provided'}\n\n"
            "Reply YES to continue or NO to restart."
        )

        return OnboardingResult(
            message=summary,
            completed=False,
            next_step=OnboardingStep.CONFIRM,
        )

    @staticmethod
    def _confirm(
        user,
        session,
        message,
    ):
        answer = message.strip().lower()

        if answer not in ["yes", "y", "1"]:
            SessionManager.set_onboarding_step(
                session,
                OnboardingStep.FIRST_NAME,
            )

            return OnboardingResult(
                message="Okay, let's start again.\n\n" + msg.FIRST_NAME,
                completed=False,
                next_step=OnboardingStep.FIRST_NAME,
            )

        SessionManager.complete_onboarding(session)

        return OnboardingResult(
            message=(
                f"Welcome {user.display_name or user.first_name}! \n\n"
                "Your Warima profile has been created successfully."
            ),
            completed=True,
            next_step=OnboardingStep.COMPLETE,
            create_wallets=True,
        )
