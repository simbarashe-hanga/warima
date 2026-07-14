from dotenv import load_dotenv
from huggingface_hub import AsyncInferenceClient
import os


load_dotenv()


client = AsyncInferenceClient(
    api_key=os.getenv("HF_TOKEN"),
)

MODEL = os.getenv(
    "HF_MODEL",
    "meta-llama/Llama-3.3-70B-Instruct:together",
)

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

Keep replies under 80 words.

Use simple, friendly conversational language.
"""

async def chat(
    user_message: str,
    history: list | None = None,
):
    history = history or []

    try:
        completion = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                *history,
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            max_tokens=200,
            temperature=0.7,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"LLM Error: {e}")
        return (
            "I'm sorry, I'm having trouble processing your request at the moment. "
            "Please try again shortly."
        )
