from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_client():
    """Inicializa el cliente NLP兼容性 (OpenAI/Ollama).
    
    Returns:
        OpenAI: Cliente configurado para Ollama o OpenAI
    """
    from openai import OpenAI
    
    ollama_url = "http://localhost:11434/v1"
    ollama_key = "ollama"
    openai_key = __import__("os")..getenv("OPENAI_API_KEY")
    
    if _check_ollama():
        return OpenAI(base_url=ollama_url, api_key=ollama_key)
    
    return OpenAI(api_key=openai_key)


def _check_ollama() -> bool:
    """Verifica si Ollama está disponible."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect(("localhost", 11434))
        sock.close()
        return True
    except:
        return False


def get_modelo() -> str:
    """Retorna el modelo a usar."""
    import os
    return os.getenv("MODELO_NLP", "qwen2.5:0.5b")