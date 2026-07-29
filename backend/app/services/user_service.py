from app.models.user import User
from app.models.user_identity import UserIdentity
from app.models.user_session import UserSession

from app.models.enums import (
    IdentityProvider,
    SessionState,
    UserStatus,
)

from app.repositories.user_repository import UserRepository
from app.repositories.user_identity_repository import UserIdentityRepository
from app.repositories.user_session_repository import (
    UserSessionRepository,
)

from app.schemas.auth import AuthenticationResult


class UserService:

    def __init__(self, db):
        self.db = db

        self.user_repo = UserRepository(db)
        self.identity_repo = UserIdentityRepository(db)
        self.session_repo = UserSessionRepository(db)

    def authenticate_whatsapp(
        self,
        wa_id: str,
    ) -> AuthenticationResult:
        """
        Authenticate a WhatsApp user.

        If the WhatsApp number already exists, return the
        existing User, Identity and Session.

        Otherwise create:
            User
            UserIdentity
            UserSession

        and return them.
        """

        print("[1] Looking for existing identity")

        identity = self.identity_repo.find_by_provider(
            IdentityProvider.WHATSAPP,
            wa_id,
        )

        print("[2] Identity lookup finished")

        if identity:
            print("[3] Existing identity found")
            session = self.session_repo.get_by_identity(
                identity.id,
            )

            print("[4] Session loaded")

            return AuthenticationResult(
                user=identity.user,
                identity=identity,
                session=session,
                is_new=False,
            )

        print("[5] No identity found. Creating user...")

        try:
            # Create User
            user = User(
                status=UserStatus.PENDING,
            )

            print("[6] User object created")

            self.user_repo.create(user)

            print("[7] User saved")

            # Create WhatsApp Identity
            identity = UserIdentity(
                user_id=user.id,
                provider=IdentityProvider.WHATSAPP,
                provider_identifier=wa_id,
            )

            print("[8] Identity object created")

            self.identity_repo.create(identity)

            print("[9] Identity saved")

            # Create Session
            session = UserSession(
                user_identity_id=identity.id,
                state=SessionState.START,
            )

            print("[10] Session object created")

            self.session_repo.create(session)

            print("[11] Session saved")

            print("[12] Committing transaction")

            self.db.commit()

            print("[13] Commit complete")

            return AuthenticationResult(
                user=user,
                identity=identity,
                session=session,
                is_new=True,
            )

        except Exception as e:
            print("[Error]", e)
            self.db.rollback()
            raise
