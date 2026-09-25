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

class StokvelStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"

class MembershipStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    LEFT = "LEFT"

class MembershipRole(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    TREASURER = "TREASURER"
    SECRETARY = "SECRETARY"
    MEMBER = "MEMBER"

class WalletStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"

class WalletTransactionType(str, Enum):
    CONTRIBUTION = "CONTRIBUTION"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"

class WalletTransactionStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class WalletLedgerEntryType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"

class SettlementStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class SettlementAsset(str, Enum):
    SOL = "SOL"
    ZAR = "ZAR"
    WZAR = "WZAR"

class StokvelType(str, Enum):
    SAVINGS = "SAVINGS"
    AGRICULTURE = "AGRICULTURE"
    DIGITAL_ASSET = "DIGITAL_ASSET"

class TreasuryDenomination(str, Enum):
    SOL = "SOL"
    WZAR = "WZAR"
    ZAR = "ZAR"

class TreasuryRail(str, Enum):
    SOLANA = "SOLANA"
    EVM = "EVM"
    OFF_CHAIN = "OFF_CHAIN"


class TreasuryStrategy(str, Enum):
    ON_CHAIN = "ON_CHAIN"
    AGRICULTURE = "AGRICULTURE"
    CASH = "CASH"


class TreasuryReturnSource(str, Enum):
    ON_CHAIN = "ON_CHAIN"
    MEAT_SALES = "MEAT_SALES"
    CASH_RETURNS = "CASH_RETURNS"

class BlockchainChain(str, Enum):
    SOLANA = "SOLANA"
    EVM = "EVM"

class BlockchainAccountType(str, Enum):
    MANAGED = "MANAGED"
    EXTERNAL = "EXTERNAL"

class BlockchainAccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"

class PaymentStatus(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
