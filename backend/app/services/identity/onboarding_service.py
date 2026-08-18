from app.engine.onboarding_engine import OnboardingEngine


class OnboardingService:

    def __init__(self, db):
        self.db = db

    def process(
        self,
        user,
        session,
        member_account,
        message,
    ):
        return OnboardingEngine.handle(
            user=user,
            session=session,
            message=message,
        )
