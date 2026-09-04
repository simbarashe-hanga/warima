# backend/app/workers/worker.py

import asyncio
import traceback

from dotenv import load_dotenv

from app.db.session import SessionLocal

from app.services.identity.user_service import UserService
from app.services.identity.session_manager import SessionManager

from app.services.messaging.queue_service import (
    get_and_mark_processing,
    mark_done,
    mark_failed,
)

from app.services.messaging.conversation_service import (
    save_message,
)

from app.services.messaging.messaging_service import (
    send_message,
)

from app.engine.intent import detect_intent
from app.engine.flow_router import FlowRouter
from app.engine.wallet_engine import WalletEngine

from app.services.ai.agent_service import AgentService

from app.engine.stokvel_engine import StokvelEngine


load_dotenv()


# ============================================================================
# MESSAGE PROCESSING
# ============================================================================

async def process_message(db, event):
    """
    Process one queued WhatsApp message.

    Responsibilities:
        1. Authenticate the WhatsApp user
        2. Initialize session context
        3. Detect intent
        4. Route through FlowRouter
        5. Apply context updates
        6. Save conversation messages
        7. Commit database changes
        8. Send WhatsApp response

    Business logic belongs to engines/services.
    """

    message = event.payload

    # ------------------------------------------------------------------------
    # EXTRACT MESSAGE
    # ------------------------------------------------------------------------

    wa_id = message["user_id"]
    raw_text = message.get("text", "").strip()

    print("=" * 80)
    print("EVENT:", message)
    print("=" * 80)

    user_service = UserService(db)

    # ------------------------------------------------------------------------
    # AUTHENTICATE / LOAD USER
    # ------------------------------------------------------------------------

    auth = user_service.authenticate_whatsapp(wa_id)

    user = auth.user
    identity = auth.identity
    session = auth.session
    member_account = auth.member_account

    print("USER:", user.id)
    print("NEW USER:", auth.is_new)

    # ------------------------------------------------------------------------
    # CREATE FLOW ROUTER
    # ------------------------------------------------------------------------

    agent_service = AgentService()
    wallet_engine = WalletEngine()
    stokvel_engine = StokvelEngine()

    flow_router = FlowRouter(
        wallet_engine=wallet_engine,
        stokvel_engine=stokvel_engine,
        agent=agent_service,
    )

    try:

        # ====================================================================
        # SAVE USER MESSAGE
        # ====================================================================

        save_message(
            db,
            wa_id,
            "user",
            raw_text,
        )

        db.flush()

        # ====================================================================
        # ONBOARDING
        # ====================================================================

        if not SessionManager.profile_completed(session):

            print("FLOW: onboarding")
            print("MESSAGE:", raw_text)

            # ---------------------------------------------------------------
            # Import here so normal processing does not unnecessarily load
            # onboarding dependencies.
            # ---------------------------------------------------------------

            from app.services.identity.onboarding_service import (
                OnboardingService,
            )

            onboarding = OnboardingService(db)

            result = onboarding.process(
                user=user,
                session=session,
                member_account=member_account,
                message=raw_text,
            )

            # ---------------------------------------------------------------
            # OnboardingService normally returns an object with .message.
            # Support dict/string responses as well.
            # ---------------------------------------------------------------

            if isinstance(result, dict):

                response = result.get(
                    "message",
                    "",
                )

                context_update = result.get(
                    "context_update",
                    {},
                )

                if context_update:
                    SessionManager.update_context(
                        session,
                        context_update,
                    )

            elif hasattr(result, "message"):

                response = result.message

            else:

                response = str(result)

        # ====================================================================
        # NORMAL PROCESSING
        # ====================================================================

        else:

            # ---------------------------------------------------------------
            # INTENT DETECTION
            # ---------------------------------------------------------------

            intent = detect_intent(
                raw_text,
                session,
            )

            print("INTENT:", intent)

            # ---------------------------------------------------------------
            # ROUTER
            #
            # FlowRouter is now responsible for deciding which engine
            # handles the message.
            #
            # IMPORTANT:
            # intent MUST be passed here.
            # ---------------------------------------------------------------

            print("FLOW: router")
            print("MESSAGE:", raw_text)

            result = await flow_router.route(
                message=raw_text,
                intent=intent,
                session=session,
                member_context={
                    "user": user,
                    "identity": identity,
                    "member_account": member_account,
                },
                db=db,
            )

            print("FLOW ROUTER RESULT:", result)

            # ---------------------------------------------------------------
            # NORMALIZE ROUTER RESPONSE
            # ---------------------------------------------------------------

            if isinstance(result, dict):

                response = result.get(
                    "message",
                    "",
                )

                context_update = result.get(
                    "context_update",
                    {},
                )

                # -----------------------------------------------------------
                # Apply context returned by the engine.
                #
                # SessionManager owns session.context.
                # -----------------------------------------------------------

                if context_update:

                    SessionManager.update_context(
                        session,
                        context_update,
                    )

            else:

                response = str(result)

        # ====================================================================
        # SAFETY
        # ====================================================================

        if not response:

            response = (
                "Sorry, I couldn't process that request.\n\n"
                "Type *Help* to see what I can do."
            )

        # ====================================================================
        # SAVE ASSISTANT RESPONSE
        # ====================================================================

        save_message(
            db,
            wa_id,
            "assistant",
            response,
        )

        # ====================================================================
        # DEBUG SESSION BEFORE COMMIT
        # ====================================================================

        print("=" * 60)
        print("SESSION CONTEXT BEFORE COMMIT")
        print(session.context)
        print("=" * 60)

        # ====================================================================
        # COMMIT
        # ====================================================================

        db.commit()

        # Refresh after commit so we are looking at persisted state.

        db.refresh(session)

        print("=" * 60)
        print("SESSION CONTEXT AFTER COMMIT")
        print(session.context)
        print("=" * 60)

        # ====================================================================
        # SEND WHATSAPP MESSAGE
        # ====================================================================

        await send_message(
            wa_id,
            response,
        )

        print("=" * 60)
        print("MESSAGE SENT")
        print(response)
        print("=" * 60)

    except Exception:

        # ---------------------------------------------------------------
        # Roll back all database changes associated with this message.
        # ---------------------------------------------------------------

        db.rollback()

        raise


# ============================================================================
# WORKER LOOP
# ============================================================================

async def worker_loop():
    """
    Continuously process queued WhatsApp events.
    """

    print("Worker started...")

    while True:

        db = None

        try:

            # ---------------------------------------------------------------
            # Open a fresh DB session for each polling cycle.
            # ---------------------------------------------------------------

            db = SessionLocal()

            # ---------------------------------------------------------------
            # Retrieve the next queued event and mark it as processing.
            # ---------------------------------------------------------------

            event = get_and_mark_processing(db)

            if event:

                try:

                    # -------------------------------------------------------
                    # Process message
                    # -------------------------------------------------------

                    await process_message(
                        db,
                        event,
                    )

                    # -------------------------------------------------------
                    # Mark queue event complete
                    # -------------------------------------------------------

                    mark_done(
                        db,
                        event,
                    )

                    # -------------------------------------------------------
                    # Commit queue status if mark_done does not commit itself.
                    # -------------------------------------------------------

                    db.commit()

                except Exception as e:

                    print("Worker error:", e)
                    traceback.print_exc()

                    # -------------------------------------------------------
                    # Roll back any failed message transaction.
                    # -------------------------------------------------------

                    db.rollback()

                    # -------------------------------------------------------
                    # Mark event failed.
                    # -------------------------------------------------------

                    try:

                        mark_failed(
                            db,
                            event,
                            traceback.format_exc(),
                        )

                        db.commit()

                    except Exception:

                        db.rollback()

                        print(
                            "Failed to mark event as failed:"
                        )

                        traceback.print_exc()

        except Exception as e:

            print("Database unavailable:", e)
            traceback.print_exc()

        finally:

            if db:

                db.close()

        # --------------------------------------------------------------------
        # Prevent a tight polling loop.
        # --------------------------------------------------------------------

        await asyncio.sleep(1)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    asyncio.run(worker_loop())
