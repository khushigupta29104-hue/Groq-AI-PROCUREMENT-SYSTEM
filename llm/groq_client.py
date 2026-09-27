"""
groq_client.py
================
Thin wrapper around LangChain's ChatGroq class. Groq hosts open-weight
models (Llama 3.3, etc.) on custom LPU hardware, giving very fast
inference and a generous free tier that (unlike some providers) does
not aggressively restrict brand-new accounts.

All prompt construction stays OUTSIDE this file (see prompts/ and
llm/prompt_runner.py) -- this module only knows how to talk to Groq.

Requires GROQ_API_KEY to be set in the environment (loaded from .env
via python-dotenv in frontend/app.py). Get a free key at:
https://console.groq.com/keys
"""

import os
from functools import lru_cache

from langchain_groq import ChatGroq

from llm.llm_config import get_llm_settings
from utils.logger import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    """Returns a cached ChatGroq instance configured from system_config.json + GROQ_API_KEY."""
    cfg = get_llm_settings()
    api_key = os.environ.get("GROQ_API_KEY", "")
    logger.info("Initializing ChatGroq model='%s'", cfg["llm_model"])
    return ChatGroq(
        model=cfg["llm_model"],
        api_key=api_key,
        temperature=cfg["temperature"],
        max_tokens=cfg["max_output_tokens"],
        timeout=cfg["request_timeout_seconds"],
    )


def generate(prompt: str) -> str:
    """
    Sends `prompt` to the Groq API and returns the plain text response.

    Raises:
        RuntimeError: if the Groq API is unreachable, the API key is
            invalid/missing, or a rate-limit error occurs.
    """
    llm = get_llm()
    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)
    except Exception as exc:  # noqa: BLE001
        logger.error("Groq generation failed: %s", exc)
        raise RuntimeError(
            "Could not reach the Groq API. Please check that GROQ_API_KEY is set correctly "
            "in your .env file and that you have not exceeded your API rate limit."
        ) from exc


def health_check() -> bool:
    """
    Verifies the Groq API is reachable and the API key is valid by
    sending a minimal test prompt. Used by the sidebar's connection
    status indicator (cached for a few minutes to avoid burning quota).
    """
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return False
    try:
        llm = get_llm()
        llm.invoke("ping")
        return True
    except Exception:  # noqa: BLE001
        return False
