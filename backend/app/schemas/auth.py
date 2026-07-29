from dataclasses import dataclass

from app.models.user import User
from app.models.user_identity import UserIdentity
from app.models.user_session import UserSession


@dataclass
class AuthenticationResult:
    user: User
    identity: UserIdentity
    session: UserSession
    is_new: bool
