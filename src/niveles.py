from src.cliente import get_client, get_modelo, get_provider_name
from src.utils import limpiar_respuesta_json

PROMPT_SENTIMIENTO = """Analiza el sentimiento del texto. Responde UNICAMENTE en formato JSON con:
- sentimiento: positivo, negativo o neutral
- puntuacion: numero del 0 al 1
- emociones: lista de emociones detectadas
- confianza: numero del 0 al 1"""

PROMPT_ENTIDADES = """Extrae todas las entidades del texto. Responde UNICAMENTE en formato JSON con:
- personas: lista de nombres de personas
- organizaciones: lista de empresas/instituciones
- lugares: lista de ubicaciones
- fechas: lista de fechas mencionadas
- cantidades: lista de numeros y precios
- otros: otros identificadores relevantes"""

PROMPT_INTENCION = """Detecta la intension del usuario. Responde UNICAMENTE en formato JSON con:
- intencion_principal: una de [informacion, compra, soporte, queja, sugerencia, otro]
- subcategoria: mas especifica
- urgencia: alta, media, baja
- accion_sugerida: que deberia hacer la aplicacion"""

PROMPT_CLASIFICACION = """Clasifica el texto en las siguientes categorias. Responde UNICAMENTE en formato JSON con:
- tema: tecnico, facturacion, cuenta, producto, servicio_cliente, otro
- tipo: pregunta, queja, sugerencia, informacion, solicitud
- canal_adecuado: email, chat, telefono, automatico
- prioridad: 1 (urgente) a 5 (sin urgencia)"""

PROMPT_RESUMEN = {
    "ultracorto": "Resume en UNA frase corta.",
    "medio": "Resume en 3 puntos clave.",
    "detallado": "Haz un resumen estructurado con introduccion, desarrollo y conclusion."
}

PROMPT_RESUMEN_MEDIO = "Resume el texto en 3 puntos clave."

# Prompt unificado para analisis completo en 1 llamada
PROMPT_UNIFICADO = """Analiza el siguiente texto y devuelve UNICAMENTE un JSON con:

1. SENTIMIENTO (sentimiento, puntuacion 0-1, emociones, confianza 0-1)
2. ENTIDADES (personas, organizaciones, lugares, fechas, cantidades, otros)
3. INTENCION (intencion_principal, subcategoria, urgencia, accion_sugerida)
4. CLASIFICACION (tema, tipo, canal_adecuado, prioridad 1-5)
5. RESUMEN (ultracorto, medio, detallado)

Responde SOLO con JSON valido, sin texto adicional."""

# Cache para evitar analisis repetidos (se limpia automaticamente)
_cache = {}
_cache_modelo = None  # Para limpiar cache al cambiar modelo


def _es_respuesta_invalida(resultado: dict) -> bool:
    """Verifica si la respuesta tiene muchos N/A o esta vacia."""
    if not resultado:
        return True
    na_count = 0
    total = 0
    for v in resultado.values():
        if isinstance(v, str) and v in ("N/A", "n/a", ""):
            na_count += 1
        elif isinstance(v, list) and not v:
            na_count += 1
        total += 1
    return total > 0 and na_count / total > 0.5


def _llamar_modelo(system_prompt: str, texto: str, max_tokens: int = 300, modelo: str = None) -> dict:
    """Llama al modelo segun el proveedor configurado."""
    try:
        provider = get_provider_name()
        client = get_client()
        modelo_a_usar = modelo if modelo else get_modelo()
        
        if provider == "huggingface":
            return _call_huggingface(client, system_prompt, texto)
        
        response = client.chat.completions.create(
            model=modelo_a_usar,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto}
            ],
            temperature=0.0,
            max_tokens=max_tokens
        )
        
        contenido = response.choices[0].message.content
        return limpiar_respuesta_json(contenido)
        
    except Exception as e:
        return {"error": str(e)}


def _call_huggingface(client, system_prompt: str, texto: str) -> dict:
    """Llama a la API de HuggingFace."""
    prompt = f"System: {system_prompt}\nUser: {texto}"
    
    try:
        response = client.text_generation(
            prompt,
            model=get_modelo(),
            parameters={
                "max_new_tokens": 300,
                "temperature": 0.0
            }
        )
        return limpiar_respuesta_json(response)
    except Exception as e:
        return {"error": f"HuggingFace: {str(e)}"}


def analizar_sentimiento(texto: str, modelo: str = None) -> dict:
    """Analiza el sentimiento del texto."""
    return _llamar_modelo(PROMPT_SENTIMIENTO, texto, modelo=modelo)


def extraer_entidades(texto: str, modelo: str = None) -> dict:
    """Extrae entidades del texto (NER)."""
    return _llamar_modelo(PROMPT_ENTIDADES, texto, modelo=modelo)


def detectar_intencion(texto: str, modelo: str = None) -> dict:
    """Detecta la intension del usuario."""
    return _llamar_modelo(PROMPT_INTENCION, texto, modelo=modelo)


def clasificar_texto(texto: str, modelo: str = None) -> dict:
    """Clasifica el texto en categorias."""
    return _llamar_modelo(PROMPT_CLASIFICACION, texto, modelo=modelo)


def resumir_texto(texto: str, modelo: str = None) -> dict:
    """Resume el texto en 3 niveles."""
    return _llamar_modelo(PROMPT_RESUMEN_MEDIO, texto, max_tokens=300, modelo=modelo)


def analisis_unificado(texto: str, modelo: str = None) -> dict:
    """Analisis completo en 1 llamada (rapido).
    
    Args:
        texto: Texto a analizar
        modelo: Modelo a usar (opcional)
        
    Returns:
        dict con sentimiento, entidades, intencion, clasificacion, resumen
    """
    # Limpiar cache si cambio modelo
    global _cache_modelo
    if _cache_modelo != modelo:
        _cache = {}
        _cache_modelo = modelo
    
    # Verificar cache
    texto_hash = hash(texto)
    if texto_hash in _cache:
        return _cache[texto_hash]
    
    # Llamar modelo con prompt unificado
    resultado = _llamar_modelo(PROMPT_UNIFICADO, texto, max_tokens=1500, modelo=modelo)
    
    # Verificar respuesta valida o tiene muchos N/A
    if resultado.get("error") or _es_respuesta_invalida(resultado):
        return _analisis_individual(texto, modelo=modelo)
    
    # Estructurar respuesta
    analisis = {
        "sentimiento": {
            "sentimiento": resultado.get("sentimiento", "neutral"),
            "puntuacion": resultado.get("puntuacion", 0.5),
            "emociones": resultado.get("emociones", []),
            "confianza": resultado.get("confianza", 0.5)
        },
        "entidades": {
            "personas": resultado.get("personas", []),
            "organizaciones": resultado.get("organizaciones", []),
            "lugares": resultado.get("lugares", []),
            "fechas": resultado.get("fechas", []),
            "cantidades": resultado.get("cantidades", []),
            "otros": resultado.get("otros", [])
        },
        "intencion": {
            "intencion_principal": resultado.get("intencion_principal", "otro"),
            "subcategoria": resultado.get("subcategoria", ""),
            "urgencia": resultado.get("urgencia", "baja"),
            "accion_sugerida": resultado.get("accion_sugerida", "")
        },
        "clasificacion": {
            "tema": resultado.get("tema", "otro"),
            "tipo": resultado.get("tipo", "pregunta"),
            "canal_adecuado": resultado.get("canal_adecuado", "chat"),
            "prioridad": resultado.get("prioridad", 3)
        },
        "resumen": {
            "ultracorto": resultado.get("ultracorto", ""),
            "medio": resultado.get("medio", ""),
            "detallado": resultado.get("detallado", "")
        }
    }
    
    # Guardar en cache
    _cache[texto_hash] = analisis
    
    return analisis


def _analisis_individual(texto: str, modelo: str = None) -> dict:
    """Analisis individual (lento) - fallback si unificado falla."""
    from concurrent.futures import ThreadPoolExecutor
    
    # Usar el modelo seleccionado
    def call_with_modelo(func, texto):
        return func(texto)
    
    tareas = [
        lambda: (analizar_sentimiento(texto, modelo), "sentimiento"),
        lambda: (extraer_entidades(texto, modelo), "entidades"),
        lambda: (detectar_intencion(texto, modelo), "intencion"),
        lambda: (clasificar_texto(texto, modelo), "clasificacion"),
        lambda: (resumir_texto(texto, modelo), "resumen")
    ]
    
    resultados = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(tarea) for tarea in tareas]
        for future in futures:
            try:
                result, nombre = future.result()
                resultados[nombre] = result
            except Exception:
                resultados[nombre] = {}
    
    return resultados