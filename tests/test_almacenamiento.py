import os
import json
from unittest.mock import patch


class TestAlmacenamiento:
    """Tests para almacenamiento/guardar.py"""

    def test_guardar_resultado_crea_txt(self, tmp_path):
        """Caso feliz: crea archivo TXT"""
        from almacenamiento.guardar import guardar_resultado
        
        carpeta = tmp_path / "resultados"
        txt_dir = carpeta / "txt"
        
        with patch("almacenamiento.guardar.CARPETA_TXT", txt_dir):
            with patch("almacenamiento.guardar.CARPETA_JSON", carpeta / "json"):
                texto = "Prueba de texto"
                resultado = {"sentimiento": "positivo"}
                
                rutas = guardar_resultado(texto, resultado)
                
                assert os.path.exists(rutas["txt"])

    def test_guardar_resultado_crea_json(self, tmp_path):
        """Caso feliz: crea archivo JSON"""
        from almacenamiento.guardar import guardar_resultado
        
        carpeta = tmp_path / "resultados"
        json_dir = carpeta / "json"
        
        with patch("almacenamiento.guardar.CARPETA_TXT", carpeta / "txt"):
            with patch("almacenamiento.guardar.CARPETA_JSON", json_dir):
                texto = "Prueba de texto"
                resultado = {"sentimiento": "positivo"}
                
                rutas = guardar_resultado(texto, resultado)
                
                assert os.path.exists(rutas["json"])

    def test_guardar_json_contiene_datos(self, tmp_path):
        """Validar contenido del JSON guardado"""
        from almacenamiento.guardar import guardar_resultado
        
        carpeta = tmp_path / "resultados"
        
        with patch("almacenamiento.guardar.CARPETA_TXT", carpeta / "txt"):
            with patch("almacenamiento.guardar.CARPETA_JSON", carpeta / "json"):
                texto = "Prueba de texto"
                resultado = {"sentimiento": "positivo", "puntuacion": 0.9}
                
                rutas = guardar_resultado(texto, resultado)
                
                with open(rutas["json"], "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                assert "texto" in data
                assert "resultados" in data
                assert "timestamp" in data
                assert data["texto"] == texto

    def test_guardar_txt_contiene_texto(self, tmp_path):
        """Validar contenido del TXT guardado"""
        from almacenamiento.guardar import guardar_resultado
        
        carpeta = tmp_path / "resultados"
        
        with patch("almacenamiento.guardar.CARPETA_TXT", carpeta / "txt"):
            with patch("almacenamiento.guardar.CARPETA_JSON", carpeta / "json"):
                texto = "Mi texto de prueba"
                resultado = {"sentimiento": "negativo"}
                
                rutas = guardar_resultado(texto, resultado)
                
                contenido = open(rutas["txt"], "r", encoding="utf-8").read()
                
                assert texto in contenido

    def test_guardar_txt_independiente(self, tmp_path):
        """Caso borde: guardar solo TXT"""
        from almacenamiento.guardar import guardar_txt
        
        carpeta = tmp_path / "txt"
        
        with patch("almacenamiento.guardar.CARPETA_TXT", carpeta):
            ruta = guardar_txt("Contenido prueba", "test")
            
            assert os.path.exists(ruta)

    def test_guardar_json_independiente(self, tmp_path):
        """Caso borde: guardar solo JSON"""
        from almacenamiento.guardar import guardar_json
        
        carpeta = tmp_path / "json"
        
        with patch("almacenamiento.guardar.CARPETA_JSON", carpeta):
            datos = {"key": "value"}
            ruta = guardar_json(datos, "test")
            
            assert os.path.exists(ruta)
            
            with open(ruta, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            
            assert loaded == datos

    def test_crear_carpetas_sino_existen(self, tmp_path):
        """Caso borde: crea carpetas automáticamente"""
        from almacenamiento.guardar import _crear_carpetas
        
        carpeta = tmp_path / "nueva"
        
        with patch("almacenamiento.guardar.CARPETA_TXT", carpeta / "txt"):
            with patch("almacenamiento.guardar.CARPETA_JSON", carpeta / "json"):
                _crear_carpetas()
                
                assert (carpeta / "txt").exists()
                assert (carpeta / "json").exists()