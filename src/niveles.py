from src.cliente import get_client, get_modelo
from src.utils import limpiar_respuesta_json

PROMPT_SENTIMIENTO = """Analiza el sentimiento del texto. Responde ÚNICAMENTE en formato JSON con:
- sentimiento: positivo, negativo o neutral
- puntuacion: número del 0 al 1
- emociones: lista de emocionesdetectadas
- confianza: número del 0 al 1"""

PROMPT_ENTIDADES = """Extrae todas las entidades del texto. Responde ÚNICAMENTE en formato JSON con:
- personas: lista de nombres de personas
- organizaciones: lista de empresas/instituciones
- lugares: lista de ubicaciones
- fechas: lista de fechas mencionadas
- cantidades: lista de números y precios
- otros: otros identificadores relevantes"""

PROMPT_INTENCION = """Detecta la intención del usuario. Responde ÚNICAMENTE en formato JSON con:
- intencion_principal: una de [informacion, compra, soporte, queja, sugerencia, otro]
- subcategoria: más específica
- urgencia: alta, media, baja
- accion_sugerida: qué debería hacer la aplicación"""

PROMPT_CLASIFICACION = """Clasifica el texto en las siguientes categorías. Responde ÚNICAMENTE en formato JSON con:
- tema: tecnico, facturacion, cuenta, producto, servicio_cliente, otro
- tipo: pregunta, queja, sugerencia, informacion, solicitud
- canal_adecuado: email, chat, telefono, automatico
- prioridad: 1 (urgente) a 5 (sin urgencia)"""

PROMPT_RESUMEN = {
    "ultracorto": "Resume en UNA frase corta.",
    "medio": "Resume en 3 puntos clave.",
    "detallado": "Haz un resumen estructurado con introducción, desarrollo y conclusión."
}


def _llamar_modelo(system_prompt: str, texto: str, max_tokens: int = 300) -> dict:
    """Llama al modelo y retorna la respuesta."""
    client = get_client()
    modelo = get_modelo()
    
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


def analizar_sentimiento(texto: str) -> dict:
    """Analiza el sentimiento del texto."""
    return _llamar_modelo(PROMPT_SENTIMIENTO, texto)


def extraer_entidades(texto: str) -> dict:
    """Extrae entidades del texto (NER)."""
    return _llamar_modelo(PROMPT_ENTIDADES, texto)


def detectar_intencion(texto: str) -> dict:
    """Detecta la intención del usuario."""
    return _llamar_modelo(PROMPT_INTENCION, texto)


def clasificar_texto(texto: str) -> dict:
    """Clasifica el texto en categorías."""
    return _llamar_modelo(PROMPT_CLASIFICACION, texto)


def resumir_texto(texto: str) -> dict:
    """Resume el texto en 3 niveles."""
    resultados = {}
    for nivel, prompt in PROMPT_RESUMEN.items():
        resultados[nivel] = _llamar_modelo(prompt, texto, max_tokens=300 if nivel == "detallado" else 150)
    return resultados