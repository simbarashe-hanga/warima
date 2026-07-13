from sqlalchemy import Column, String, Integer
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    phone_number = Column(string)
    first_name = Column(string)
    last_name = Column(string)
    email = Column(string)
    pin_hash = Column(string)
    status = Column(String)
    created_at = Column(String)
    updated_at = Column(string
