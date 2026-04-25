import pytest
from unittest.mock import patch, MagicMock


class TestAnalizador:
    """Tests para src/analizador.py"""

    @patch("src.niveles.get_client")
    @patch("src.niveles.get_modelo")
    def test_analizar_texto_devuelve_dict(self, mock_modelo, mock_client):
        """Caso feliz: verificar estructura de retorno"""
        mock_modelo.return_value = "qwen2.5:0.5b"
        mock_client.return_value = MagicMock()

        with patch("src.niveles._llamar_modelo") as mock_llamar:
            mock_llamar.return_value = {"sentimiento": "positivo"}
            
            from src.analizador import analizar_texto
            resultado = analizar_texto("Me gusta este producto")

            assert isinstance(resultado, dict)
            assert "sentimiento" in resultado
            assert "entidades" in resultado
            assert "intencion" in resultado
            assert "resumen" in resultado
            assert "clasificacion" in resultado

    def test_texto_vacio_lanza_error(self):
        """Error: texto vacío debe lanzar ValueError"""
        from src.analizador import analizar_texto
        
        with pytest.raises(ValueError):
            analizar_texto("")

    def test_texto_vacio_solo_espacios(self):
        """Error: solo espacios debe lanzar ValueError"""
        from src.analizador import analizar_texto
        
        with pytest.raises(ValueError):
            analizar_texto("   ")

    @patch("src.niveles.get_client")
    @patch("src.niveles.get_modelo")
    def test_texto_largo_no_falla(self, mock_modelo, mock_client):
        """Caso borde: texto largo no debe fallar"""
        mock_modelo.return_value = "qwen2.5:0.5b"
        
        with patch("src.niveles._llamar_modelo") as mock_llamar:
            mock_llamar.return_value = {"resultado": "ok"}
            
            from src.analizador import analizar_texto
            texto = "hola " * 1000
            resultado = analizar_texto(texto)

            assert isinstance(resultado, dict)

    @patch("src.niveles.get_client")
    @patch("src.niveles.get_modelo")
    def test_estructura_sentimiento(self, mock_modelo, mock_client):
        """Validar estructura interna de sentimiento"""
        mock_modelo.return_value = "qwen2.5:0.5b"
        
        with patch("src.niveles._llamar_modelo") as mock_llamar:
            mock_llamar.return_value = {"sentimiento": "positivo", "puntuacion": 0.8}
            
            from src.analizador import analizar_texto
            resultado = analizar_texto("Texto de prueba")

            assert isinstance(resultado["sentimiento"], dict)

    @patch("src.niveles.get_client")
    @patch("src.niveles.get_modelo")
    def test_todas_claves_presentes(self, mock_modelo, mock_client):
        """Verificar todas las claves del resultado"""
        mock_modelo.return_value = "qwen2.5:0.5b"
        
        with patch("src.niveles._llamar_modelo") as mock_llamar:
            mock_llamar.return_value = {"ok": True}
            
            from src.analizador import analizar_texto
            resultado = analizar_texto("Prueba")

            expected_keys = {"sentimiento", "entidades", "intencion", "clasificacion", "resumen"}
            assert expected_keys == set(resultado.keys())