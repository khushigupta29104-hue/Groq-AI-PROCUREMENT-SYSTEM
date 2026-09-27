"""
llm_config.py
==============
Central place defining which Groq model, temperature, and token
limits are used. Reads from config/system_config.json so switching
models is a config change, never a code change.
"""

from utils.config_loader import get_system_config


def get_llm_settings() -> dict:
    """Returns the 'groq' section of system_config.json."""
    return get_system_config()["groq"]
