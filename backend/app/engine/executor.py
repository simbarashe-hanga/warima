# backend/app/engine/executor.py
from app.services.payments.transaction_service import create_or_get_transaction
from app.services.identity.session_manager import SessionManager


def handle_intent(intent_data, user, session, member_account, db):
    intent = intent_data.get("intent")

    #
    # Default response
    #

    response = "Sorry, I don't understand."

    ####################################################################
    # Greeting
    ####################################################################

    if intent == "greeting":
        return "Hey! Type 'Contribute' or 'Agent' to get started"

    ####################################################################
    # Contribution
    ####################################################################

    if intent == "start_contribution":
        SessionManager.start_wallet(
            session,
            step="awaiting_amount",
        )

        return "How much would you like to contribute?"

    ###################################################################
    # AI Agent
    ###################################################################

    if intent == "agent":
        SessionManager.start_wallet(
            session,
            step="chatting",
        )

        return "You are chatting with the Warima AI Agent."

    ###################################################################
    # Portfolio
    ###################################################################
    
    if intent == "portfolio":
        return _handle_portfolio(
            user=user,
            member_account=member_account,
        )

    ###################################################################
    # Pigs
    ###################################################################

    if intent == "pigs":
        return _handle_pigs(user)

    ###################################################################
    # Buy Pig
    ###################################################################

    if intent == "buy_pig":
        return _handle_buy_pig(user, intent_data)

    ###################################################################
    # Contribution Amount
    ###################################################################

    if intent == "provide_amount":
        amount = intent_data.get("amount")
        context = SessionManager.context(session)
        context["wallet"]["amount"] = amount

        SessionManager.set_wallet_step(
            session,
            "awaiting_confirmation",
        )

        return f"Confirm R{amount}? Reply 1 to confirm, 2 to cancel."

    ####################################################################
    # Confirm
    ####################################################################

    if intent == "confirm":
        context = SessionManager.context(session)
        amount = context["wallet"].get("amount")

        if not amount:
            return (
                "No contribution amount found.\n"
                "Type 'contribute' to start again."
            )

        txn = create_or_get_transaction(
                db=db,
                user_id=user.id,
                amount=amount,
        )

        SessionManager.finish_wallet(session)

        return (
            f"Contribution of R{amount} received.\n"
            f"Transaction ID: {txn.id}"
        )

    ########################################################################
    # Cancel
    ########################################################################

    if intent == "cancel":
        SessionManager.finish_wallet(session)
        return "Cancelled. Type 'contribute' to start again"

    ##########################################################################
    # Unknown
    ##########################################################################

    return response

##############################################################################
# Blockchain Helpers
##############################################################################

def _handle_portfolio(user, member_account):
    """Handle portfolio command"""
    return (
        "*Your Portfolio*\n\n"
        f"Account: {member_account.account_number}\n"
        f"Account status: {member_account.status.value}\n\n"
        "Wallet information is not available yet."
    )

def _handle_pigs(user):
    """Handle pigs command"""
    # This would call the blockchain
    return (
        "*Your Pigs*\n\n"
        "You currently have no pigs.\n"
        "Type 'Buy [amount]' to invest in a pig!\n\n "
        "Example: BUY 1500"
    )

def _handle_buy_pig(user, intent_data):
    """Handle buy pig command"""
    amount = intent_data.get("amount", 0)

    if amount <= 0:
        return (
            "*Buy a Pig*\n\n"
            "To buy a pig, type: BUY [amount]\n"
            "Example: Buy 1500 (for R1500)\n\n"
            "What breed would you like? (Large White, Duroc, Landrace)"
        )

    return (
        f"*Investing R{amount} in a new pig\n\n"
        f"1. This will create a new pig on the blockchain\n"
        f"2. You'll receive shares based on your investment\n"
        f"3. The pig will be tracked on the blockchain\n\n"
        "Reply 'Confirm' to proceed or 'Cancel' to cancel."
    )

