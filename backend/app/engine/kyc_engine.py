from typing import Dict, Optional
from app.services.identity.session_manager import SessionManager

class KYC:
    """Handles KYC (Know Your Customer) operations"""
    
    @classmethod
    def process(cls, session: Dict, message: str) -> Dict:
        """Process KYC commands"""
        message_lower = message.lower().strip()
        
        # Get KYC context
        context = session.get("context", {})
        kyc_context = context.get("kyc", {})
        
        # Check if in KYC flow
        if kyc_context.get("active"):
            return cls._handle_kyc_flow(session, message)
        
        # Handle KYC commands
        if message_lower in ["kyc", "verify", "identity"]:
            return cls._start_kyc_flow(session)
        
        elif message_lower == "kyc status":
            return cls._get_kyc_status(session)
        
        return {
            "message": "🔐 *KYC Commands*\n\n"
                       "• KYC - Start identity verification\n"
                       "• KYC STATUS - Check your verification status\n\n"
                       "We need to verify your identity for compliance.",
            "context_update": {}
        }
    
    @classmethod
    def _start_kyc_flow(cls, session: Dict) -> Dict:
        """Start the KYC flow"""
        SessionManager.update_context(session, {
            "kyc": {
                "active": True,
                "step": "full_name"
            }
        })
        
        return {
            "message": "🔐 *Identity Verification*\n\n"
                       "Let's verify your identity. This is required for compliance.\n\n"
                       "What is your full name as it appears on your ID?",
            "context_update": {"kyc": {"active": True, "step": "full_name"}}
        }
    
    @classmethod
    def _handle_kyc_flow(cls, session: Dict, message: str) -> Dict:
        """Handle active KYC flow"""
        context = session.get("context", {})
        kyc_context = context.get("kyc", {})
        step = kyc_context.get("step", "full_name")
        
        message_lower = message.lower().strip()
        
        if message_lower in ["back", "exit", "cancel"]:
            SessionManager.update_context(session, {
                "kyc": {"active": False}
            })
            return {
                "message": "KYC verification cancelled. Type KYC to start again.",
                "context_update": {"kyc": {"active": False}}
            }
        
        if step == "full_name":
            # Store full name
            SessionManager.update_context(session, {
                "kyc": {
                    "active": True,
                    "step": "id_number",
                    "full_name": message
                }
            })
            return {
                "message": f"Thank you, {message}.\n\n"
                           "Please enter your ID number (e.g., 9201025671082):",
                "context_update": {"kyc": {"step": "id_number"}}
            }
        
        elif step == "id_number":
            # Store ID number
            SessionManager.update_context(session, {
                "kyc": {
                    "active": True,
                    "step": "phone",
                    "full_name": kyc_context.get("full_name", ""),
                    "id_number": message
                }
            })
            return {
                "message": "Please enter your phone number (e.g., 0712345678):",
                "context_update": {"kyc": {"step": "phone"}}
            }
        
        elif step == "phone":
            # Store phone and confirm
            SessionManager.update_context(session, {
                "kyc": {
                    "active": True,
                    "step": "confirm",
                    "full_name": kyc_context.get("full_name", ""),
                    "id_number": kyc_context.get("id_number", ""),
                    "phone": message
                }
            })
            
            return {
                "message": f"✅ *Please confirm your details*\n\n"
                           f"Name: {kyc_context.get('full_name', '')}\n"
                           f"ID Number: {kyc_context.get('id_number', '')}\n"
                           f"Phone: {message}\n\n"
                           "Reply CONFIRM to submit or CANCEL to start over.",
                "context_update": {"kyc": {"step": "confirm"}}
            }
        
        elif step == "confirm":
            if message_lower in ["confirm", "yes", "1"]:
                # Complete KYC
                SessionManager.update_context(session, {
                    "kyc": {
                        "active": False,
                        "verified": True,
                        "completed_at": str(datetime.now())
                    }
                })
                return {
                    "message": "🎉 *KYC Verification Complete!*\n\n"
                               "Your identity has been verified successfully.\n"
                               "You now have full access to all features.",
                    "context_update": {"kyc": {"active": False, "verified": True}}
                }
            else:
                # Reset KYC
                SessionManager.update_context(session, {
                    "kyc": {"active": True, "step": "full_name"}
                })
                return {
                    "message": "Let's start over.\n\n"
                               "What is your full name as it appears on your ID?",
                    "context_update": {"kyc": {"step": "full_name"}}
                }
        
        return {
            "message": "I didn't understand that. Please follow the prompts.",
            "context_update": {}
        }
    
    @classmethod
    def _get_kyc_status(cls, session: Dict) -> Dict:
        """Get KYC verification status"""
        context = session.get("context", {})
        kyc_context = context.get("kyc", {})
        
        if kyc_context.get("verified"):
            return {
                "message": "✅ *KYC Status: Verified*\n\n"
                           "Your identity has been verified.\n"
                           f"Verified on: {kyc_context.get('completed_at', 'Unknown')}",
                "context_update": {}
            }
        else:
            return {
                "message": "⚠️ *KYC Status: Not Verified*\n\n"
                           "Please complete KYC verification to access all features.\n"
                           "Type KYC to start the verification process.",
                "context_update": {}
            }

# Import datetime for timestamps
from datetime import datetime
