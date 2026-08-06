from app.engine.onboarding_steps import OnboardingStep


class SessionManager:
    """
    Centralized session context manager

    No other module should modify session.context directly
    """

    @staticmethod
    def context(session):

        if session.context is None:
            session.context = {}

        return session.context


    @classmethod
    def initialize(cls, session):

        context = cls.context(session)

        #
        # General state
        #

        context.setdefault(
            "authenticated",
            True,
        )

        context.setdefault(
            "profile_completed",
            False,
        )

        #
        # Onboarding
        #

        context.setdefault(
            "onboarding",
            {
                "active": True,
                "step": OnboardingStep.WELCOME,
            },
        )

        #
        # Wallet Flow
        #

        context.setdefault(
            "wallet",
            {
                "active": False,
                "step": None,
            },
        )

        #
        # Stokvel Flow
        #

        context.setdefault(
            "stokvel",
            {
                "active": False,
                "step": None,
            },
        )

        #
        # KYC Flow
        #

        context.setdefault(
            "kyc",
            {
                "active": False,
                "step": None,
            },
        )

        #
        # Investment Flow
        #

        context.setdefault(
            "investment",
            {
                "active": False,
                "step": None,
            },
        )

        return context

    ##########################################################################
    #
    # Onboarding
    #
    ###########################################################################

    @classmethod
    def onboarding_active(cls, session):
        context = cls.initialize(session)
        return context["onboarding"]["active"]

    @classmethod
    def onboarding_step(cls, session):
        context = cls.initialize(session)
        return context["onboarding"]["step"]

    @classmethod
    def set_onboarding_step(cls, session, step):
        context = cls.initialize(session)
        context["onboarding"]["step"] = step
        return step

    @classmethod
    def complete_onboarding(cls, session):
        context = cls.initialize(session)
        context["profile_completed"] = True
        context["onboarding"]["active"] = False
        context["onboarding"]["step"] = None

    ###############################################################################
    #
    # Wallet Flow
    #
    ###############################################################################

    @classmethod
    def start_wallet(cls, session, step=None):
        context = cls.initialize(session)
        context["wallet"]["active"] = True
        context["wallet"]["step"] = step

    @classmethod
    def wallet_step(cls, session):
        context = cls.initialize(session)
        return context["wallet"]["step"]

    @classmethod
    def set_wallet_step(cls, session, step):
        context = cls.initialize(session)
        context["wallet"]["step"] = step

    @classmethod
    def finish_wallet(cls, session):
        context = cls.initialize(session)
        context["wallet"]["active"] = False
        context["wallet"]["step"] = None

    ##############################################################################
    #
    # Stokvel Flow
    #
    #############################################################################

    @classmethod
    def start_stokvel(cls, session, step=None):
        context = cls.initialize(session)
        context["stokvel"]["active"] = True
        context["stokvel"]["step"] = step

    @classmethod
    def finish_stokvel(cls, session):
        context = cls.initialize(session)
        context["stokvel"]["active"] = False
        context["stokvel"]["step"] = None

    ####################################################################################
    #
    # KYC Flow
    #
    ###################################################################################

    @classmethod
    def start_kyc(cls, session, step=None):
        context = cls.initialize(session)

        context["kyc"]["active"] = True
        context["kyc"]["step"] = step

    @classmethod
    def finish_kyc(cls, session):
        context = cls.initialize(session)
        context["kyc"]["active"] = False
        context["kyc"]["step"] = None

    ################################################################################
    #
    # Investment Flow
    #
    #################################################################################

    @classmethod
    def start_investment(cls, session, step=None):
        context = cls.initialize(session)
        context["investment"]["active"] = True
        context["investment"]["step"] = step

    @classmethod
    def finish_investment(cls, session):
        context = cls.initialize(session)
        context["investment"]["active"] = False
        context["investment"]["step"] = None

    @classmethod
    def profile_completed(cls, session):
        context = cls.initialize(session)
        return context["profile_completed"]
