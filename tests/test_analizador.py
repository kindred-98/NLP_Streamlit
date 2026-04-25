"""Tests para src/analizador.py - Punto de entrada principal."""

import pytest
from unittest.mock import patch
from src.analizador import analizar_texto


class TestAnalizarTexto:
    """Tests para analizar_texto()."""

    def test_texto_valido(self):
        """Analiza texto válido."""
        with patch('src.analizador.analisis_unificado', return_value={
            "sentimiento": {"sentimiento": "positivo"}
        }) as mock:
            resultado = analizar_texto("Gracias por tu ayuda")
            assert "sentimiento" in resultado
            mock.assert_called_once()

    def test_texto_vacio_lanza_error(self):
        """Texto vacío lanza ValueError."""
        with pytest.raises(ValueError, match="no puede estar vacio"):
            analizar_texto("")

    def test_texto_solo_espacios_lanza_error(self):
        """Texto solo espacios lanza ValueError."""
        with pytest.raises(ValueError, match="no puede estar vacio"):
            analizar_texto("   ")

    def test_texto_none_lanza_error(self):
        """Texto None lanza ValueError."""
        with pytest.raises(ValueError):
            analizar_texto(None)

    def test_error_en_analisis_retorna_error_dict(self):
        """Error retorna dict con error y estructura."""
        with patch('src.analizador.analisis_unificado', side_effect=Exception("Error")):
            resultado = analizar_texto("texto válido")
            assert "error" in resultado
            assert "sentimiento" in resultado
            assert "entidades" in resultado
            assert "intencion" in resultado
            assert "clasificacion" in resultado
            assert "resumen" in resultado

    def test_pasa_modelo(self):
        """Pasa modelo a analisis_unificado."""
        with patch('src.analizador.analisis_unificado', return_value={}) as mock:
            analizar_texto("texto", modelo="qwen2.5:3b")
            mock.assert_called_once_with("texto", modelo="qwen2.5:3b")