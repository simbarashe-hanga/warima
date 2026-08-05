from enum import Enum


class UserStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"


class IdentityProvider(str, Enum):
    WHATSAPP = "WHATSAPP"
    EMAIL = "EMAIL"
    GOOGLE = "GOOGLE"
    APPLE = "APPLE"


class SessionState(str, Enum):
    START = "START"
    ASK_FIRST_NAME = "ASK_FIRST_NAME"
    ASK_LAST_NAME = "ASK_LAST_NAME"
    ASK_LANGUAGE = "ASK_LANGUAGE"
    HOME = "HOME"
    CONTRIBUTION = "CONTRIBUTION"
    LOAN = "LOAN"
    INVESTMENT = "INVESTMENT"
    SETTINGS = "SETTINGS"


class MemberAccountType(str, Enum):
    PERSONAL = "PERSONAL"
    BUSINESS = "BUSINESS"
    COMMUNITY = "COMMUNITY"
    CHURCH = "CHURCH"
    SCHOOL = "SCHOOL"


class MemberAccountStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"
