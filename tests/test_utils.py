import pytest
import json
from src.utils import limpiar_respuesta_json, validar_texto, formatear_resultado


class TestUtils:
    """Tests para src/utils.py"""

    def test_limpiar_json_valido(self):
        """Caso feliz: JSON válidosin etiquetas"""
        contenido = '{"sentimiento": "positivo", "puntuacion": 0.9}'
        resultado = limpiar_respuesta_json(contenido)
        
        assert resultado == {"sentimiento": "positivo", "puntuacion": 0.9}

    def test_limpiar_json_con_markdown(self):
        """Caso feliz: limpiartags markdown"""
        contenido = '```json\n{"sentimiento": "positivo"}\n```'
        resultado = limpiar_respuesta_json(contenido)
        
        assert resultado == {"sentimiento": "positivo"}

    def test_limpiar_json_con_marcas(self):
        """Caso feliz:清理múltiples marcas"""
        contenido = '```json```{"error": "msg"}```'
        resultado = limpiar_respuesta_json(contenido)
        
        assert resultado == {"error": "msg"}

    def test_limpiar_json_invalido_retorna_error(self):
        """Error: JSONinválido retorna dict con error"""
        contenido = 'no es json válido'
        resultado = limpiar_respuesta_json(contenido)
        
        assert "error" in resultado
        assert "raw" in resultado

    def test_validar_texto_valido(self):
        """Caso feliz: texto válido"""
        assert validar_texto("Texto de prueba válido") == True

    def test_validar_texto_vacio(self):
        """Error: texto vacío"""
        assert validar_texto("") == False

    def test_validar_texto_solo_espacios(self):
        """Error: solo espacios"""
        assert validar_texto("   ") == False

    def test_validar_texto_muy_corto(self):
        """Error: texto muy corto (< 4 chars)"""
        assert validar_texto("ab") == False

    def test_validar_texto_exacto_minimo(self):
        """Caso borde: texto con 4 caracteres"""
        assert validar_texto("abcd") == True

    def test_formatear_resultado(self):
        """Caso feliz: formatear dict"""
        data = {"sentimiento": "positivo", "puntuacion": 0.9}
        resultado = formatear_resultado(data)
        
        assert isinstance(resultado, str)
        assert "sentimiento" in resultado

    def test_formatear_resultado_vacio(self):
        """Caso borde: dict vacío"""
        data = {}
        resultado = formatear_resultado(data)
        
        assert resultado == "{}"