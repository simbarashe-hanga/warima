from dataclasses import dataclass

from app.models.user import User
from app.models.user_identity import UserIdentity
from app.models.user_session import UserSession
from app.models.member_account import MemberAccount


@dataclass
class AuthenticationResult:
    user: User
    identity: UserIdentity
    session: UserSession
    member_account: MemberAccount
    is_new: bool
