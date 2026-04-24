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


class Config:
    """Configuración centralizada."""
    
    PROVIDER = os.getenv("NLP_PROVIDER", "ollama").lower()
    MODEL = os.getenv("NLP_MODEL", "qwen2.5:0.5b")
    
    # Ollama
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # HuggingFace
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    HF_ENDPOINT = os.getenv("HF_ENDPOINT", "")


def get_provider() -> Provider:
    """Obtiene el proveedor configurado."""
    try:
        return Provider(Config.PROVIDER)
    except ValueError:
        return Provider.OLLAMA


def get_client() -> Any:
    """Factory de clientes NLP.
    
    Retorna el cliente sesuai según la configuración.
    """
    provider = get_provider()
    
    if provider == Provider.OLLAMA:
        return _get_ollama_client()
    elif provider == Provider.OPENAI:
        return _get_openai_client()
    elif provider == Provider.HUGGINGFACE:
        return _get_huggingface_client()
    
    return _get_ollama_client()


def _get_ollama_client():
    """Cliente para Ollama local."""
    from openai import OpenAI
    
    if not is_ollama_available():
        raise RuntimeError("Ollama no está disponible. Ejecuta 'ollama serve'")
    
    return OpenAI(
        base_url=Config.OLLAMA_URL,
        api_key=Config.OLLAMA_API_KEY
    )


def _get_openai_client():
    """Cliente para OpenAI cloud."""
    from openai import OpenAI
    
    if not Config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY no configurada")
    
    return OpenAI(api_key=Config.OPENAI_API_KEY)


def _get_huggingface_client():
    """Cliente para HuggingFace Inference API."""
    from huggingface_hub import InferenceClient
    
    return InferenceClient(
        token=Config.HF_TOKEN,
        endpoint=Config.HF_ENDPOINT or None
    )


def is_ollama_available() -> bool:
    """Verifica si Ollama está corriendo."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(("localhost", 11434))
        sock.close()
        return True
    except (socket.error, OSError):
        return False


def get_modelo() -> str:
    """Retorna el modelo configurado."""
    return Config.MODEL


def get_provider_name() -> str:
    """Retorna el nombre del proveedor."""
    return get_provider().value