import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from app.core.prompts import WARIMA_SYSTEM_PROMPT

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


async def chat(
    user_message: str,
    history: list | None = None,
    system_prompt: str | None = None,
) -> str:

    history = history or []

    messages = [
        {
            "role": "system",
            "content": system_prompt or WARIMA_SYSTEM_PROMPT,
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    response = await client.chat.completions.create(
        model=os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini",
        ),
        messages=messages,
        temperature=float(
            os.getenv("LLM_TEMPERATURE", "0.6")
        ),
        max_tokens=int(
            os.getenv("LLM_MAX_TOKENS", "250")
        ),
    )

    return response.choices[0].message.content.strip()
