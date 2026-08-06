from sqlalchemy.orm import Session
from app.models.member_account import MemberAccount


class MemberAccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, account_id):
        return (
            self.db.query(MemberAccount)
            .filter(MemberAccount)
            .first()
        )

    def get_by_user(self, user_id):
        return (
            self.db.query(MemberAccount)
            .filter(MemberAccount.user_id == user_id)
            .first()
        )

    def get_by_account_number(self, account_number):
        return (
            self.db.query(MemberAccount)
            .filter(
                MemberAccount.account_number == account_number
            )
            .first()
        )

    def create(self, account):
        self.db.add(account)
        self.db.flush()
        self.db.refresh(account)
        return account

    def update(self):
        self.db.flush()

    def delete(self, account):
        self.db.delete(account)
