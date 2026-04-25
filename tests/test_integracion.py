"""Tests de integración para la app completa."""

from unittest.mock import patch


class TestIntegracionAnalisis:
    """Test de análisis completo."""
    
    def test_analisis_entrada_y_salida(self):
        """Test flujo completo entrada → análisis → resultado."""
        from src.analizador import analizar_texto
        
        resultado_mock = {
            "sentimiento": {"sentimiento": "neutral", "puntuacion": 0.5, "emociones": ["curiosidad"], "confianza": 0.8},
            "entidades": {"personas": [], "organizaciones": [], "lugares": [], "fechas": [], "cantidades": [], "otros": ["Python"]},
            "intencion": {"intencion_principal": "informacion", "subcategoria": "ayuda", "urgencia": "media", "accion_sugerida": "responder"},
            "clasificacion": {"tema": "tecnico", "tipo": "pregunta", "canal_adecuado": "chat", "prioridad": 3},
            "resumen": {"raw": "Solución..."}
        }
        
        with patch('src.niveles._analisis_individual', return_value=resultado_mock):
            resultado = analizar_texto("¿Cómo configuro timeout en Python?")
            
            assert "sentimiento" in resultado
            assert "entidades" in resultado
            assert "intencion" in resultado
            assert "clasificacion" in resultado
            assert "resumen" in resultado
    
    def test_resultado_tiene_campos_completos(self):
        """Verifica que todos los campos requeridos estén."""
        from src.analizador import analizar_texto
        
        resultado_mock = {
            "sentimiento": {"sentimiento": "neutral"},
            "entidades": {"otros": []},
            "intencion": {"intencion_principal": "informacion"},
            "clasificacion": {"tema": "tecnico"},
            "resumen": {"raw": "test"}
        }
        
        with patch('src.niveles._analisis_individual', return_value=resultado_mock):
            resultado = analizar_texto("test")
            
            assert resultado["sentimiento"]["sentimiento"] is not None
            assert "otros" in resultado["entidades"]
            assert isinstance(resultado["entidades"]["otros"], list)
            assert resultado["intencion"]["intencion_principal"] is not None
            assert resultado["clasificacion"]["tema"] is not None
            assert resultado["resumen"] is not None


class TestValidarTexto:
    """Test validación de texto."""
    
    def test_texto_valido(self):
        """Texto válido pasa."""
        from src.utils import validar_texto
        
        assert validar_texto("Python es un lenguaje de programación")
    
    def test_texto_vacio_falla(self):
        """Texto vacío falla."""
        from src.utils import validar_texto
        
        assert not validar_texto("")
    
    def test_texto_muy_corto_falla(self):
        """Texto muy corto falla."""
        from src.utils import validar_texto
        
        assert not validar_texto("abc")


class TestLimpiarRespuestaJSON:
    """Test limpiar respuestas del modelo."""
    
    def test_limpia_json_valido(self):
        """Limpia JSON válido."""
        from src.utils import limpiar_respuesta_json
        
        resultado = limpiar_respuesta_json('{"sentimiento": "positivo"}')
        
        assert resultado["sentimiento"] == "positivo"
    
    def test_limpia_con_markdown(self):
        """Limpia JSON con markdown."""
        from src.utils import limpiar_respuesta_json
        
        resultado = limpiar_respuesta_json('```json\n{"sentimiento": "positivo"}\n```')
        
        assert resultado["sentimiento"] == "positivo"
    
    def test_maneja_error(self):
        """Maneja respuesta inválida."""
        from src.utils import limpiar_respuesta_json
        
        resultado = limpiar_respuesta_json("no es json")
        
        assert "error" in resultado or "raw" in resultado


class TestFormatearResultado:
    """Test formatear resultados."""
    
    def test_formatear_json(self):
        """Formatea a JSON."""
        from src.utils import formatear_resultado
        
        data = {
            "sentimiento": {"sentimiento": "neutral"},
            "entidades": {"otros": ["Python"]}
        }
        
        resultado = formatear_resultado(data)
        
        assert isinstance(resultado, str)