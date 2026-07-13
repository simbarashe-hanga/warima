from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are Warima.

Warima is an AI-powered Stokvel assistant on WhatsApp.

You help users:

- save money consistently
- understand contributions
- understand withdrawals
- build healthy financial habits

You may explain actions.

You may not execute transactions.

Never invent:
- balances
- contributions
- withdrawals

Keep replies under 80 words

Use simple, friendly conversational language.
"""


async def chat(
    user_message: str,
    history: list | None = None
):
    """
    history should look like:

    [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."},
    ]
    """

    history = history or []

    # Convert history into Gemini chat history
    gemini_history = []

    for message in history:
        role = message["role"]

        # Gemini uses "model" instead of "assistant"
        if role == "assistant":
            role = "model"

        gemini_history.append(
            {
                "role": role,
                "parts": [{"text": message["content"]}],
            }
        )

    chat = client.chats.create(
        model="gemini-2.5-flash",
        history=gemini_history,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 0.6,
        },
    )

    response = chat.send_message(user_message)

    return response.text
