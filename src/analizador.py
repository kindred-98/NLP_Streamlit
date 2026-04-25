from concurrent.futures import ThreadPoolExecutor, as_completed
from src.niveles import (
    analizar_sentimiento,
    extraer_entidades,
    detectar_intencion,
    clasificar_texto,
    resumir_texto
)


def analizar_texto(texto: str) -> dict:
    """Orquesta todos los análisis NLP en paralelo.
    
    Args:
        texto: Texto a analizar
        
    Returns:
        dict: Resultados de todos los análisis
    """
    if not texto or not texto.strip():
        raise ValueError("El texto no puede estar vacio")
    
    resultados = {}
    errores = {}
    
    # Tareas a ejecutar en paralelo
    tareas = {
        "sentimiento": lambda: analizar_sentimiento(texto),
        "entidades": lambda: extraer_entidades(texto),
        "intencion": lambda: detectar_intencion(texto),
        "clasificacion": lambda: clasificar_texto(texto),
        "resumen": lambda: resumir_texto(texto)
    }
    
    # Ejecutar en paralelo (máximo 3 hilos simultáneos)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(tarea): nombre 
            for nombre, tarea in tareas.items()
        }
        
        for future in as_completed(futures):
            nombre = futures[future]
            try:
                resultados[nombre] = future.result()
            except Exception as e:
                errores[nombre] = str(e)
                resultados[nombre] = {"error": str(e)}
    
    return resultados