from sqlalchemy import Column, String, Integer
from app.db.base import Base


class Whatsapp_Accounts(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    user_id
    wa_id
    phone_number
    verified
    created_at
