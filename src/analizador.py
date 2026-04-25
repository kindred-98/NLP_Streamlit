from src.niveles import analisis_unificado


def analizar_texto(texto: str, modelo: str = None) -> dict:
    """Analisis rapido en 1 llamada.
    
    Args:
        texto: Texto a analizar
        modelo: Modelo a usar (opcional)
        
    Returns:
        dict: Resultados del analisis
    """
    if not texto or not texto.strip():
        raise ValueError("El texto no puede estar vacio")
    
    try:
        return analisis_unificado(texto, modelo=modelo)
    except Exception as e:
        return {
            "error": str(e),
            "sentimiento": {},
            "entidades": {},
            "intencion": {},
            "clasificacion": {},
            "resumen": {}
        }