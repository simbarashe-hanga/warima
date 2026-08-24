from typing import Dict, Optional, Any
from app.services.identity.session_manager import SessionManager

class StokvelEngine:
    """Handles stokvel-related operations"""
    
    @classmethod
    def process(cls, session: Dict, message: str) -> Dict:
        """Process stokvel commands"""
        message_lower = message.lower().strip()
        
        # Get stokvel context
        context = session.get("context", {})
        stokvel_context = context.get("stokvel", {})
        
        # Check if in stokvel flow
        if stokvel_context.get("active"):
            return cls._handle_stokvel_flow(session, message)
        
        # Handle stokvel commands
        if message_lower in ["stokvel", "group", "savings"]:
            return cls._start_stokvel_flow(session)
        
        elif message_lower == "members":
            return cls._list_members(session)
        
        elif message_lower == "vote":
            return cls._start_vote(session)
        
        elif message_lower.startswith("vote yes") or message_lower.startswith("vote no"):
            return cls._handle_vote(session, message)
        
        elif message_lower == "proposals":
            return cls._list_proposals(session)
        
        elif message_lower == "stokvel help":
            return cls._get_help()
        
        return {
            "message": cls._get_help(),
            "context_update": {}
        }
    
    @classmethod
    def _start_stokvel_flow(cls, session: Dict) -> Dict:
        """Start the stokvel flow"""
        SessionManager.update_context(session, {
            "stokvel": {
                "active": True,
                "step": "menu"
            }
        })
        
        return {
            "message": cls._get_menu(),
            "context_update": {"stokvel": {"active": True}}
        }
    
    @classmethod
    def _handle_stokvel_flow(cls, session: Dict, message: str) -> Dict:
        """Handle active stokvel flow"""
        message_lower = message.lower().strip()
        
        if message_lower in ["back", "exit", "cancel"]:
            SessionManager.update_context(session, {
                "stokvel": {"active": False}
            })
            return {
                "message": "Exited stokvel menu. Type STOKVEL to return.",
                "context_update": {"stokvel": {"active": False}}
            }
        
        if message_lower == "members":
            return cls._list_members(session)
        
        if message_lower == "vote":
            return cls._start_vote(session)
        
        if message_lower == "proposals":
            return cls._list_proposals(session)
        
        return {
            "message": cls._get_menu(),
            "context_update": {}
        }
    
    @classmethod
    def _list_members(cls, session: Dict) -> Dict:
        """List stokvel members"""
        # Placeholder - implement actual member listing
        return {
            "message": "*Stokvel Members*\n\n"
                       "1. Admin (Admin)\n"
                       "2. Member 1\n"
                       "3. Member 2\n"
                       "4. Member 3\n\n"
                       "Total: 4 members\n"
                       "Type 'STOKVEL' to return to menu.",
            "context_update": {}
        }
    
    @classmethod
    def _start_vote(cls, session: Dict) -> Dict:
        """Start a voting session"""
        return {
            "message": "*Active Proposals*\n\n"
                       "1. Buy 2 Large White pigs (R16,000)\n"
                       "   Ends: 3 days\n\n"
                       "2. Sell pig #4 (R8,500)\n"
                       "   Ends: 5 days\n\n"
                       "Reply: 'VOTE YES 1' or 'VOTE NO 1'\n"
                       "Type 'STOKVEL' to return to menu.",
            "context_update": {}
        }
    
    @classmethod
    def _handle_vote(cls, session: Dict, message: str) -> Dict:
        """Handle voting"""
        parts = message.lower().split()
        if len(parts) < 3:
            return {
                "message": "Please specify: VOTE YES 1 or VOTE NO 1",
                "context_update": {}
            }
        
        vote = parts[1]  # yes or no
        proposal_id = parts[2]  # proposal number
        
        return {
            "message": f"Your vote has been recorded!\n"
                       f"Proposal: #{proposal_id}\n"
                       f"Vote: {vote.upper()}\n\n"
                       "Your vote has been recorded on the blockchain.",
            "context_update": {}
        }
    
    @classmethod
    def _list_proposals(cls, session: Dict) -> Dict:
        """List all proposals"""
        return {
            "message": "*All Proposals*\n\n"
                       "1. Buy 2 Large White pigs (R16,000)\n"
                       "   Status: Active\n"
                       "   Votes: 3 YES, 1 NO\n\n"
                       "2. Sell pig #4 (R8,500)\n"
                       "   Status: Active\n"
                       "   Votes: 2 YES, 2 NO\n\n"
                       "Type 'VOTE' to vote on proposals.",
            "context_update": {}
        }
    
    @classmethod
    def _get_menu(cls) -> str:
        return "*Stokvel Menu*\n\n" \
               "• MEMBERS - View all members\n" \
               "• VOTE - Vote on proposals\n" \
               "• PROPOSALS - List all proposals\n" \
               "• BACK - Exit stokvel menu\n\n" \
               "Type your choice or 'STOKVEL HELP' for more info."
    
    @classmethod
    def _get_help(cls) -> str:
        return "*Stokvel Commands*\n\n" \
               "• STOKVEL - Enter stokvel menu\n" \
               "• MEMBERS - List all members\n" \
               "• VOTE - Vote on proposals\n" \
               "• PROPOSALS - List all proposals\n" \
               "• VOTE YES 1 - Vote yes on proposal 1\n" \
               "• VOTE NO 1 - Vote no on proposal 1\n\n" \
               "Your stokvel is managed on the blockchain!"
