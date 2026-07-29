from app.models.enums import IdentityProvider
from app.repositories.base import BaseRepository
from app.models.user_identity import UserIdentity
from uuid import UUID


class UserIdentityRepository(BaseRepository):

    def find_by_provider(
        self,
        provider: IdentityProvider,
        identifier: str,
    ) -> UserIdentity | None:
        return (
            self.db.query(UserIdentity)
            .filter(
                UserIdentity.provider == provider,
                UserIdentity.provider_identifier == identifier,
            )
            .first()
        )

    def create(self, identity: UserIdentity):
        self.db.add(identity)
        self.db.flush()
        return identity
