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
    ) -> str:

        history = history or []

        messages = [
            {
                "role": "system",
                "content": WARIMA_SYSTEM_PROMPT,
            }
        ]

        for message in history:

            role = message["role"]

            if role not in (
                "system",
                "user",
                "assitant",
            ):
                role = "user"

            messages.append(
                {
                    "role": "user",
                    "content": user_message,
                }
            )

            print("=" * 60)
            print("HF MODEL:", os.getenv("HF_MODEL"))
            print("MESSAGE COUNT:", len(messages))
            print("=" * 60)

            response = await client.chat_completion(
                model=os.getenv("HF_MODEL"),
                messages=messages,
                temperature=0.6,
                max_tokens=250,
            )

            return (
                response
                .choices[0]
                .message
                .content
                .strip()
            )
