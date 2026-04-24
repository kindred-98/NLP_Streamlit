from pathlib import Path
import json
from datetime import datetime

RESULTADOS_DIR = Path("resultados")
CARPETA_JSON = RESULTADOS_DIR / "json"


def _listar_json() -> list:
    """Lista todos los archivos json en resultados."""
    if not CARPETA_JSON.exists():
        return []
    return sorted(CARPETA_JSON.glob("*.json"), reverse=True)


def listar_analisis() -> list:
    """Lista todos los análisis guardados.
    
    Returns:
        list: Lista de análisis con metadata
    """
    analisis = []
    for archivo in _listar_json():
        try:
            data = json.loads(archivo.read_text(encoding="utf-8"))
            analisis.append({
                "archivo": archivo.name,
                "timestamp": data.get("timestamp"),
                "texto": data.get("texto", "")[:100]
            })
        except:
            continue
    return analisis


def leer_json(nombre: str) -> dict:
    """Lee un archivo json específico.
    
    Args:
        nombre: Nombre del archivo
        
    Returns:
        dict: Contenido del archivo
    """
    ruta = CARPETA_JSON / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No encontrado: {nombre}")
    
    return json.loads(ruta.read_text(encoding="utf-8"))


def buscar_por_fecha(fecha: str) -> list:
    """Busca análisis por fecha (formato: YYYYMMDD).
    
    Args:
        fecha: Fecha a buscar
        
    Returns:
        list: Análisis encontrados
    """
    resultados = []
    for archivo in _listar_json():
        if fecha in archivo.name:
            resultados.append(json.loads(archivo.read_text(encoding="utf-8")))
    return resultados


def leer_ultimo() -> dict:
    """Lee el último análisis guardado.
    
    Returns:
        dict: Último análisis o dict vacío
    """
    archivos = _listar_json()
    if not archivos:
        return {}
    return json.loads(archivos[0].read_text(encoding="utf-8"))