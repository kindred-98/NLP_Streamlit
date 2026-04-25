"""Tests para src/niveles.py - Prompts y funciones de análisis."""

from unittest.mock import patch, MagicMock
from src.niveles import (
    PROMPT_SENTIMIENTO, PROMPT_ENTIDADES, PROMPT_INTENCION,
    PROMPT_CLASIFICACION, PROMPT_RESUMEN_CORTO, PROMPT_RESUMEN_MEDIO,
    PROMPT_RESUMEN_DETALLADO, _llamar_modelo, _call_huggingface,
    analizar_sentimiento, extraer_entidades, detectar_intencion,
    clasificar_texto, resumir_texto, analisis_unificado, _analisis_individual
)


class TestPromptsDefined:
    """Verifica que los prompts están definidos."""

    def test_prompt_sentimiento_exists(self):
        """PROMPT_SENTIMIENTO definido."""
        assert len(PROMPT_SENTIMIENTO) > 0
        assert "sentimiento" in PROMPT_SENTIMIENTO.lower()

    def test_prompt_entidades_exists(self):
        """PROMPT_ENTIDADES definido."""
        assert len(PROMPT_ENTIDADES) > 0
        assert "tecnicos" in PROMPT_ENTIDADES.lower() or "tecnologias" in PROMPT_ENTIDADES.lower()

    def test_prompt_intencion_exists(self):
        """PROMPT_INTENCION definido."""
        assert len(PROMPT_INTENCION) > 0
        assert "intencion" in PROMPT_INTENCION.lower()

    def test_prompt_clasificacion_exists(self):
        """PROMPT_CLASIFICACION definido."""
        assert len(PROMPT_CLASIFICACION) > 0
        assert "tema" in PROMPT_CLASIFICACION.lower()

    def test_prompt_resumen_corto_exists(self):
        """PROMPT_RESUMEN_CORTO definido."""
        assert len(PROMPT_RESUMEN_CORTO) > 0

    def test_prompt_resumen_medio_exists(self):
        """PROMPT_RESUMEN_MEDIO definido."""
        assert len(PROMPT_RESUMEN_MEDIO) > 0

    def test_prompt_resumen_detallado_exists(self):
        """PROMPT_RESUMEN_DETALLADO definido."""
        assert len(PROMPT_RESUMEN_DETALLADO) > 0


class TestLlamarModelo:
    """Tests para _llamar_modelo()."""

    def test_llamar_modelo_ollama(self):
        """Llama modelo Ollama correctamente."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"sentimiento": "positivo"}'
        mock_client.chat.completions.create = MagicMock(return_value=mock_response)

        with patch('src.niveles.get_provider_name', return_value='ollama'):
            with patch('src.niveles.get_client', return_value=mock_client):
                with patch('src.niveles.get_modelo', return_value='llama3.2'):
                    resultado = _llamar_modelo("prompt", "texto")
                    assert resultado == {"sentimiento": "positivo"}

    def test_llamar_modelo_huggingface(self):
        """Llama modelo HuggingFace."""
        mock_client = MagicMock()
        with patch('src.niveles.get_provider_name', return_value='huggingface'):
            with patch('src.niveles.get_client', return_value=mock_client):
                with patch('src.niveles._call_huggingface', return_value={"ok": True}) as mock_hf:
                    _llamar_modelo("prompt", "texto")
                    mock_hf.assert_called_once()

    def test_llamar_modelo_con_error(self):
        """Maneja errores correctamente."""
        with patch('src.niveles.get_provider_name', return_value='ollama'):
            with patch('src.niveles.get_client', side_effect=Exception("Error")):
                resultado = _llamar_modelo("prompt", "texto")
                assert "error" in resultado

    def test_llamar_modelo_custom_model(self):
        """Usa modelo custom."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"ok": true}'
        mock_client.chat.completions.create = MagicMock(return_value=mock_response)

        with patch('src.niveles.get_provider_name', return_value='ollama'):
            with patch('src.niveles.get_client', return_value=mock_client):
                _llamar_modelo("prompt", "texto", modelo="custom-model")
                mock_client.chat.completions.create.assert_called_once()
                call_kwargs = mock_client.chat.completions.create.call_args
                assert call_kwargs.kwargs.get('model') == "custom-model"


class TestCallHuggingFace:
    """Tests para _call_huggingface()."""

    def test_call_huggingface_success(self):
        """HuggingFace exitoso."""
        mock_client = MagicMock()
        mock_client.text_generation = MagicMock(return_value='{"result": "ok"}')

        with patch('src.niveles.get_modelo', return_value='meta-llama'):
            resultado = _call_huggingface(mock_client, "system", "user")
            assert "result" in resultado or "error" not in resultado

    def test_call_huggingface_error(self):
        """HuggingFace con error."""
        mock_client = MagicMock()
        mock_client.text_generation = MagicMock(side_effect=Exception("HF Error"))

        resultado = _call_huggingface(mock_client, "system", "user")
        assert "error" in resultado


class TestAnalizarSentimiento:
    """Tests para analizar_sentimiento()."""

    def test_analizar_sentimiento_texto(self):
        """Analiza sentimiento de texto."""
        with patch('src.niveles._llamar_modelo', return_value={"sentimiento": "positivo"}) as mock:
            resultado = analizar_sentimiento("Gracias por la ayuda")
            assert resultado == {"sentimiento": "positivo"}
            mock.assert_called_once()

    def test_analizar_sentimiento_con_modelo(self):
        """Analiza con modelo específico."""
        with patch('src.niveles._llamar_modelo', return_value={}) as mock:
            analizar_sentimiento("texto", modelo="llama3.2")
            call_kwargs = mock.call_args
            assert call_kwargs.kwargs.get('modelo') == "llama3.2"


class TestExtraerEntidades:
    """Tests para extraer_entidades()."""

    def test_extraer_entidades(self):
        """Extrae entidades."""
        with patch('src.niveles._llamar_modelo', return_value={"personas": ["Juan"]}) as mock:
            resultado = extraer_entidades("Juan vive en Madrid")
            assert "personas" in resultado
            mock.assert_called_once()


class TestDetectarIntencion:
    """Tests para detectar_intencion()."""

    def test_detectar_intencion(self):
        """Detecta intención."""
        with patch('src.niveles._llamar_modelo', return_value={"intencion_principal": "soporte"}) as mock:
            resultado = detectar_intencion("No funciona mi pedido")
            assert "intencion_principal" in resultado
            mock.assert_called_once()


class TestClasificarTexto:
    """Tests para clasificar_texto()."""

    def test_clasificar_texto(self):
        """Clasifica texto."""
        with patch('src.niveles._llamar_modelo', return_value={"tema": "tecnico"}) as mock:
            resultado = clasificar_texto("Tengo un error en Python")
            assert "tema" in resultado
            mock.assert_called_once()


class TestResumirTexto:
    """Tests para resumir_texto()."""

    def test_resumir_texto(self):
        """Resume texto."""
        with patch('src.niveles._llamar_modelo', return_value={"resumen": "texto resumido"}) as mock:
            resultado = resumir_texto("Texto largo para resumir")
            assert resultado is not None
            mock.assert_called_once()


class TestAnalisisUnificado:
    """Tests para analisis_unificado()."""

    def test_analisis_unificado_llama_individual(self):
        """analisis_unificado llama a _analisis_individual."""
        with patch('src.niveles._analisis_individual', return_value={"sentimiento": {}}) as mock:
            analisis_unificado("texto")
            mock.assert_called_once()

    def test_analisis_unificado_pasa_modelo(self):
        """analisis_unificado pasa el modelo."""
        with patch('src.niveles._analisis_individual', return_value={}) as mock:
            analisis_unificado("texto", modelo="qwen2.5:3b")
            mock.assert_called_once_with("texto", modelo="qwen2.5:3b")


class TestAnalisisIndividual:
    """Tests para _analisis_individual()."""

    def test_analisis_individual_resultados(self):
        """Retorna todos los análisis."""
        with patch('src.niveles.analizar_sentimiento', return_value={}):
            with patch('src.niveles.extraer_entidades', return_value={}):
                with patch('src.niveles.detectar_intencion', return_value={}):
                    with patch('src.niveles.clasificar_texto', return_value={}):
                        with patch('src.niveles.resumir_texto', return_value={}):
                            resultado = _analisis_individual("texto")
                            assert "sentimiento" in resultado
                            assert "entidades" in resultado
                            assert "intencion" in resultado
                            assert "clasificacion" in resultado
                            assert "resumen" in resultado

    def test_analisis_individual_con_modelo(self):
        """Pasa modelo a todas las funciones."""
        with patch('src.niveles.analizar_sentimiento', return_value={}) as mock_sent:
            with patch('src.niveles.extraer_entidades', return_value={}):
                with patch('src.niveles.detectar_intencion', return_value={}):
                    with patch('src.niveles.clasificar_texto', return_value={}):
                        with patch('src.niveles.resumir_texto', return_value={}):
                            _analisis_individual("texto", modelo="qwen2.5:3b")
                            mock_sent.assert_called_once_with("texto", "qwen2.5:3b")

    def test_analisis_individual_maneja_excepciones(self):
        """Maneja excepciones en las tareas."""
        with patch('src.niveles.analizar_sentimiento', side_effect=Exception("Error")):
            with patch('src.niveles.extraer_entidades', return_value={}):
                with patch('src.niveles.detectar_intencion', return_value={}):
                    with patch('src.niveles.clasificar_texto', return_value={}):
                        with patch('src.niveles.resumir_texto', return_value={}):
                            resultado = _analisis_individual("texto")
                            assert isinstance(resultado, dict)