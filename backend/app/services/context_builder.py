from typing import Dict, Any
from app.core.prompts import WARIMA_SYSTEM_PROMPT


class ContextBuilder:

    @staticmethod
    async def build(
        user,
        identity,
        session,
        member_account,
    ) -> Dict[str, Any]:

        return {

            "identity": {

                "id": str(identity.id),
                "provider": str(identity.provider),
                "provider_identifier": identity.provider_identifier,
            },

            "profile": {

                "id": str(user.id),
                "display_name": user.display_name,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "language": user.language,
                "status": str(user.status),
            },

            "member_account": {
                "id": str(member_account.id),
                "account_number": member_account.account_number,
                "display_name": member_account.display_name,
                "account_type": str(member_account.account_type),
                "status": str(member_account.status),
            },

            "session": {
                "state": str(session.state),
                "context": session.context or {},
            },

            #
            # Future modules
            #

            "wallets": [],
            "memberships": [],
            "roles": [],
            "permissions": [],
        }

    @staticmethod
    def context_to_prompt(context):

        profile = context["profile"]
        identity = context["identity"]
        account = context["member_account"]
        session = context["session"]

        lines = []

        lines.append("MEMBER CONTEXT")
        lines.append("")

        #
        # Identity
        #

        lines.append("IDENTITY")

        lines.append(
            f"Provider: {identity['provider']}"
        )

        lines.append(
            f"Identifier: {identity['provider_identifier']}"
        )

        lines.append("")

        #
        # Member Account
        #
        lines.append("MEMBER ACCOUNT")

        lines.append(f"Account Number: {account['account_number']}")
        lines.append(f"Display Name: {account['display_name']}")
        lines.append(f"Account Type: {account['account_type']}")
        lines.append(f"Status: {account['status']}")

        lines.append("")

        #
        # Profile
        #

        lines.append("PROFILE")

        lines.append(f"First Name: {profile['first_name']}")
        lines.append(f"Last Name: {profile['last_name']}")
        lines.append(f"Language: {profile['language']}")
        lines.append(f"Status: {profile['status']}")

        if profile["email"]:
            lines.append(f"Email: {profile['email']}")

        lines.append("")

        #
        # Session
        #

        lines.append("SESSION")

        lines.append(f"State: {session['state']}")

        for key, value in session["context"].items():
            lines.append(f"{key}: {value}")

        lines.append("")

        #
        # Future modules
        #

        lines.append("WALLETS")
        lines.append("Wallets: Not Loaded")

        lines.append("")

        lines.append("MEMBERSHIP")
        lines.append("Memberships: Not Loaded")
        
        lines.append("")

        lines.append("ROLES")
        lines.append("Roles: Not Loaded")
        
        lines.append("")

        lines.append("PERMISSIONS")
        lines.append("Permissions Not Loaded")

        return "\n".join(lines)

    @classmethod
    async def build_system_prompt(
        cls,
        user,
        identity,
        session,
        member_account,
    ):

        context = await cls.build(
            user=user,
            identity=identity,
            session=session,
            member_account=member_account
        )

        return (
            WARIMA_SYSTEM_PROMPT
            + "\n\n"
            + cls.context_to_prompt(context)
        )
