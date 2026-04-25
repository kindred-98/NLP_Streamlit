"""Tests para src/utils.py - Utilidades de parsing y validación."""

from src.utils import (
    limpiar_respuesta_json, validar_texto, formatear_resultado,
    parsear_respuesta_fallback
)


class TestLimpiarRespuestaJson:
    """Tests para limpiar_respuesta_json()."""

    def test_json_valido_sin_marcas(self):
        """JSON válido sin marcas."""
        contenido = '{"sentimiento": "positivo", "puntuacion": 0.9}'
        resultado = limpiar_respuesta_json(contenido)
        assert resultado == {"sentimiento": "positivo", "puntuacion": 0.9}

    def test_json_con_markdown_json(self):
        """JSON con ```json."""
        contenido = '```json\n{"sentimiento": "positivo"}\n```'
        resultado = limpiar_respuesta_json(contenido)
        assert resultado == {"sentimiento": "positivo"}

    def test_json_con_marcas_multiples(self):
        """JSON con múltiples marcas."""
        contenido = '```json```{"error": "msg"}```'
        resultado = limpiar_respuesta_json(contenido)
        assert resultado == {"error": "msg"}

    def test_json_con_solo_backticks(self):
        """JSON con solo backticks."""
        contenido = '```\n{"clave": "valor"}\n```'
        resultado = limpiar_respuesta_json(contenido)
        assert resultado == {"clave": "valor"}

    def test_json_con_espacios_extra(self):
        """JSON con espacios extra."""
        contenido = '  \n  {"clave": "valor"}  \n  '
        resultado = limpiar_respuesta_json(contenido)
        assert resultado == {"clave": "valor"}

    def test_json_anidado_en_texto(self):
        """JSON anidado dentro de texto."""
        contenido = 'Aquí está el resultado: {"sentimiento": "neutral"} más texto'
        resultado = limpiar_respuesta_json(contenido)
        assert "sentimiento" in resultado or "raw" in resultado

    def test_json_invalido_devuelve_raw(self):
        """JSON inválido devuelve fallback."""
        contenido = 'no es json válido aquí'
        resultado = limpiar_respuesta_json(contenido)
        assert "raw" in resultado or "sentimiento" in resultado or "error" in contenido

    def test_json_invalido_totally(self):
        """JSON completamente inválido."""
        contenido = 'abcdefghij'
        resultado = limpiar_respuesta_json(contenido)
        assert isinstance(resultado, dict)

    def test_json_con_lineas_mixtas(self):
        """JSON con líneas mixtas (texto y JSON)."""
        contenido = 'texto plano\n{"clave": "valor"}\nmas texto'
        resultado = limpiar_respuesta_json(contenido)
        assert isinstance(resultado, dict)

    def test_json_con_json_invalido_primera_busqueda(self):
        """JSON inválido pero con patrón JSON parcial."""
        contenido = '{"clave": incomplete'
        resultado = limpiar_respuesta_json(contenido)
        assert isinstance(resultado, dict)


class TestParsearRespuestaFallback:
    """Tests para parsear_respuesta_fallback()."""

    def test_fallback_con_pipe(self):
        """Parsea respuesta con pipes."""
        texto = 'sentimiento: positivo | puntuacion: 0.8'
        resultado = parsear_respuesta_fallback(texto)
        assert "sentimiento" in resultado
        assert resultado.get("sentimiento") == "positivo"

    def test_fallback_con_espacios(self):
        """Fallback con espacios."""
        texto = '  sentimiento : positivo | puntuacion : 0.8  '
        resultado = parsear_respuesta_fallback(texto)
        assert "sentimiento" in resultado

    def test_fallback_con_numero_entero(self):
        """Fallback con número entero."""
        texto = 'prioridad: 5'
        resultado = parsear_respuesta_fallback(texto)
        assert "prioridad" in resultado

    def test_fallback_con_numero_float(self):
        """Fallback con número float string."""
        texto = 'puntuacion: 0.95'
        resultado = parsear_respuesta_fallback(texto)
        assert "puntuacion" in resultado

    def test_fallback_con_comillas(self):
        """Fallback con comillas."""
        texto = 'tema: "mi problema"'
        resultado = parsear_respuesta_fallback(texto)
        assert "tema" in resultado

    def test_fallback_con_corchetes(self):
        """Fallback con corchetes."""
        texto = 'emociones: [alegria, tristeza]'
        resultado = parsear_respuesta_fallback(texto)
        assert "emociones" in resultado

    def test_fallback_sin_datos_validos(self):
        """Fallback sin datos."""
        texto = 'texto sin estructura'
        resultado = parsear_respuesta_fallback(texto)
        assert "raw" in resultado

    def test_fallback_raw_limita_longitud(self):
        """Fallback raw limita a 500 chars."""
        texto = 'x' * 1000
        resultado = parsear_respuesta_fallback(texto)
        assert len(resultado.get("raw", "")) <= 500

    def test_fallback_regex_sentimiento(self):
        """Fallback con regex para sentimiento."""
        texto = 'sentimiento: positivo'
        resultado = parsear_respuesta_fallback(texto)
        assert "sentimiento" in resultado

    def test_fallback_regex_personas(self):
        """Fallback con regex para personas."""
        texto = 'Personas: [Juan, Maria]'
        resultado = parsear_respuesta_fallback(texto)
        assert "personas" in resultado

    def test_fallback_regex_lugares(self):
        """Fallback con regex para lugares."""
        texto = 'Lugares: [Madrid, Barcelona]'
        resultado = parsear_respuesta_fallback(texto)
        assert "lugares" in resultado

    def test_fallback_numero_sin_decimal(self):
        """Fallback número sin decimal."""
        texto = 'prioridad: 5'
        resultado = parsear_respuesta_fallback(texto)
        assert resultado.get("prioridad") == "5"
        assert isinstance(resultado.get("prioridad"), str)

    def test_fallback_numero_con_decimal(self):
        """Fallback número con decimal."""
        texto = 'puntuacion: 0.95'
        resultado = parsear_respuesta_fallback(texto)
        assert resultado.get("puntuacion") == "0.95"
        assert isinstance(resultado.get("puntuacion"), str)

    def test_fallback_subcategoria(self):
        """Fallback subcategoria."""
        texto = 'subcategoria: ayuda técnica'
        resultado = parsear_respuesta_fallback(texto)
        assert "subcategoria" in resultado

    def test_fallback_urgencia(self):
        """Fallback urgencia."""
        texto = 'urgencia: alta'
        resultado = parsear_respuesta_fallback(texto)
        assert "urgencia" in resultado

    def test_fallback_tema(self):
        """Fallback tema."""
        texto = 'tema: técnicos'
        resultado = parsear_respuesta_fallback(texto)
        assert "tema" in resultado

    def test_fallback_tipo(self):
        """Fallback tipo."""
        texto = 'tipo: pregunta'
        resultado = parsear_respuesta_fallback(texto)
        assert "tipo" in resultado

    def test_fallback_canal_adecuado(self):
        """Fallback canal_adecuado."""
        texto = 'canal_adecuado: chat'
        resultado = parsear_respuesta_fallback(texto)
        assert "canal_adecuado" in resultado


class TestValidarTexto:
    """Tests para validar_texto()."""

    def test_texto_valido(self):
        """Texto válido."""
        assert validar_texto("Texto de prueba válido")

    def test_texto_vacio(self):
        """Texto vacío."""
        assert not validar_texto("")

    def test_texto_solo_espacios(self):
        """Solo espacios."""
        assert not validar_texto("   ")

    def test_texto_solo_tabs(self):
        """Solo tabs."""
        assert not validar_texto("\t\t")

    def test_texto_muy_corto(self):
        """Texto muy corto."""
        assert not validar_texto("ab")

    def test_texto_3_caracteres(self):
        """Texto con 3 caracteres (mínimo es 4)."""
        assert not validar_texto("abc")

    def test_texto_4_caracteres(self):
        """Texto con 4 caracteres (borde)."""
        assert validar_texto("abcd")

    def test_texto_5_caracteres(self):
        """Texto con 5 caracteres."""
        assert validar_texto("abcde")

    def test_texto_none(self):
        """Texto None."""
        assert not validar_texto(None)

    def test_texto_newlines(self):
        """Texto con newlines."""
        assert validar_texto("a\nb\nc\nd")


class TestFormatearResultado:
    """Tests para formatear_resultado()."""

    def test_formatear_dict_simple(self):
        """Formatea dict simple."""
        data = {"sentimiento": "positivo", "puntuacion": 0.9}
        resultado = formatear_resultado(data)
        assert isinstance(resultado, str)
        assert "sentimiento" in resultado

    def test_formatear_dict_vacio(self):
        """Formatea dict vacío."""
        assert formatear_resultado({}) == "{}"

    def test_formatear_dict_nested(self):
        """Formatea dict anidado."""
        data = {"nivel1": {"nivel2": "valor"}}
        resultado = formatear_resultado(data)
        assert "nivel1" in resultado

    def test_formatear_dict_con_unicode(self):
        """Formatea dict con unicode."""
        data = {"texto": "ñ á é í ó ú 中文"}
        resultado = formatear_resultado(data)
        assert isinstance(resultado, str)

    def test_formatear_lista_retorna_json(self):
        """Formatea lista (se convierte a JSON string)."""
        data = [1, 2, 3]
        resultado = formatear_resultado(data)
        assert isinstance(resultado, str)