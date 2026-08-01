from dotenv import load_dotenv
import asyncio
from app.db.session import SessionLocal
from app.services.user_service import UserService
from app.services.llm_service import chat


from app.services.queue_service import (
    get_and_mark_processing,
    mark_done,
    mark_failed,
)

from app.services.conversation_service import (
    save_message,
    get_recent_messages,
)

from app.services.messaging_service import send_message
from app.engine.intent import detect_intent
from app.engine.executor import handle_intent
#from app.models.user_session import UserSession

load_dotenv()

async def process_message(db, event):
    message = event.payload

    # WhatsApp sender
    wa_id = message["user_id"]
    text = message.get("text", "").lower()

    print("EVENT:", message)
    print("USER:", wa_id)
    print("TEXT:", text)

    # Load session or create session
    user_service = UserService(db)

    auth = user_service.authenticate_whatsapp(wa_id)

    user = auth.user
    identity = auth.identity
    session = auth.session

    print("USER ID:", user.id)
    print("NEW USER:", auth.is_new)

    context = session.context or {}

    save_message(
        db,
        wa_id,
        "user",
        text,
    )


    # Intent detection
    intent_data = detect_intent(
        text,
        context,
    )

    print("INTENT:", intent_data)

    if intent_data["intent"] == "unknown":

        print("ROUTING TO LLM")

        history = get_recent_messages(
            db,
            wa_id,
            limit=10,
        )
        print("=" * 60)
        print("HISTORY LENGTH:", len(history))

        for i, msg in enumerate(history):
            print(i, msg)

        print("=" * 60)

        try:
            response = await chat(
                user_message=text,
                history=history,
            )

        except Exception as e:
            print("LLM ERROR:", e)

            response = (
                "Warima AI is temporarily unavailable."
                "Please try again shortly."
            )

        print("LLM RESPONSE:", response)

        new_context = context

    else:

        response, new_context, _ = handle_intent(
            intent_data,
            context,
            user.id,
            db,
        )

    save_message(
        db,
        wa_id,
        "assistant",
        response,
    )


    print("RESPONSE:", response)

    # Update context
    session.context = new_context or {}
    db.commit()

    # Send reply
    await send_message(
        wa_id,
        response,
    )


async def worker_loop():
    print("Worker started...")

    while True:
        db = None
        try:
            db = SessionLocal()

            event = get_and_mark_processing(db)

            if event:
                try:
                    await process_message(db, event)
                    mark_done(db, event)

                except Exception as e:
                    print("Worker error:", e)
                    mark_failed(db, event, str(e))

        except Exception as e:
            print("Database unavailable:", e)

        finally:
            if db:
                db.close()

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(worker_loop())
