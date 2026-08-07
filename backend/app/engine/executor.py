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
