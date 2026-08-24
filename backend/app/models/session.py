# backend/app/models/session.py
from sqlalchemy import Column, String, JSON, DateTime
from app.db.base import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True) # Phone number or user ID
    user_id = Column(String)
    context = Column(JSON, default={}) # Contains blockchain, portfolio, etc
    last_active = Column(DateTime)
    created_at = Column(DateTime)
