from dotenv import load_dotenv

import traceback
import asyncio

from app.db.session import SessionLocal

from app.services.identity.user_service import UserService
from app.services.identity.session_manager import SessionManager
from app.services.identity.onboarding_service import OnboardingService
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.llm_service import chat

from app.services.messaging.queue_service import (
    get_and_mark_processing,
    mark_done,
    mark_failed,
)

from app.services.messaging.conversation_service import (
    save_message,
    get_recent_messages,
)

from app.services.messaging.messaging_service import send_message

from app.engine.intent import detect_intent
from app.engine.executor import handle_intent


load_dotenv()


async def process_message(db, event):
    message = event.payload

    #
    # WhatsApp sender
    #
    wa_id = message["user_id"]
    raw_text = message.get("text", "")
    intent_text = raw_text.lower().strip()


    print("=" * 80)
    print("EVENT:", message)
    print("=" * 80)

    #
    # Authenticate User
    #
    user_service = UserService(db)
    auth = user_service.authenticate_whatsapp(wa_id)

    user = auth.user
    identity = auth.identity
    session = auth.session
    member_account = auth.member_account

    print("USER:", user.id)
    print("NEW USER:", auth.is_new)

    #
    # Initialize session context
    #
    SessionManager.initialize(session)

    try:

        #################################################################
        # Save incoming message
        #################################################################

        user_message = save_message(
            db,
            wa_id,
            "user",
            raw_text,
        )

        db.flush()
    
        ################################################################
        # Onboarding
        ################################################################

        if not SessionManager.profile_completed(session):
            onboarding = OnboardingService(db)

            result = onboarding.process(
                user=user,
                session=session,
                member_account=member_account,
                message=raw_text,
            )

            response = result.message

        #################################################################
        # Normal Processing
        #################################################################

        else:
            intent = detect_intent(
                intent_text,
                session,
            )

            print("INTENT:", intent)

            #
            # Structured Intent
            #

            if intent["intent"] != "unknown":
                response = handle_intent(
                    intent_data=intent,
                    user=user,
                    session=session,
                    member_account=member_account,
                    db=db,
                )

            #
            # AI Conversation
            #

            else:
                print("ROUTING TO LLM")

                system_prompt = await ContextBuilder.build_system_prompt(
                    user=user,
                    identity=identity,
                    session=session,
                    member_account=member_account,
                )

                history = get_recent_messages(
                    db,
                    wa_id,
                    limit=10,
                    exclude_id=user_message.id,
                )

                response = await chat(
                    user_message=raw_text,
                    history=history,
                    system_prompt=system_prompt,
                )

        ############################################################################
        # Save assistant response
        ############################################################################

        save_message(
            db,
            wa_id,
            "assistant",
            response,
        )

        ##########################################################################
        # Commit everything once
        ##########################################################################
        
        print("=" * 60)
        print("SESSION CONTEXT BEFORE COMMIT")
        print(session.context)
        print("=" * 60)
        
        db.commit()

        db.refresh(session)

        print("=" * 60)
        print("SESSION CONTEXT AFTER COMMIT")
        print(session.context)
        print("=" * 60)

        ##########################################################################
        # Send WhatsApp message
        #########################################################################

        await send_message(
            wa_id,
            response,
        )

    except Exception:
        db.rollback()
        raise

async def worker_loop():
    print("Worker started...")
    while True:
        db = None
        try:
            db = SessionLocal()
            event = get_and_mark_processing(db)
            if event:
                try:
                    await process_message(
                        db,
                        event,
                    )

                    mark_done(
                        db,
                        event,
                    )

                except Exception as e:
                    print("Worker error:", e)
                    mark_failed(
                        db,
                        event,
                        traceback.format_exc(),
                    )

        except Exception as e:
            print("Database unavailable:", e)

        finally:
            if db:
                db.close()

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(worker_loop())
