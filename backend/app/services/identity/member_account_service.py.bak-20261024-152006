import uuid

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
        account = (
            self.db.query(MemberAccount)
            .order_by(MemberAccount.created_at.desc())
            .first()
        )

        if not account:
            return "WRM00000001"

        try:
            last = int(account.account_number.replace("WRM", ""))
        except Exception:
            last = 0

        return f"WRM{last + 1:08d}"
