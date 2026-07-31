from dotenv import load_dotenv
import os

from app.services.llm.together import chat as together_chat
from app.services.llm.gemini import chat as gemini_chat
from app.services.llm.openai import chat as openai_chat

load_dotenv()


async def chat(
    user_message: str,
    history: list | None = None,
):
    provider = os.getenv("LLM_PROVIDER", "together").lower()

    if provider == "together":
        return await together_chat(user_message, history)

    if provider == "gemini":
        return await gemini_chat(user_message, history)

    if provider == "openai":
        return await openai_chat(user_message, history)

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")
