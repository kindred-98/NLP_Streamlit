from src.niveles import (
    analizar_sentimiento,
    extraer_entidades,
    detectar_intencion,
    clasificar_texto,
    resumir_texto
)


def analizar_texto(texto: str) -> dict:
    """Orquesta todos los análisis NLP sobre un texto.
    
    Args:
        texto: Texto a analizar
        
    Returns:
        dict: Resultados de todos los análisis
        
    Raises:
        ValueError: Si el texto está vacío
    """
    if not texto or not texto.strip():
        raise ValueError("El texto no puede estar vacío")
    
    return {
        "sentimiento": analizar_sentimiento(texto),
        "entidades": extraer_entidades(texto),
        "intencion": detectar_intencion(texto),
        "clasificacion": clasificar_texto(texto),
        "resumen": resumir_texto(texto)
    }