from src.cliente import get_client, get_modelo, get_provider_name
from src.utils import limpiar_respuesta_json
from concurrent.futures import ThreadPoolExecutor

# ========================================================
# PROMPTS - Mejorados para seguir instrucciones
# ========================================================

PROMPT_SENTIMIENTO = """Analiza el SENTIMIENTO DEL USUARIO, no la respuesta técnica.

guias:
- Si pregunta como "como hago...", "quiero saber...", "alguien sabe..." = NEUTRAL (busca info)
- Si dice "gracias", "perfecto", "excelente" = POSITIVO (agradecimiento)
- Si dice "molesto", "vergüenza", "nadie responde" = NEGATIVO (frustracion)
- Si dice "urgente", "ahora" = URGENCIA (alta prioridad)

Responde SIEMPRE en JSON exacto:
{"sentimiento":"neutral|positivo|negativo","puntuacion":0.0,"emociones":["principal"],"confianza":0.0}

Ejemplos:
- "Hola alguien sabe como configurar timeout?" = {"sentimiento":"neutral","puntuacion":0.5,"emociones":["curiosidad"],"confianza":0.9}
- "Muchas gracias! funciono perfectly" = {"sentimiento":"positivo","puntuacion":0.9,"emociones":["gratitud","alivio"],"confianza":0.95}
- "Llevo 3 dias esperando y nadie responde" = {"sentimiento":"negativo","puntuacion":0.7,"emociones":["frustracion","impaciencia"],"confianza":0.9}"""

PROMPT_ENTIDADES = """Extrae solo DATOS TECNICOS del texto. No inventes nada.

guias:
- tecnologias: Python, JavaScript, SQL, HTML, Docker, React, etc.
- conceptos: timeout, API, BASE DE DATOS, JWT, CACHE, SESION, etc.
- productos: nombres de software, librerias, paquetes (requests, pandas, numpy)
- numeros: versiones, puertos, tiempos, cantidades mencionadas
- errores: si menciona errores, copialos tal cual

Responde SIEMPRE en JSON exacto:
{"personas":[],"organizaciones":[],"lugares":[],"fechas":[],"cantidades":[],"otros":[]}

Ejemplo pregunta sobre timeout:
{"personas":[],"organizaciones":[],"lugares":[],"fechas":["10 segundos"],"cantidades":["10"],"otros":["Python","requests","HTTP","timeout"]}"""

PROMPT_INTENCION = """Detect que QUIERE HACER el usuario.

guias:
- "como hago", "quiero saber", "alguien sabe" = INFORMACION (ayuda tecnica)
- "no funciona", "error", "no anda" = SOPORTE (problema)
- "quiero comprar", "precios", "cuesta" = COMPRA
- "queja", "muy molesto", "nadie responde" = QUEJA
- "sugerencia", "podrian", "mejor si" = SUGERENCIA

Responde SIEMPRE en JSON exacto:
{"intencion_principal":"informacion|soporte|compra|queja|sugerencia","subcategoria":"","urgencia":"alta|media|baja","accion_sugerida":""}

Ejemplos:
- "alguien sabe configurar timeout?" = {"intencion_principal":"informacion","subcategoria":"configuracion tecnica","urgencia":"baja","accion_sugerida":"explicar con ejemplos"}
- "mi pedido no llego" = {"intencion_principal":"soporte","subcategoria":"entrega","urgencia":"alta","accion_sugerida":"verificar estado"}"""

PROMPT_CLASIFICACION = """Clasifica el TICKET basado en CONTENIDO y URGENCIA.

guias para TEMA:
- duda técnica, código, programación = TECNICO
- facturas, pagos, dinero = FACTURACION  
- login, cuenta, password, perfil = CUENTA
- producto calidad, entrega = PRODUCTO
- soporte, ayuda, nadie responde = SERVICIO_CLIENTE
- lo demas = OTRO

guias para PRIORIDAD:
- urgencia alta palabras: urgente, ahora, rápido, crítico = PRIORIDAD 1
- palabras medianas: importante, necesito, proyecto = PRIORIDAD 2-3  
- palabras suaves: consulta, alguien sabe, quiero info = PRIORIDAD 4-5

Responde SIEMPRE en JSON exacto:
{"tema":"tecnico|facturacion|cuenta|producto|servicio_cliente|otro","tipo":"pregunta|queja|sugerencia|informacion|solicitud","canal_adecuado":"email|chat|telefono|automatico","prioridad":1-5}

Ejemplo pregunta técnica:
{"tema":"tecnico","tipo":"pregunta","canal_adecuado":"chat","prioridad":3}"""

PROMPT_RESUMEN_CORTO = """Responde en UNA sola frase lo que necesitas hacer. Máx 10 palabras."""

PROMPT_RESUMEN_MEDIO = """Eres un PROFESOR amigable. Explica la solución AL USUARIO como si fuera un amigo.

FORMATO:
1. **Qué problema tienes**: Resumen en 1 línea
2. **SOLUCIÓN**: Código funcional
3. **Alternativa**: Si existe

Responde en español claro."""

PROMPT_RESUMEN_DETALLADO = """Eres un PROFESOR TÉCNICO experto. El usuario tiene una duda/ problema y necesita-entender la solución COMPLETA.

ESTRUCTURA OBLIGATORIA:
1. **QUÉ PROBLEMA TIENES**: Resumen en 1 línea (qué intenta hacer)
2. **POR QUÉ OCURRE**: Explicación técnica simple (máx 2 líneas)
3. **SOLUCIÓN PRINCIPAL**: Código funcional completo con comentarios
4. **EJEMPLO COMPLETO**: Caso de uso real ejecutable
5. **ALTERNATIVAS**: Otras formas de resolverlo (si existen)
6. **WARNINGS**: Cosas importantes a tener cuidado
7. **RECURSOS EXTRA**: Links o docs si relevante

.guias:
- Usa markdown para código (```python)
- Sé detallado pero claro
- El usuario necesita entender DE VERDAD
- Agrega comentarios en el código
- Si hay errores comunes, adviertelos

Idioma: Español claro, sin tecnicismos innecesarios."""

# ========================================================
# FUNCIONES DE ANALISIS
# ========================================================

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
    return _llamar_modelo(PROMPT_RESUMEN_MEDIO, texto, modelo=modelo)


# ========================================================
# ANALISIS PRINCIPAL
# ========================================================

def analisis_unificado(texto: str, modelo: str = None) -> dict:
    """Usa analisis individual que funciona mejor."""
    return _analisis_individual(texto, modelo=modelo)


def _analisis_individual(texto: str, modelo: str = None) -> dict:
    """Analisis con 5 llamadas separadas (mas preciso)."""
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