from app.engine.onboarding_steps import OnboardingStep


class SessionManager:
    """
    Centralized manager for all session state.

    This is the ONLY class that should read or write session.context.
    """

    #####################################################################
    # Internal
    #####################################################################

    @classmethod
    def initialize(cls, session):
        if session.context is None:
            session.context = {}

        context = session.context

        context.setdefault("authenticated", True)
        context.setdefault("profile_completed", False)

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
            },
        )

        context.setdefault(
            "kyc",
            {
                "active": False,
                "step": None,
            },
        )

        context.setdefault(
            "investment",
            {
                "active": False,
                "step": None,
            },
        )

        return context

    @classmethod
    def context(cls, session):
        return cls.initialize(session)

    #####################################################################
    # Authentication
    #####################################################################

    @classmethod
    def authenticated(cls, session):
        return cls.initialize(session)["authenticated"]

    @classmethod
    def set_authenticated(cls, session, value: bool):
        cls.initialize(session)["authenticated"] = value

    #####################################################################
    # Profile
    #####################################################################

    @classmethod
    def profile_completed(cls, session):
        return cls.initialize(session)["profile_completed"]

    @classmethod
    def set_profile_completed(cls, session, value: bool):
        cls.initialize(session)["profile_completed"] = value

    #####################################################################
    # Onboarding
    #####################################################################

    @classmethod
    def onboarding_active(cls, session):
        return cls.initialize(session)["onboarding"]["active"]

    @classmethod
    def onboarding_step(cls, session):
        return cls.initialize(session)["onboarding"]["step"]

    @classmethod
    def set_onboarding_step(cls, session, step):
        onboarding = dict(cls.initialize(session)["onboarding"])
        onboarding["step"] = step
        cls.initialize(session)["onboarding"] = onboarding

    @classmethod
    def complete_onboarding(cls, session):
        cls.set_profile_completed(session, True)

        onboarding = dict(cls.initialize(session)["onboarding"])
        onboarding["active"] = False
        onboarding["step"] = None

        cls.initialize(session)["onboarding"] = onboarding

    #####################################################################
    # Wallet
    #####################################################################

    @classmethod
    def wallet_active(cls, session):
        return cls.initialize(session)["wallet"]["active"]

    @classmethod
    def wallet_step(cls, session):
        return cls.initialize(session)["wallet"]["step"]

    @classmethod
    def wallet_amount(cls, session):
        return cls.initialize(session)["wallet"]["amount"]

    @classmethod
    def start_wallet(cls, session, step=None):
        wallet = dict(cls.initialize(session)["wallet"])
        wallet["active"] = True
        wallet["step"] = step
        wallet["amount"] = None

        cls.initialize(session)["wallet"] = wallet

    @classmethod
    def set_wallet_step(cls, session, step):
        wallet = dict(cls.initialize(session)["wallet"])
        wallet["step"] = step

        cls.initialize(session)["wallet"] = wallet

    @classmethod
    def set_wallet_amount(cls, session, amount):
        wallet = dict(cls.initialize(session)["wallet"])
        wallet["amount"] = amount

        cls.initialize(session)["wallet"] = wallet

    @classmethod
    def finish_wallet(cls, session):
        wallet = dict(cls.initialize(session)["wallet"])
        wallet["active"] = False
        wallet["step"] = None
        wallet["amount"] = None

        cls.initialize(session)["wallet"] = wallet

    #####################################################################
    # Stokvel
    #####################################################################

    @classmethod
    def start_stokvel(cls, session, step=None):
        stokvel = dict(cls.initialize(session)["stokvel"])
        stokvel["active"] = True
        stokvel["step"] = step

        cls.initialize(session)["stokvel"] = stokvel

    @classmethod
    def finish_stokvel(cls, session):
        stokvel = dict(cls.initialize(session)["stokvel"])
        stokvel["active"] = False
        stokvel["step"] = None

        cls.initialize(session)["stokvel"] = stokvel

    #####################################################################
    # KYC
    #####################################################################

    @classmethod
    def start_kyc(cls, session, step=None):
        kyc = dict(cls.initialize(session)["kyc"])
        kyc["active"] = True
        kyc["step"] = step

        cls.initialize(session)["kyc"] = kyc

    @classmethod
    def finish_kyc(cls, session):
        kyc = dict(cls.initialize(session)["kyc"])
        kyc["active"] = False
        kyc["step"] = None

        cls.initialize(session)["kyc"] = kyc

    #####################################################################
    # Investment
    #####################################################################

    @classmethod
    def start_investment(cls, session, step=None):
        investment = dict(cls.initialize(session)["investment"])
        investment["active"] = True
        investment["step"] = step

        cls.initialize(session)["investment"] = investment

    @classmethod
    def finish_investment(cls, session):
        investment = dict(cls.initialize(session)["investment"])
        investment["active"] = False
        investment["step"] = None

        cls.initialize(session)["investment"] = investment
