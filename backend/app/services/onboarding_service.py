from app.repositories.user_repository import UserRepository
from app.engine.onboarding_engine import OnboardingEngine

class OnboardingService:

    def __init__(self, db):
        self.db = db
        self.user_repo = UserRepository(db)

    def process(
        self,
        user,
        session,
        member_account,
        message,
    ):
        return OnboardingEngine.handle(
            db=self.db,
            user=user,
            session=session,
            message=message,
        )
