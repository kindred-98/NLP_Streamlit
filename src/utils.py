import json
import re


def limpiar_respuesta_json(contenido: str) -> dict:
    """Limpia la respuesta del modelo y la parsea a JSON.
    
    Mejorado para manejar modelos que devuelven código extra.
    """
    # 1. Limpiar markers de código
    limpio = contenido.replace("```json", "").replace("```", "").strip()
    
    # 2. Intentar parsear directo
    try:
        return json.loads(limpio)
    except json.JSONDecodeError:
        pass
    
    # 3. Buscar JSON dentro del texto
    json_match = re.search(r'\{[^{}]*"[a-zA-Z_]+"[^{}]*\}', limpio, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # 4. Buscar objeto JSON anidado
    json_match = re.search(r'\{.*\}', limpio, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # 5. Intentar limpiar y reintentar
    # Buscar solo las partes válidas del JSON
    try:
        # Extraer solo lo que parece JSON válido
        lines = limpio.split('\n')
        json_lines = []
        for line in lines:
            if '{' in line or '}' in line or '"' in line or ':' in line:
                json_lines.append(line)
        
        if json_lines:
            texto_json = '\n'.join(json_lines)
            return json.loads(texto_json)
    except json.JSONDecodeError:
        pass
    
    # 6. Si no se puede parsear, devolver lo queTenemos
    return parsear_respuesta_fallback(limpio)


def parsear_respuesta_fallback(texto: str) -> dict:
    """Intenta extraer campos conocidos del texto."""
    resultado = {}
    texto = texto.strip()
    
    # Si viene estilo "campo: valor | campo2: valor2"
    if '|' in texto:
        for parte in texto.split('|'):
            parte = parte.strip()
            if ':' in parte:
                campo, valor = parte.split(':', 1)
                campo = campo.strip().lower()
                valor = valor.strip()
                # Limpiar comillas y corchetes
                valor = valor.strip("[]'\"").replace("'", "")
                if valor.isdigit():
                    valor = float(valor) if '.' in valor else int(valor)
                resultado[campo] = valor
    
    if resultado:
        return resultado
    
    # Mapeo de campos comunes - regex
    campos = {
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
    
    for campo, patron in campos.items():
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            resultado[campo] = match.group(1)
    
    if resultado:
        return resultado
    
    return {"raw": texto[:500]}


def validar_texto(texto: str) -> bool:
    """Valida que el texto sea válido para análisis."""
    return bool(texto and texto.strip() and len(texto.strip()) > 3)


def formatear_resultado(resultado: dict) -> str:
    """Formatea un resultado como string legible."""
    return json.dumps(resultado, indent=2, ensure_ascii=False)