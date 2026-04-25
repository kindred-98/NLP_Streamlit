"""Tests para almacenamiento/guardar.py - Guardado de archivos."""

import pytest
from unittest.mock import patch, MagicMock
from almacenamiento.guardar import (
    _crear_carpetas, _formatear_txt, guardar_resultado,
    guardar_txt, guardar_json
)


class TestCrearCarpetas:
    """Tests para _crear_carpetas()."""

    def test_crear_carpetas(self):
        """Crea carpetas correctamente."""
        with patch('almacenamiento.guardar.CARPETA_TXT') as mock_txt:
            with patch('almacenamiento.guardar.CARPETA_JSON') as mock_json:
                mock_txt.mkdir = MagicMock()
                mock_json.mkdir = MagicMock()
                _crear_carpetas()
                mock_txt.mkdir.assert_called_once_with(parents=True, exist_ok=True)
                mock_json.mkdir.assert_called_once_with(parents=True, exist_ok=True)


class TestFormatearTxt:
    """Tests para _formatear_txt()."""

    def test_formatear_txt_completo(self):
        """Formatea TXT con todos los campos."""
        texto = "Texto de prueba"
        resultados = {
            "sentimiento": {"sentimiento": "positivo"},
            "entidades": {"personas": ["Juan"]},
            "intencion": {"intencion_principal": "soporte"},
            "resumen": {"resumen": "texto resumido"},
            "clasificacion": {"tema": "tecnico"}
        }
        timestamp = "20240101_123456"

        resultado = _formatear_txt(texto, resultados, timestamp)

        assert "ANALISIS NLP" in resultado
        assert "20240101_123456" in resultado
        assert texto in resultado
        assert "positivo" in resultado
        assert "Juan" in resultado

    def test_formatear_txt_vacio(self):
        """Formatea TXT con resultados vacíos."""
        resultado = _formatear_txt("texto", {}, "20240101")
        assert "ANALISIS NLP" in resultado

    def test_formatear_txt_sin_algun_campo(self):
        """Formatea TXT faltando campos."""
        resultados = {"sentimiento": {"sentimiento": "positivo"}}
        resultado = _formatear_txt("texto", resultados, "20240101")
        assert "ANALISIS NLP" in resultado


class TestGuardarResultado:
    """Tests para guardar_resultado()."""

    def test_guardar_resultado_texto_vacio(self):
        """Texto vacío lanza ValueError."""
        with pytest.raises(ValueError, match="no puede estar vacio"):
            guardar_resultado("", {})

    def test_guardar_resultado_solo_espacios(self):
        """Texto solo espacios lanza ValueError."""
        with pytest.raises(ValueError, match="no puede estar vacio"):
            guardar_resultado("   ", {})

    def test_guardar_resultado_crea_archivos(self):
        """Crea archivos TXT y JSON."""
        with patch('almacenamiento.guardar._crear_carpetas'):
            with patch('almacenamiento.guardar.datetime') as mock_dt:
                mock_dt.now.return_value.strftime.return_value = "20240101_123456_789012"

                with patch('builtins.open', MagicMock()):
                    with patch('json.dump'):
                        resultado = guardar_resultado("texto", {"sentimiento": {}})

                        assert "txt" in resultado
                        assert "json" in resultado
                        assert "20240101_123456_789012" in resultado["txt"]
                        assert "20240101_123456_789012" in resultado["json"]

    def test_guardar_resultado_guarda_json(self):
        """Guarda JSON con estructura correcta."""
        with patch('almacenamiento.guardar._crear_carpetas'):
            with patch('almacenamiento.guardar.datetime') as mock_dt:
                mock_dt.now.return_value.strftime.return_value = "20240101_123456"

                with patch('builtins.open', MagicMock()):
                    with patch('json.dump') as mock_json_dump:
                        guardar_resultado("texto", {"sentimiento": {}})
                        mock_json_dump.assert_called_once()
                        args = mock_json_dump.call_args[0][0]
                        assert "timestamp" in args
                        assert "texto" in args
                        assert "resultados" in args


class TestGuardarTxt:
    """Tests para guardar_txt()."""

    def test_guardar_txt_crea_archivo(self):
        """Crea archivo TXT."""
        with patch('almacenamiento.guardar._crear_carpetas'):
            with patch('almacenamiento.guardar.datetime') as mock_dt:
                mock_dt.now.return_value.strftime.return_value = "20240101_123456"

                with patch('builtins.open', MagicMock()):
                    ruta = guardar_txt("contenido")
                    assert ruta.endswith(".txt")
                    assert "20240101_123456" in ruta

    def test_guardar_txt_con_nombre(self):
        """Crea archivo con nombre específico."""
        with patch('almacenamiento.guardar._crear_carpetas'):
            with patch('builtins.open', MagicMock()):
                ruta = guardar_txt("contenido", nombre="mi_archivo")
                assert "mi_archivo" in ruta


class TestGuardarJson:
    """Tests para guardar_json()."""

    def test_guardar_json_crea_archivo(self):
        """Crea archivo JSON."""
        with patch('almacenamiento.guardar._crear_carpetas'):
            with patch('almacenamiento.guardar.datetime') as mock_dt:
                mock_dt.now.return_value.strftime.return_value = "20240101_123456"

                with patch('builtins.open', MagicMock()):
                    with patch('json.dump'):
                        ruta = guardar_json({"clave": "valor"})
                        assert ruta.endswith(".json")
                        assert "20240101_123456" in ruta

    def test_guardar_json_con_nombre(self):
        """Crea JSON con nombre específico."""
        with patch('almacenamiento.guardar._crear_carpetas'):
            with patch('builtins.open', MagicMock()):
                with patch('json.dump'):
                    ruta = guardar_json({"clave": "valor"}, nombre="datos")
                    assert "datos" in ruta

    def test_guardar_json_usa_json_dump(self):
        """Llama a json.dump."""
        with patch('almacenamiento.guardar._crear_carpetas'):
            with patch('builtins.open', MagicMock()):
                with patch('json.dump') as mock_dump:
                    guardar_json({"test": 123})
                    mock_dump.assert_called_once()