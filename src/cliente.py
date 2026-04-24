import os
import socket
from enum import Enum
from typing import Any
from dotenv import load_dotenv

load_dotenv()


class Provider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    LMSTUDIO = "lmstudio"


class Config:
    """Configuración centralizada."""
    
    PROVIDER = os.getenv("NLP_PROVIDER", "ollama").lower()
    
    # Modelos por proveedor
    MODEL_OLLAMA = os.getenv("NLP_MODEL_OLLAMA", "llama3.2")
    MODEL_LMSTUDIO = os.getenv("NLP_MODEL_LMSTUDIO", "tinyllama-1.1b-chat-v1.0")
    MODEL_OPENAI = os.getenv("NLP_MODEL_OPENAI", "gpt-4o-mini")
    MODEL_HF = os.getenv("NLP_MODEL_HF", "meta-llama/Llama-3.2-8B-Instruct")
    
    # URLs
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
    LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
    HF_ENDPOINT = os.getenv("HF_ENDPOINT", "")
    
    # Claves
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    HF_TOKEN = os.getenv("HF_TOKEN", "")


def get_provider() -> Provider:
    try:
        return Provider(Config.PROVIDER)
    except ValueError:
        return Provider.OLLAMA


def get_client() -> Any:
    provider = get_provider()
    
    if provider == Provider.OLLAMA:
        return _get_ollama_client()
    elif provider == Provider.OPENAI:
        return _get_openai_client()
    elif provider == Provider.HUGGINGFACE:
        return _get_huggingface_client()
    elif provider == Provider.LMSTUDIO:
        return _get_lmstudio_client()
    
    return _get_ollama_client()


def _get_ollama_client():
    from openai import OpenAI
    
    if not is_ollama_available():
        raise RuntimeError("Ollama no está disponible. Ejecuta 'ollama serve'")
    
    return OpenAI(
        base_url=Config.OLLAMA_URL,
        api_key=Config.OLLAMA_API_KEY
    )


def _get_openai_client():
    from openai import OpenAI
    
    if not Config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY no configurada")
    
    return OpenAI(api_key=Config.OPENAI_API_KEY)


def _get_huggingface_client():
    from huggingface_hub import InferenceClient
    
    return InferenceClient(
        token=Config.HF_TOKEN,
        endpoint=Config.HF_ENDPOINT or None
    )


def _get_lmstudio_client():
    from openai import OpenAI
    
    return OpenAI(
        base_url=Config.LMSTUDIO_URL,
        api_key="lm-studio"
    )


def is_ollama_available() -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(("localhost", 11434))
        sock.close()
        return True
    except (socket.error, OSError):
        return False


def is_lmstudio_available() -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(("localhost", 1234))
        sock.close()
        return True
    except (socket.error, OSError):
        return False


def get_modelo() -> str:
    """Retorna el modelo según el proveedor."""
    provider = get_provider()
    
    if provider == Provider.OLLAMA:
        return Config.MODEL_OLLAMA
    elif provider == Provider.LMSTUDIO:
        return Config.MODEL_LMSTUDIO
    elif provider == Provider.OPENAI:
        return Config.MODEL_OPENAI
    elif provider == Provider.HUGGINGFACE:
        return Config.MODEL_HF
    
    return Config.MODEL_OLLAMA


def get_provider_name() -> str:
    return get_provider().value