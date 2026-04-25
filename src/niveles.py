from src.cliente import get_client, get_modelo, get_provider_name
from src.utils import limpiar_respuesta_json

PROMPT_SENTIMIENTO = """Responde SIEMPRE asi: {"sentimiento":"valor","puntuacion":0.0,"emociones":["a"],"confianza":0.0}
Valor de sentimiento debe ser: positivo, negativo o neutral
Valor de puntuacion entre 0 y 1
Valor de emociones entre corchetes
Ejemplo para pergunta técnica: {"sentimiento":"neutral","puntuacion":0.5,"emociones":["curiosidad"],"confianza":0.8}"""

PROMPT_ENTIDADES = """Responde SIEMPRE asi: {"personas":[],"organizaciones":[],"lugares":[],"fechas":[],"cantidades":[],"otros":[]}
Si mentionas Python, requests, HTTP, agregar a "otros"
Ejemplo: {"personas":[],"organizaciones":["empresa X"],"lugares":[],"fechas":["hoy"],"cantidades":["10"],"otros":["Python","HTTP","timeout"]}"""

PROMPT_INTENCION = """Responde SIEMPRE asi: {"intencion_principal":"","subcategoria":"","urgencia":"","accion_sugerida":""}
Urgencia debe ser: alta, media o baja
Intencion principal debe ser: informacion, compra, soporte, queja, sugerencia
Ejemplo pregunta técnica: {"intencion_principal":"informacion","subcategoria":"ayuda tecnica","urgencia":"media","accion_sugerida":"responder"}"""

PROMPT_CLASIFICACION = """Responde SIEMPRE asi: {"tema":"","tipo":"","canal_adecuado":"","prioridad":3}
Tema debe ser: tecnico, facturacion, cuenta, producto, servicio_cliente, otro
Tipo debe ser: pregunta, queja, sugerencia, informacion, solicitud
Canal debe ser: email, chat, telefono, automatico
Prioridad entre 1 y 5
Ejemplo pregunta técnica: {"tema":"tecnico","tipo":"pregunta","canal_adecuado":"chat","prioridad":3}"""

PROMPT_RESUMEN_MEDIO = "Responde solo con el resumen en maximo 3 frases."

# Prompt unificado para analisis completo en 1 llamada
PROMPT_UNIFICADO = """Analiza el siguiente texto y devuelve SOLO JSON con los campos exactos, sin texto adicional:
{"sentimiento": "positivo|negativo|neutral", "puntuacion": 0.0, "emociones": [], "confianza": 0.0}
{"personas": [], "organizaciones": [], "lugares": [], "fechas": [], "cantidades": [], "otros": []}
{"intencion_principal": "", "subcategoria": "", "urgencia": "", "accion_sugerida": ""}
{"tema": "", "tipo": "", "canal_adecuado": "", "prioridad": 1}
{"resumen": ""}
Responde SOLO JSON, sin explicaciones."""

# Cache desactivado temporalmente
_cache = {}


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
    # Cache desactivado - siempre analizar
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