import json
import re

# Pares clave/valor separados por '|' que aparecen en respuestas no estructuradas.
CAMPOS_FALLBACK = {
    'sentimiento': r'sentimiento["\s]*:["\s]*(\w+)',
    'puntuacion': r'puntuacion["\s]*:["\s]*([0-9.]+)',
    'emociones': r'emociones["\s]*:["\s]*\[(.*?)\]',
    'confianza': r'confianza["\s]*:["\s]*([0-9.]+)',
    'personas': r'personas["\s]*:["\s]*\[(.*?)\]',
    'lugares': r'lugares["\s]*:["\s]*\[(.*?)\]',
    'intencion_principal': r'intencion_principal["\s]*:["\s]*(\w+)',
    'subcategoria': r'subcategoria["\s]*:["\s]*"?([^",\n]+)"?',
    'urgencia': r'urgencia["\s]*:["\s]*(\w+)',
    'tema': r'tema["\s]*:["\s]*"?([^",\n]+)"?',
    'tipo': r'tipo["\s]*:["\s]*"?([^",\n]+)"?',
    'canal_adecuado': r'canal_adecuado["\s]*:["\s]*"?([^",\n]+)"?',
    'prioridad': r'prioridad["\s]*:["\s]*([0-9]+)',
}

MAX_RAW = 500


def _cargar_json(texto: str):
    """Intenta cargar texto como JSON; devuelve None si no es válido."""
    try:
        return json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return None


def _buscar_bloque_json(texto: str):
    """Localiza y parsea el primer bloque {...} con un identificador entre comillas.

    Se recorre el texto con indexación en lugar de usar una expresión regular
    ambigua, evitando backtracking polinómico sobre entradas largas.
    """
    inicio = texto.find('{')
    while inicio != -1:
        fin = texto.find('}', inicio + 1)
        if fin == -1:
            return None
        bloque = texto[inicio:fin + 1]
        if re.search(r'"[a-zA-Z_]+"', bloque):
            datos = _cargar_json(bloque)
            if datos is not None:
                return datos
        inicio = texto.find('{', fin + 1)
    return None


def _parsear_lineas_json(texto: str):
    """Reintenta el parseo usando solo las líneas con estructura de JSON."""
    lineas = [
        linea for linea in texto.split('\n')
        if '{' in linea or '}' in linea or '"' in linea or ':' in linea
    ]
    if not lineas:
        return None
    return _cargar_json('\n'.join(lineas))


def _buscar_json_rodeado(texto: str):
    """Busca un objeto JSON delimitado por llaves en el texto."""
    inicio = texto.find('{')
    if inicio == -1:
        return None
    fin = texto.rfind('}')
    if fin < inicio:
        return None
    return _cargar_json(texto[inicio:fin + 1])


def limpiar_respuesta_json(contenido: str) -> dict:
    """Limpia la respuesta del modelo y la parsea a JSON.

    Mejorado para manejar modelos que devuelven código extra.
    """
    # 1. Limpiar markers de código
    limpio = contenido.replace("```json", "").replace("```", "").strip()

    # 2. Intentar parsear directo
    directo = _cargar_json(limpio)
    if directo is not None:
        return directo

    # 3. Buscar JSON dentro del texto
    bloque = _buscar_bloque_json(limpio)
    if bloque is not None:
        return bloque

    # 4. Buscar objeto JSON anidado
    anidado = _buscar_json_rodeado(limpio)
    if anidado is not None:
        return anidado

    # 5. Intentar limpiar y reintentar con las líneas útiles
    por_lineas = _parsear_lineas_json(limpio)
    if por_lineas is not None:
        return por_lineas

    # 6. Si no se puede parsear, devolver lo que tenemos
    return parsear_respuesta_fallback(limpio)


def _convertir_valor(valor: str):
    """Convierte un texto numérico a int/float; en otro caso lo deja igual."""
    if valor.isdigit():
        return float(valor) if '.' in valor else int(valor)
    return valor


def _parsear_pipes(texto: str) -> dict:
    """Parsea respuestas con formato 'campo: valor | campo2: valor2'."""
    resultado = {}
    for parte in texto.split('|'):
        if ':' not in parte:
            continue
        campo, valor = parte.split(':', 1)
        # Limpiar comillas y corchetes
        valor = valor.strip().strip("[]'\"").replace("'", "")
        resultado[campo.strip().lower()] = _convertir_valor(valor)
    return resultado


def _parsear_regex(texto: str) -> dict:
    """Extrae campos conocidos usando expresiones regulares."""
    return {
        campo: match.group(1)
        for campo, patron in CAMPOS_FALLBACK.items()
        if (match := re.search(patron, texto, re.IGNORECASE)) is not None
    }


def parsear_respuesta_fallback(texto: str) -> dict:
    """Intenta extraer campos conocidos del texto."""
    texto = texto.strip()

    # Si viene estilo "campo: valor | campo2: valor2"
    if '|' in texto:
        resultado = _parsear_pipes(texto)
        if resultado:
            return resultado

    resultado = _parsear_regex(texto)
    if resultado:
        return resultado

    return {"raw": texto[:MAX_RAW]}


def validar_texto(texto: str) -> bool:
    """Valida que el texto sea válido para análisis."""
    return bool(texto and texto.strip() and len(texto.strip()) > 3)


def formatear_resultado(resultado: dict) -> str:
    """Formatea un resultado como string legible."""
    return json.dumps(resultado, indent=2, ensure_ascii=False)