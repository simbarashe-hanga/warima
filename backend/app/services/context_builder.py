from typing import Dict, Any
from app.core.prompts import WARIMA_SYSTEM_PROMPT


class ContextBuilder:

    @staticmethod
    async def build(
        user,
        identity,
        session,
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

            "session": {

                "state": str(session.state),

                "context": session.context or {},
            },

            "wallets": [],

            "memberships": [],

            "roles": [],

            "permissions": [],
        }

    @staticmethod
    def context_to_prompt(
        context,
    ):

        profile = context["profile"]
        identity = context["identity"]
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
        # Profile
        #

        lines.append("PROFILE")

        lines.append(
            f"Display Name: {profile['display_name']}"
        )

        lines.append(
            f"First Name: {profile['first_name']}"
        )

        lines.append(
            f"Last Name: {profile['last_name']}"
        )

        lines.append(
            f"Language: {profile['language']}"
        )

        lines.append(
            f"Status: {profile['status']}"
        )

        if profile["email"]:
            lines.append(
                f"Email: {profile['email']}"
            )

        lines.append("")

        #
        # Session
        #

        lines.append("SESSION")

        lines.append(
            f"State: {session['state']}"
        )

        for key, value in session["context"].items():

            lines.append(
                f"{key}: {value}"
            )

        lines.append("")

        #
        # Wallets
        #

        lines.append("Wallets: Not Loaded")

        #
        # Memberships
        #

        lines.append(
            "Memberships: Not Loaded"
        )

        return "\n".join(lines)

    @classmethod
    async def build_system_prompt(
        cls,
        user,
        identity,
        session,
    ):

        context = await cls.build(
            user=user,
            identity=identity,
            session=session,
        )

        return (
            WARIMA_SYSTEM_PROMPT
            + "\n\n"
            + cls.context_to_prompt(context)
        )
