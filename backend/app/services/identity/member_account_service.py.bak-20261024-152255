import uuid

from sqlalchemy import Integer, cast, func, text

from app.models.member_account import MemberAccount
from app.models.enums import (
    MemberAccountStatus,
    MemberAccountType,
)

from app.repositories.member_account_repository import (
    MemberAccountRepository,
)


class MemberAccountService:
    def __init__(self, db):
        self.db = db
        self.repo = MemberAccountRepository(db)

    def get_member_account(self, user_id):
        return self.repo.get_by_user(user_id)

    def ensure_member_account(self, user):
        account = self.repo.get_by_user(user.id)

        if account:
            return account

        return self.create_default_account(user)

    def create_default_account(self, user):
        account = MemberAccount(
            user_id=user.id,
            account_number=self.generate_account_number(),
            display_name=user.display_name,
            account_type=MemberAccountType.PERSONAL,
            status=MemberAccountStatus.ACTIVE,
        )

        return self.repo.create(account)

    def generate_account_number(self):
        # Serialize allocation across transactions using this generator.
        self.db.execute(
            text("SELECT pg_advisory_xact_lock(:lock_key)"),
            {"lock_key": 872014620261},
        )

        # Ignore demo identifiers; use only WRM followed by eight digits.
        last_number = (
            self.db.query(
                func.max(
                    cast(
                        func.substring(MemberAccount.account_number, 4, 8),
                        Integer,
                    )
                )
            )
            .filter(
                MemberAccount.account_number.op("~")(r"^WRM[0-9]{8}$")
            )
            .scalar()
        )

        next_number = (last_number or 0) + 1

        if next_number > 99_999_999:
            raise ValueError("Member account number sequence is exhausted")

        return f"WRM{next_number:08d}"
