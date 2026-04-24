"""NLP Streamlit - Core modules."""

from src.cliente import (
    get_client,
    get_modelo,
    get_provider,
    get_provider_name,
    is_ollama_available,
    Config,
    Provider
)
from src.config import logger

__all__ = [
    "get_client",
    "get_modelo",
    "get_provider",
    "get_provider_name",
    "is_ollama_available",
    "Config",
    "Provider",
    "logger"
]