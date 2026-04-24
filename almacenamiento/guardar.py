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


def guardar_resultado(texto: str, resultados: dict) -> dict:
    """Guarda los resultados en txt y json.
    
    Args:
        texto: Texto analizado
        resultados: Diccionario con los análisis
        
    Returns:
        dict: Rutas donde se guardaron los archivos
    """
    _crear_carpetas()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"analisis_{timestamp}"
    
    ruta_txt = CARPETA_TXT / f"{base}.txt"
    ruta_json = CARPETA_JSON / f"{base}.json"
    
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write(f"TEXTO ANALIZADO:\n{texto}\n\n")
        f.write("=" * 50 + "\n")
        f.write("RESULTADOS:\n")
        f.write(json.dumps(resultados, indent=2, ensure_ascii=False))
    
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump({
            "texto": texto,
            "resultados": resultados,
            "timestamp": timestamp
        }, f, indent=2, ensure_ascii=False)
    
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