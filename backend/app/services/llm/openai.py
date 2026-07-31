import os

from openai import AsyncOpenAI

from app.core.prompts import WARIMA_SYSTEM_PROMPT


client = AsyncOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


async def chat(
    user_message,
    history=None,
):
    history = history or []

    messages = [
        {
            "role": "system",
            "content": WARIMA_SYSTEM_PROMPT,
        }
    ]

    messages.extend(history


    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    response = await client.chat.completions.create(
        model=os.getenv("HF_MODEL"),
        messages=messages,
        temperature=0.6,
    )

    return response.choices[0].message.content
