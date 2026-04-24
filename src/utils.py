import json


def limpiar_respuesta_json(contenido: str) -> dict:
    """Limpia la respuesta del modelo y la parsea a JSON.
    
    Args:
        contenido: Respuesta cruda del modelo
        
    Returns:
        dict: Respuesta parseada a JSON
    """
    limpio = contenido.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(limpio)
    except json.JSONDecodeError:
        return {"error": "No se pudo parsear la respuesta", "raw": contenido}


def validar_texto(texto: str) -> bool:
    """Valida que el texto sea válido para análisis.
    
    Args:
        texto: Texto a validar
        
    Returns:
        bool: True si es válido
    """
    return bool(texto and texto.strip() and len(texto.strip()) > 3)


def formatear_resultado(resultado: dict) -> str:
    """Formatea un resultado como string legible.
    
    Args:
        resultado: Diccionario a formatear
        
    Returns:
        str: Resultado formateado
    """
    return json.dumps(resultado, indent=2, ensure_ascii=False)