from pathlib import Path
import json
from datetime import datetime

RESULTADOS_DIR = Path("resultados")
CARPETA_TXT = RESULTADOS_DIR / "txt"
CARPETA_JSON = RESULTADOS_DIR / "json"


def _crear_carpetas():
    """Crea las carpetas si no existen."""
    CARPETA_TXT.mkdir(parents=True, exist_ok=True)
    CARPETA_JSON.mkdir(parents=True, exist_ok=True)


def _formatear_txt(texto: str, resultados: dict, timestamp: str) -> str:
    """Formatea el resultado en TXT legible."""
    return f"""
============================================
ANALISIS NLP — {timestamp}
============================================

TEXTO ANALIZADO:
{texto}

RESULTADOS:
--------------------------------------------
SENTIMIENTO:    {resultados.get('sentimiento', {})}
ENTIDADES:      {resultados.get('entidades', {})}
INTENCION:      {resultados.get('intencion', {})}
RESUMEN:        {resultados.get('resumen', {})}
CLASIFICACION:  {resultados.get('clasificacion', {})}
"""


def guardar_resultado(texto: str, resultados: dict) -> dict:
    """Guarda los resultados en txt y json.
    
    Args:
        texto: Texto analizado
        resultados: Diccionario con los analisis
        
    Returns:
        dict: Rutas donde se guardaron los archivos
    """
    if not texto or not texto.strip():
        raise ValueError("El texto no puede estar vacio")
        
    _crear_carpetas()
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")
    base = f"analisis_{timestamp}"
    
    ruta_txt = CARPETA_TXT / f"{base}.txt"
    ruta_json = CARPETA_JSON / f"{base}.json"
    
    contenido_txt = _formatear_txt(texto, resultados, timestamp)
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write(contenido_txt.strip())
    
    data = {
        "timestamp": timestamp,
        "texto": texto,
        "resultados": resultados
    }
    
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return {"txt": str(ruta_txt), "json": str(ruta_json)}


def guardar_txt(texto: str, nombre: str = None) -> str:
    """Guarda solo un archivo txt.
    
    Args:
        texto: Contenido a guardar
        nombre: Nombre del archivo (opcional)
        
    Returns:
        str: Ruta donde se guardó
    """
    _crear_carpetas()
    
    if not nombre:
        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    ruta = CARPETA_TXT / f"{nombre}.txt"
    
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    
    return str(ruta)


def guardar_json(datos: dict, nombre: str = None) -> str:
    """Guarda solo un archivo json.
    
    Args:
        datos: Contenido a guardar
        nombre: Nombre del archivo (opcional)
        
    Returns:
        str: Ruta donde se guardó
    """
    _crear_carpetas()
    
    if not nombre:
        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    ruta = CARPETA_JSON / f"{nombre}.json"
    
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    return str(ruta)