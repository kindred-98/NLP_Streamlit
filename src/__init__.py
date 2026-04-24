"""NLP Streamlit - Módulo de análisis de texto."""

from src.niveles import (
    analizar_sentimiento,
    extraer_entidades,
    detectar_intencion,
    clasificar_texto,
    resumir_texto
)
from src.analizador import analizar_texto

__all__ = [
    "analizar_sentimiento",
    "extraer_entidades",
    "detectar_intencion",
    "clasificar_texto",
    "resumir_texto",
    "analizar_texto"
]