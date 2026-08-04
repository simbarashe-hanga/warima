import os

from dotenv import load_dotenv
from huggingface_hub import AsyncInferenceClient

from app.core.prompts import WARIMA_SYSTEM_PROMPT

load_dotenv()

client = AsyncInferenceClient(
    token=os.getenv("HF_TOKEN"),
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

    # Conversation history
    for message in history:

        role = message.get("role", "assistant")

        if role not in ("system", "user", "assistant"):
            role = "assistant"

        messages.append(
            {
                "role": role,
                "content": message.get("content", ""),
            }
        )

    # Latest user message
    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    print("=" * 80)
    print("HF MODEL:", os.getenv("HF_MODEL"))
    print("=" * 80)
    print(messages[0]["content"])
    print("=" * 80)
    print("MESSAGE COUNT:", len(messages))

    for i, m in enumerate(messages):
        print(f"{i}: {m['role']} -> {m['content']}")

    print("=" * 80)

    response = await client.chat_completion(
        model=os.getenv("HF_MODEL"),
        messages=messages,
        temperature=0.6,
        max_tokens=250,
    )

    return response.choices[0].message.content.strip()
