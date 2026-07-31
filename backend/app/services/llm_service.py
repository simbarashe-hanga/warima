from dotenv import load_dotenv
import os

from app.services.llm.huggingface import chat as huggingface_chat
from app.services.llm.gemini import chat as gemini_chat
from app.services.llm.openai import chat as openai_chat

load_dotenv()


async def chat(
    user_message: str,
    history: list | None = None,
) -> str:

    provider = os.getenv("LLM_PROVIDER", "huggingface").lower().strip()

    if provider == "huggingface":
        return await huggingface_chat(user_message, history)

    if provider == "gemini":
        return await gemini_chat(user_message, history)

    if provider == "openai":
        return await openai_chat(user_message, history)

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")
