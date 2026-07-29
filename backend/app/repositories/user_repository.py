from app.repositories.base import BaseRepository
from app.models.user import User
from uuid import UUID


class UserRepository(BaseRepository):

    def get(self, user_id: UUID) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create(self, user: User):
        self.db.add(user)
        self.db.flush()		#Generates UUID before commit
        return user
