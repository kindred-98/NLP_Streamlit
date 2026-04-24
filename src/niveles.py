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


def _llamar_modelo(system_prompt: str, texto: str, max_tokens: int = 300) -> dict:
    """Llama al modelo segun el proveedor configurado."""
    try:
        provider = get_provider_name()
        client = get_client()
        modelo = get_modelo()
        
        if provider == "huggingface":
            return _call_huggingface(client, system_prompt, texto)
        
        response = client.chat.completions.create(
            model=modelo,
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


def analizar_sentimiento(texto: str) -> dict:
    """Analiza el sentimiento del texto."""
    return _llamar_modelo(PROMPT_SENTIMIENTO, texto)


def extraer_entidades(texto: str) -> dict:
    """Extrae entidades del texto (NER)."""
    return _llamar_modelo(PROMPT_ENTIDADES, texto)


def detectar_intencion(texto: str) -> dict:
    """Detecta la intension del usuario."""
    return _llamar_modelo(PROMPT_INTENCION, texto)


def clasificar_texto(texto: str) -> dict:
    """Clasifica el texto en categorias."""
    return _llamar_modelo(PROMPT_CLASIFICACION, texto)


def resumir_texto(texto: str) -> dict:
    """Resume el texto en 3 niveles."""
    resultados = {}
    for nivel, prompt in PROMPT_RESUMEN.items():
        resultados[nivel] = _llamar_modelo(prompt, texto, max_tokens=300 if nivel == "detallado" else 150)
    return resultados