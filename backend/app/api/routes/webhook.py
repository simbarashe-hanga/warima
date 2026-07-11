import os

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.idempotency_service import is_duplicate, save_message
from app.services.queue_service import enqueue_event
from app.utils.extract_message import extract_message

router = APIRouter()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


@router.get("", response_class=PlainTextResponse)
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    print(
        "VERIFY:",
        hub_mode,
        hub_verify_token,
        VERIFY_TOKEN,
        hub_challenge,
    )

    if (
        hub_mode == "subscribe"
        and hub_verify_token == VERIFY_TOKEN
    ):
        return PlainTextResponse(hub_challenge)

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("")
async def receive_webhook(payload: dict, db: Session = Depends(get_db)):
    message = extract_message(payload)

    print("EXTRACTED:", message)

    if not message:
        print("NO MESSAGE")
        return {"status": "ignored"}

    print("CHECKING DUPLICATE")

    duplicate = is_duplicate(db, message["id"])
    print("DUPLICATE?", duplicate)

    if duplicate:
        return {"status": "duplicate"}

    print("SAVING MESSAGE")
    save_message(db, message["id"])

    print("ENQUEUEING")
    enqueue_event(db, message)

    print("DONE")

    return {"status": "queued"}


@router.get("/health")
def health(db: Session = Depends(get_db)):
    return {"status": "ok"}
