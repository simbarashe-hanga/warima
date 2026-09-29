import asyncio
import os

from dotenv import load_dotenv
from google import genai

from app.core.prompts import WARIMA_SYSTEM_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


async def chat(
    user_message: str,
    history: list | None = None,
    system_prompt: str | None = None,
) -> str:

    history = history or []

    gemini_history = []

    for message in history:

        role = message.get("role", "assistant")

        # Gemini uses "model" instead of "assistant"
        if role == "assistant":
            role = "model"

        if role not in ("user", "model"):
            continue

        gemini_history.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": message.get("content", "")
                    }
                ],
            }
        )

    chat = client.chats.create(
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash",
        ),
        history=gemini_history,
        config={
            "system_instruction": (
                system_prompt
                or WARIMA_SYSTEM_PROMPT
            ),
            "temperature": float(
                os.getenv("LLM_TEMPERATURE", "0.6")
            ),
            "max_output_tokens": int(
                os.getenv("LLM_MAX_TOKENS", "512")
            ),
        },
    )

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = await chat.send_message(
                user_message
            )

            return response.text.strip()

        except Exception as exc:

            error_text = str(exc)

            is_transient = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
            )

            if not is_transient:
                raise

            if attempt == max_retries - 1:
                raise

            wait_seconds = 2 ** attempt

            print(
                "=" * 80
            )
            print(
                "GEMINI TEMPORARY ERROR"
            )
            print(
                f"ATTEMPT: {attempt + 1}/{max_retries}"
            )
            print(
                f"RETRYING IN: {wait_seconds}s"
            )
            print(
                error_text
            )
            print(
                "=" * 80
            )

            await asyncio.sleep(
                wait_seconds
            )

    raise RuntimeError(
        "Gemini request failed after retries."
    )
