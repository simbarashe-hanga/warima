from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os

load_dotenv()

client = InferenceClient(api_key=os.getenv("HF_API_TOKEN"))

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
for message in client.chat_completion(
    model="meta-llama/Llamma-3-8B-Instruct",
    messages=[{"role": "user", "content": ""}],
    stream=True,
):
    print(message.choices[0].delta.content, end="")
