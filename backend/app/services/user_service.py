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

from app.services.member_account_service import MemberAccountService

from app.schemas.auth import AuthenticationResult


class UserService:

    def __init__(self, db):
        self.db = db

        self.user_repo = UserRepository(db)
        self.identity_repo = UserIdentityRepository(db)
        self.session_repo = UserSessionRepository(db)
        self.member_account_service = MemberAccountService(db)

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

            #
            # Recover missing session
            #

            if session is None:
                print("[4] Session missing. Creating.") 

                session = UserSession(
                    user_identity_id=identity.id,
                    state=SessionState.START,
                )

                SessionManager.initialize(session)

                self.session_repo.create(session)

            #
            # Ensure default context exists
            #

            if session.context is None:
                session.context = {}

            session.context.setdefault(
                "authenticated",
                True,
            )

            session.context.setdefault(
                "new_user",
                False,
            )

            session.context.setdefault(
                "onboarding",
                False,
            )

            session.context.setdefault(
                "profile_completed",
                True,
            )

            #
            # Ensure financial account exists
            #

            member_account = (
                self.member_account_service.ensure_member_account(
                    identity.user,
                )
            )

            self.db.commit()

            return AuthenticationResult(
                user=identity.user,
                identity=identity,
                session=session,
                member_account=member_account,
                is_new=False,
            )

        #
        # First-time member
        #

        print("[5] No identity found. Creating user...")

        try:
            # Create User
            user = User(
                status=UserStatus.PENDING,
            )

            self.user_repo.create(user)

            identity = UserIdentity(
                user_id=user.id,
                provider=IdentityProvider.WHATSAPP,
                provider_identifier=wa_id,
            )

            self.identity_repo.create(identity)

            session = UserSession(
                user_identity_id=identity.id,
                state=SessionState.START,
                context={
                    "authenticated": True,
                    "new_user": True,
                    "onboarding": True,
                    "profile_completed": False,
                    "flow": "welcome",
                },
            )

            self.session_repo.create(session)

            #
            # Create default financial account
            #

            member_account = (
                self.member_account_service.ensure_member_account(
                    user,
                )
            )

            self.db.commit()

            return AuthenticationResult(
                user=user,
                identity=identity,
                session=session,
                member_account=member_account,
                is_new=True,
            )
        
        except Exception as e:
            print("[Error]", e)
            self.db.rollback()
            raise
