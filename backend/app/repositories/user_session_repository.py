from app.repositories.base import BaseRepository
from app.models.user_session import UserSession
from uuid import UUID


class UserSessionRepository(BaseRepository):

    def get_by_identity(self, identity_id:UUID) -> UserSession | None:
        return (
            self.db.query(UserSession)
            .filter(
                UserSession.user_identity_id == identity_id
            )
            .first()
        )

    def create(self, session):
        self.db.add(session)
        self.db.flush()
        return session
