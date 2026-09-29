from app.engine.onboarding_engine import OnboardingEngine
from app.services.identity.session_manager import SessionManager


class OnboardingService:

    def __init__(self, db):
        self.db = db

    async def process(
        self,
        user,
        session,
        member_account,
        message,
        intent=None,
        member_context=None,
    ):

        intent = intent or {}
        member_context = member_context or {}

        SessionManager.initialize(session)

        result = await OnboardingEngine.handle(
            message=message,
            intent=intent,
            session=session,
            member_context=member_context,
        )

        # ---------------------------------------------------------------
        # Persist onboarding data to the canonical User record.
        #
        # The engine owns onboarding conversation state.
        # This service owns persistence.
        # ---------------------------------------------------------------

        context = SessionManager.context(session)
        onboarding = context.get("onboarding", {})

        if user is not None:

            user.first_name = onboarding.get("first_name")
            user.last_name = onboarding.get("last_name")
            user.display_name = onboarding.get("display_name")
            user.language = onboarding.get("language")
            user.email = onboarding.get("email")

            self.db.add(user)

        if result.save_session:
            self.db.add(session)

        if member_account is not None:
            self.db.add(member_account)

        self.db.commit()

        return result
