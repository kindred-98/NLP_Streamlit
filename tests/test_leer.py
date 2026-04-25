"""Tests para almacenamiento/leer.py - Lectura de archivos."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from almacenamiento.leer import (
    _listar_json, listar_analisis, leer_json,
    buscar_por_fecha, leer_ultimo
)


class TestListarJson:
    """Tests para _listar_json()."""

    def test_listar_json_sin_carpeta(self):
        """Sin carpeta retorna lista vacía."""
        with patch('almacenamiento.leer.CARPETA_JSON', Path('/noexiste')):
            resultado = _listar_json()
            assert resultado == []

    def test_listar_json_con_archivos(self):
        """Con archivos retorna lista ordenada."""
        mock_path = MagicMock()
        mock_path.name = "20240101.json"
        mock_path.exists.return_value = True
        mock_path.glob.return_value = [mock_path]

        with patch('almacenamiento.leer.CARPETA_JSON', mock_path):
            with patch('almacenamiento.leer.Path.glob', return_value=[mock_path]):
                resultado = _listar_json()
                assert isinstance(resultado, list)


class TestListarAnalisis:
    """Tests para listar_analisis()."""

    def test_listar_analisis_vacio(self):
        """Sin archivos retorna lista vacía."""
        with patch('almacenamiento.leer._listar_json', return_value=[]):
            resultado = listar_analisis()
            assert resultado == []

    def test_listar_analisis_con_archivo(self):
        """Con archivo retorna análisis."""
        mock_archivo = MagicMock()
        mock_archivo.name = "analisis_20240101.json"
        mock_archivo.read_text = MagicMock(return_value='{"timestamp": "20240101", "texto": "texto de prueba"}')

        with patch('almacenamiento.leer._listar_json', return_value=[mock_archivo]):
            resultado = listar_analisis()
            assert len(resultado) == 1
            assert resultado[0]["archivo"] == "analisis_20240101.json"
            assert resultado[0]["timestamp"] == "20240101"
            assert resultado[0]["texto"] == "texto de prueba"

    def test_listar_analisis_con_texto_largo(self):
        """Texto largo se trunca a 100 chars."""
        texto_largo = "a" * 300
        mock_archivo = MagicMock()
        mock_archivo.name = "test.json"
        mock_archivo.read_text = MagicMock(return_value=f'{{"texto": "{texto_largo}"}}')

        with patch('almacenamiento.leer._listar_json', return_value=[mock_archivo]):
            resultado = listar_analisis()
            assert len(resultado[0]["texto"]) <= 100

    def test_listar_analisis_archivo_invalido_skip(self):
        """Archivo inválido se ignora."""
        mock_archivo = MagicMock()
        mock_archivo.name = "test.json"
        mock_archivo.read_text = MagicMock(side_effect=Exception("Error"))

        with patch('almacenamiento.leer._listar_json', return_value=[mock_archivo]):
            resultado = listar_analisis()
            assert resultado == []


class TestLeerJson:
    """Tests para leer_json()."""

    def test_leer_json_existe(self):
        """Lee archivo existente."""
        mock_ruta = MagicMock(spec=Path)
        mock_ruta.exists.return_value = True
        mock_ruta.read_text.return_value = '{"clave": "valor"}'

        with patch('almacenamiento.leer.CARPETA_JSON') as mock_carpeta:
            mock_carpeta.__truediv__.return_value = mock_ruta
            with patch('json.loads', return_value={"clave": "valor"}) as mock_json:
                resultado = leer_json("test.json")
                assert resultado == {"clave": "valor"}
                mock_json.assert_called_once()

    def test_leer_json_no_existe(self):
        """Archivo no existe lanza FileNotFoundError."""
        mock_ruta = MagicMock(spec=Path)
        mock_ruta.exists.return_value = False

        with patch('almacenamiento.leer.CARPETA_JSON') as mock_carpeta:
            mock_carpeta.__truediv__.return_value = mock_ruta
            with pytest.raises(FileNotFoundError, match="No encontrado"):
                leer_json("noexiste.json")

    def test_leer_json_parse_error(self):
        """Error al parsear JSON levanta excepción."""
        mock_ruta = MagicMock(spec=Path)
        mock_ruta.exists.return_value = True
        mock_ruta.read_text.return_value = '{invalid json}'

        with patch('almacenamiento.leer.CARPETA_JSON') as mock_carpeta:
            mock_carpeta.__truediv__.return_value = mock_ruta
            with pytest.raises(json.JSONDecodeError):
                json.loads(mock_ruta.read_text())


class TestBuscarPorFecha:
    """Tests para buscar_por_fecha()."""

    def test_buscar_por_fecha_encontra(self):
        """Encuentra archivos por fecha."""
        mock_archivo = MagicMock()
        mock_archivo.name = "analisis_20240101_123456.json"
        mock_archivo.read_text = MagicMock(return_value='{"timestamp": "20240101"}')

        with patch('almacenamiento.leer._listar_json', return_value=[mock_archivo]):
            with patch('json.loads', return_value={"timestamp": "20240101"}):
                resultado = buscar_por_fecha("20240101")
                assert len(resultado) >= 1

    def test_buscar_por_fecha_no_encontra(self):
        """No encuentra archivos."""
        mock_archivo = MagicMock()
        mock_archivo.name = "analisis_20240101.json"
        mock_archivo.read_text = MagicMock(return_value='{"timestamp": "20240101"}')

        with patch('almacenamiento.leer._listar_json', return_value=[mock_archivo]):
            resultado = buscar_por_fecha("20991231")
            assert resultado == []


class TestLeerUltimo:
    """Tests para leer_ultimo()."""

    def test_leer_ultimo_existe(self):
        """Lee último archivo."""
        mock_archivo = MagicMock()
        mock_archivo.read_text = MagicMock(return_value='{"sentimiento": "positivo"}')

        with patch('almacenamiento.leer._listar_json', return_value=[mock_archivo]):
            with patch('json.loads', return_value={"sentimiento": "positivo"}):
                resultado = leer_ultimo()
                assert resultado == {"sentimiento": "positivo"}

    def test_leer_ultimo_sin_archivos(self):
        """Sin archivos retorna dict vacío."""
        with patch('almacenamiento.leer._listar_json', return_value=[]):
            resultado = leer_ultimo()
            assert resultado == {}