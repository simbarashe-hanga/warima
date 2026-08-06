class FlowRouter:

    @staticmethod
    def current_flow(session):
        context = session.context or {}

        #
        # Active onboarding
        #

        onboarding = context.get("onboarding", {})

        if onboarding.get("active"):
            return "onboarding"

        #
        # Wallet flow
        #

        wallet = context.get("wallet")

        if wallet.get("active"):
            return "wallet"

        #
        # Stokvel flow
        #

        stokvel = context.get("stokvel")

        if stokvel.get("active"):
            return "stokvel"

        #
        # Investments
        #

        investment = context.get("investment", {})

        if investment.get("active"):
            return "investment"

        #
        # KYC
        #

        kyc = context.get("kyc", {})

        if kyc.get("active"):
            return "kyc"

        return "default"
