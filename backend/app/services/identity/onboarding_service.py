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

        if result.save_session:
            self.db.add(session)

        if user is not None:
            self.db.add(user)

        if member_account is not None:
            self.db.add(member_account)

        self.db.commit()

        return result
