# backend/app/engine/conversation.py
from typing import Dict, Optional
from datetime import datetime
from app.services.identity.session_manager import SessionManager


class ConversationManager:
    """Manages conversation context from session"""

    @staticmethod
    def get_context(session: Dict) -> Dict:
        """Get conversation context from session"""
        return session.get("context", {})


    @staticmethod
    def update_context(session: Dict, updates: Dict) -> Dict:
        """Update conversation context"""
        if context not in session:
            session["context"] = {}

        session["context"].update(updates)
        return session["context"]


    @staticmethod
    def clear_context(session: Dict) -> Dict:
        """Clear conversation context"""
        session["context"] = {}
        return session


    @staticmethod
    def add_to_history(session: Dict, message: str, response: str) -> None:
        """Add to conversation history"""
        if "history" not in session:
            session["history"] = []

            session["history"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "user": message,
                "bot": response
            })

            # Keep last 50 messages
            if len(session["history"]) > 50:
                session["history"] = session["history"][-50:]
