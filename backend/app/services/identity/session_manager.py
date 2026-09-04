# backend/app/services/identity/session_manager.py

from app.engine.onboarding_steps import OnboardingStep


class SessionManager:
    """
    Centralized manager for conversation session state.

    SessionManager is the single abstraction responsible for
    reading and writing session.context.

    Engines should use SessionManager rather than directly
    manipulating session.context.
    """

    # ============================================================
    # INTERNAL
    # ============================================================

    @classmethod
    def initialize(cls, session):
        """
        Ensure the session has a valid context structure.
        """

        if session.context is None:
            session.context = {}

        if not isinstance(session.context, dict):
            raise TypeError(
                "session.context must be a dictionary"
            )

        context = session.context

        context.setdefault(
            "authenticated",
            True,
        )

        context.setdefault(
            "profile_completed",
            False,
        )

        context.setdefault(
            "onboarding",
            {
                "active": True,
                "step": OnboardingStep.WELCOME,
            },
        )

        context.setdefault(
            "wallet",
            {
                "active": False,
                "step": None,
                "amount": None,
            },
        )

        context.setdefault(
            "stokvel",
            {
                "active": False,
                "step": None,
                "options": [],
                "selected_stokvel_id": None,
            },
        )

        context.setdefault(
            "kyc",
            {
                "active": False,
                "step": None,
                "full_name": None,
                "id_number": None,
                "phone": None,
                "verified": False,
                "completed_at": None,
            },
        )

        context.setdefault(
            "investment",
            {
                "active": False,
                "step": None,
            },
        )

        context.setdefault(
            "agent",
            {
                "active": False,
                "step": None,
                "history": [],
            },
        )

        # Explicitly reassign so SQLAlchemy MutableDict
        # sees the complete context.
        session.context = context

        return context

    @classmethod
    def context(cls, session):
        return cls.initialize(session)

    # ============================================================
    # AUTHENTICATION
    # ============================================================

    @classmethod
    def authenticated(cls, session):
        return cls.context(session)["authenticated"]

    @classmethod
    def set_authenticated(
        cls,
        session,
        value: bool,
    ):
        context = cls.context(session)

        context["authenticated"] = bool(value)

        session.context = context

        return context["authenticated"]

    # ============================================================
    # PROFILE
    # ============================================================

    @classmethod
    def profile_completed(cls, session):
        return cls.context(session)["profile_completed"]

    @classmethod
    def set_profile_completed(
        cls,
        session,
        value: bool,
    ):
        context = cls.context(session)

        context["profile_completed"] = bool(value)

        session.context = context

        return context["profile_completed"]

    # ============================================================
    # ONBOARDING
    # ============================================================

    @classmethod
    def onboarding_context(cls, session):
        return cls.context(session)["onboarding"]

    @classmethod
    def onboarding_active(cls, session):
        return cls.onboarding_context(session)["active"]

    @classmethod
    def onboarding_step(cls, session):
        return cls.onboarding_context(session)["step"]

    @classmethod
    def set_onboarding_step(
        cls,
        session,
        step,
    ):
        context = cls.context(session)

        onboarding = dict(
            context["onboarding"]
        )

        onboarding["active"] = True
        onboarding["step"] = step

        context["onboarding"] = onboarding

        session.context = context

        return onboarding

    @classmethod
    def start_onboarding(
        cls,
        session,
        step=OnboardingStep.WELCOME,
    ):
        context = cls.context(session)

        context["onboarding"] = {
            "active": True,
            "step": step,
        }

        context["profile_completed"] = False

        session.context = context

        return context["onboarding"]

    @classmethod
    def complete_onboarding(cls, session):
        context = cls.context(session)

        onboarding = dict(
            context["onboarding"]
        )

        onboarding["active"] = False
        onboarding["step"] = OnboardingStep.COMPLETE

        context["onboarding"] = onboarding
        context["profile_completed"] = True

        session.context = context

        return onboarding

    @classmethod
    def reset_onboarding(cls, session):
        context = cls.context(session)

        context["onboarding"] = {
            "active": True,
            "step": OnboardingStep.FIRST_NAME,
        }

        context["profile_completed"] = False

        session.context = context

        return context["onboarding"]

    # ============================================================
    # WALLET
    # ============================================================

    @classmethod
    def wallet_context(cls, session):
        return cls.context(session)["wallet"]

    @classmethod
    def wallet_active(cls, session):
        return cls.wallet_context(session)["active"]

    @classmethod
    def wallet_step(cls, session):
        return cls.wallet_context(session)["step"]

    @classmethod
    def wallet_amount(cls, session):
        return cls.wallet_context(session)["amount"]

    @classmethod
    def start_wallet(
        cls,
        session,
        step=None,
    ):
        context = cls.context(session)

        context["wallet"] = {
            "active": True,
            "step": step,
            "amount": None,
        }

        session.context = context

        return context["wallet"]

    @classmethod
    def set_wallet_step(
        cls,
        session,
        step,
    ):
        context = cls.context(session)

        wallet = dict(
            context["wallet"]
        )

        wallet["active"] = True
        wallet["step"] = step

        context["wallet"] = wallet

        session.context = context

        return wallet

    @classmethod
    def set_wallet_amount(
        cls,
        session,
        amount,
    ):
        context = cls.context(session)

        wallet = dict(
            context["wallet"]
        )

        wallet["amount"] = amount

        context["wallet"] = wallet

        session.context = context

        return wallet

    @classmethod
    def update_wallet_context(
        cls,
        session,
        updates: dict,
    ):
        if not isinstance(updates, dict):
            raise TypeError(
                "Wallet context updates must be a dictionary"
            )

        context = cls.context(session)

        wallet = dict(
            context["wallet"]
        )

        wallet.update(updates)

        context["wallet"] = wallet

        session.context = context

        return wallet

    @classmethod
    def finish_wallet(cls, session):
        context = cls.context(session)

        context["wallet"] = {
            "active": False,
            "step": None,
            "amount": None,
        }

        session.context = context

        return context["wallet"]

    # ============================================================
    # STOKVEL
    # ============================================================

    @classmethod
    def stokvel_context(cls, session):
        return cls.context(session)["stokvel"]

    @classmethod
    def stokvel_active(cls, session):
        return cls.stokvel_context(session)["active"]

    @classmethod
    def stokvel_step(cls, session):
        return cls.stokvel_context(session)["step"]

    @classmethod
    def stokvel_options(cls, session):
        return cls.stokvel_context(session).get("options", [])

    @classmethod
    def selected_stokvel_id(cls, session):
        return cls.stokvel_context(session).get("selected_stokvel_id")

    @classmethod
    def start_stokvel(
        cls,
        session,
        step=None,
        options=None,
    ):
        context = cls.context(session)

        context["stokvel"] = {
            "active": True,
            "step": step,
            "options": options or [],
            "selected_stokvel_id": context["stokvel"].get(
                "selected_stokvel_id"
            ),
        }

        session.context = context
        return context["stokvel"]

    @classmethod
    def set_stokvel_step(
        cls,
        session,
        step,
    ):
        context = cls.context(session)

        stokvel = dict(
            context["stokvel"]
        )

        stokvel["active"] = True
        stokvel["step"] = step

        context["stokvel"] = stokvel

        session.context = context

        return stokvel

    @classmethod
    def set_stokvel_options(cls, session, options):
        context = cls.context(session)

        stokvel = dict(context["stokvel"])
        stokvel["options"] = options

        context["stokvel"] = stokvel
        session.context = context

        return stokvel

    @classmethod
    def set_selected_stokvel(cls, session, stokvel_id):
        context = cls.context(session)

        stokvel = dict(context["stokvel"])
        stokvel["selected_stokvel_id"] = str(stokvel_id)

        context["stokvel"] = stokvel
        session.context = context

        return stokvel

    @classmethod
    def clear_selected_stokvel(cls, session):
        context = cls.context(session)

        stokvel = dict(context["stokvel"])
        stokvel["selected_stokvel_id"] = None

        context["stokvel"] = stokvel
        session.context = context

        return stokvel

    @classmethod
    def pause_stokvel(cls, session):
        """
        Deactivate the stokvel conversational flow while preserving
        the currently selected stokvel

        Used when handling a selected stokvel to another flow such
        as WalletEngine.
        """
        context = cls.context(session)

        stokvel = dict(context["stokvel"])
        stokvel["active"] = False
        stokvel["step"] = None
        stokvel["options"] = []

        context["stokvel"] = stokvel
        session.context = context

        return stokvel

    @classmethod
    def finish_stokvel(cls, session):
        context = cls.context(session)

        context["stokvel"] = {
            "active": False,
            "step": None,
            "options": [],
            "selected_stokvel_id": None,
        }

        session.context = context

        return context["stokvel"]

    #=============================================================
    # FLOW MANAGEMENT
    #=============================================================

    @classmethod
    def clear_other_flows(
        cls,
        session,
        active_flow: str,
    ):
        """
        Deactivate all interactive flows except active_flow.

        Only one interactive flow should be active at a time.
        """

        context = cls.context(session)

        if active_flow != "wallet":
            cls.finish_wallet(session)

        if active_flow != "stokvel":
            if active_flow == "wallet":
                # Preserve selected stokvel when handling contribution
                # processing to WalletEngine
                cls.pause_stokvel(session)
            else:
                cls.finish_stokvel(session)

        if active_flow != "kyc":
            cls.finish_kyc(session)

        if active_flow != "investment":
            cls.finish_investment(session)

        if active_flow != "onboarding":
            onboarding = dict(context["onboarding"])
            onboarding["active"] = False
            onboarding["step"] = None
            context["onboarding"] = onboarding

        if active_flow != "agent":
            cls.finish_agent(session)

        session.context = context

        return context

    # ============================================================
    # KYC
    # ============================================================

    @classmethod
    def kyc_context(cls, session):
        return cls.context(session)["kyc"]

    @classmethod
    def kyc_active(cls, session):
        return cls.kyc_context(session)["active"]

    @classmethod
    def kyc_step(cls, session):
        return cls.kyc_context(session)["step"]

    @classmethod
    def start_kyc(
        cls,
        session,
        step="full_name",
    ):
        context = cls.context(session)

        context["kyc"] = {
            "active": True,
            "step": step,
            "full_name": None,
            "id_number": None,
            "phone": None,
            "verified": False,
            "completed_at": None,
        }

        session.context = context

        return context["kyc"]

    @classmethod
    def set_kyc_step(
        cls,
        session,
        step,
    ):
        context = cls.context(session)

        kyc = dict(
            context["kyc"]
        )

        kyc["active"] = True
        kyc["step"] = step

        context["kyc"] = kyc

        session.context = context

        return kyc

    @classmethod
    def set_kyc_data(
        cls,
        session,
        **data,
    ):
        context = cls.context(session)

        kyc = dict(
            context["kyc"]
        )

        kyc.update(data)

        context["kyc"] = kyc

        session.context = context

        return kyc

    @classmethod
    def complete_kyc(
        cls,
        session,
        completed_at=None,
    ):
        context = cls.context(session)

        kyc = dict(
            context["kyc"]
        )

        kyc["active"] = False
        kyc["step"] = None
        kyc["verified"] = True
        kyc["completed_at"] = completed_at

        context["kyc"] = kyc

        session.context = context

        return kyc

    @classmethod
    def finish_kyc(cls, session):
        context = cls.context(session)

        kyc = dict(
            context["kyc"]
        )

        kyc["active"] = False
        kyc["step"] = None

        context["kyc"] = kyc

        session.context = context

        return kyc

    # ============================================================
    # INVESTMENT
    # ============================================================

    @classmethod
    def investment_context(cls, session):
        return cls.context(session)["investment"]

    @classmethod
    def investment_active(cls, session):
        return cls.investment_context(session)["active"]

    @classmethod
    def investment_step(cls, session):
        return cls.investment_context(session)["step"]

    @classmethod
    def start_investment(
        cls,
        session,
        step=None,
    ):
        context = cls.context(session)

        context["investment"] = {
            "active": True,
            "step": step,
        }

        session.context = context

        return context["investment"]

    @classmethod
    def set_investment_step(
        cls,
        session,
        step,
    ):
        context = cls.context(session)

        investment = dict(
            context["investment"]
        )

        investment["active"] = True
        investment["step"] = step

        context["investment"] = investment

        session.context = context

        return investment

    @classmethod
    def finish_investment(cls, session):
        context = cls.context(session)

        context["investment"] = {
            "active": False,
            "step": None,
        }

        session.context = context

        return context["investment"]

    # ============================================================
    # AGENT
    # ============================================================

    @classmethod
    def agent_context(cls, session):
        return cls.context(session)["agent"]

    @classmethod
    def agent_active(cls, session):
        return cls.agent_context(session)["active"]

    @classmethod
    def start_agent(cls, session):
        context = cls.context(session)

        agent = dict(
            context["agent"]
        )

        agent["active"] = True
        agent["step"] = "chatting"

        context["agent"] = agent

        session.context = context

        return agent

    @classmethod
    def finish_agent(cls, session):
        context = cls.context(session)

        agent = dict(
            context["agent"]
        )

        agent["active"] = False
        agent["step"] = None

        context["agent"] = agent

        session.context = context

        return agent

    @classmethod
    def add_agent_message(
        cls,
        session,
        role: str,
        content: str,
    ):
        context = cls.context(session)

        agent = dict(
            context["agent"]
        )

        history = list(
            agent.get("history") or []
        )

        history.append(
            {
                "role": role,
                "content": content,
            }
        )

        agent["history"] = history
        context["agent"] = agent

        session.context = context

        return history

    # ============================================================
    # GENERIC CONTEXT
    # ============================================================

    @classmethod
    def update_context(
        cls,
        session,
        updates: dict,
    ):
        """
        Safely update session context.

        Nested dictionaries are merged rather than replaced.
        """

        if not isinstance(updates, dict):
            raise TypeError(
                "Context updates must be a dictionary"
            )

        context = cls.context(session)

        for key, value in updates.items():

            if (
                isinstance(value, dict)
                and isinstance(
                    context.get(key),
                    dict,
                )
            ):

                current = dict(
                    context[key]
                )

                current.update(value)

                context[key] = current

            else:

                context[key] = value

        session.context = context

        return context
