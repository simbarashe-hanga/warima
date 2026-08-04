from dotenv import load_dotenv
import os

from app.services.llm.huggingface import chat as huggingface_chat
from app.services.llm.gemini import chat as gemini_chat
from app.services.llm.openai import chat as openai_chat

load_dotenv()


async def chat(
    user_message: str,
    history: list | None = None,
    system_prompt: str | None = None,
) -> str:

    provider = os.getenv("LLM_PROVIDER", "huggingface").lower().strip()

    if provider == "huggingface":
        return await huggingface_chat(
            user_message,
            history,
            system_prompt=system_prompt,
        )

    if provider == "gemini":
        return await gemini_chat(
            user_message,
            history,
            system_prompt=system_prompt,
        )

    if provider == "openai":
        return await openai_chat(
            user_message,
            history,
            system_prompt=system_prompt,
        )

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")
