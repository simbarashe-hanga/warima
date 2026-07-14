from sqlalchemy import Column, String, Integer
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    phone_number = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    pin_hash = Column(String)
    status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
