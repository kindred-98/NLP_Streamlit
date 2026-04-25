"""Tests para src/cliente.py - Conexiones y configuración."""

import pytest
from unittest.mock import patch, MagicMock
from src.cliente import (
    Config, Provider, get_provider, get_client, get_modelo,
    get_provider_name, is_ollama_available, is_lmstudio_available,
    _get_ollama_client, _get_openai_client, _get_lmstudio_client
)


class TestProviderEnum:
    """Tests para el enum Provider."""

    def test_provider_values(self):
        """Valores del enum."""
        assert Provider.OLLAMA.value == "ollama"
        assert Provider.OPENAI.value == "openai"
        assert Provider.HUGGINGFACE.value == "huggingface"
        assert Provider.LMSTUDIO.value == "lmstudio"


class TestConfig:
    """Tests para Config."""

    def test_config_tiene_atributos(self):
        """Config tiene los atributos necesarios."""
        assert hasattr(Config, 'PROVIDER')
        assert hasattr(Config, 'MODEL_OLLAMA')
        assert hasattr(Config, 'MODEL_LMSTUDIO')
        assert hasattr(Config, 'OLLAMA_URL')
        assert hasattr(Config, 'LMSTUDIO_URL')
        assert isinstance(Config.PROVIDER, str)


class TestGetProvider:
    """Tests para get_provider()."""

    def test_provider_valido(self):
        """Provider válido."""
        with patch.object(Config, 'PROVIDER', 'openai'):
            assert get_provider() == Provider.OPENAI

    def test_provider_valido_ollama(self):
        """Provider ollama."""
        with patch.object(Config, 'PROVIDER', 'ollama'):
            assert get_provider() == Provider.OLLAMA

    def test_provider_valido_huggingface(self):
        """Provider huggingface."""
        with patch.object(Config, 'PROVIDER', 'huggingface'):
            assert get_provider() == Provider.HUGGINGFACE

    def test_provider_valido_lmstudio(self):
        """Provider lmstudio."""
        with patch.object(Config, 'PROVIDER', 'lmstudio'):
            assert get_provider() == Provider.LMSTUDIO

    def test_provider_invalido_retorna_ollama(self):
        """Provider inválido retorna OLLAMA por defecto."""
        with patch.object(Config, 'PROVIDER', 'proveedor_invalido_xyz'):
            assert get_provider() == Provider.OLLAMA


class TestGetClient:
    """Tests para get_client()."""

    def test_get_client_ollama(self):
        """Client Ollama."""
        with patch('src.cliente.get_provider', return_value=Provider.OLLAMA):
            with patch('src.cliente._get_ollama_client') as mock:
                mock.return_value = MagicMock()
                client = get_client()
                assert client is not None

    def test_get_client_openai(self):
        """Client OpenAI."""
        with patch('src.cliente.get_provider', return_value=Provider.OPENAI):
            with patch('src.cliente._get_openai_client') as mock:
                mock.return_value = MagicMock()
                client = get_client()
                assert client is not None

    def test_get_client_lmstudio(self):
        """Client LMStudio."""
        with patch('src.cliente.get_provider', return_value=Provider.LMSTUDIO):
            with patch('src.cliente._get_lmstudio_client') as mock:
                mock.return_value = MagicMock()
                client = get_client()
                assert client is not None


class TestGetOllamaClient:
    """Tests para _get_ollama_client()."""

    def test_ollama_disponible(self):
        """Ollama disponible."""
        with patch('src.cliente.is_ollama_available', return_value=True):
            client = _get_ollama_client()
            assert client is not None

    def test_ollama_no_disponible_raise(self):
        """Ollama no disponible lanza error."""
        with patch('src.cliente.is_ollama_available', return_value=False):
            with pytest.raises(RuntimeError, match="Ollama no está disponible"):
                _get_ollama_client()


class TestGetOpenAIClient:
    """Tests para _get_openai_client()."""

    def test_openai_sin_api_key_raise(self):
        """OpenAI sin API key lanza error."""
        with patch.object(Config, 'OPENAI_API_KEY', ''):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                _get_openai_client()

    def test_openai_con_api_key(self):
        """OpenAI con API key."""
        with patch.object(Config, 'OPENAI_API_KEY', 'sk-test'):
            with patch('openai.OpenAI'):
                client = _get_openai_client()
                assert client is not None


class TestGetLMStudioClient:
    """Tests para _get_lmstudio_client()."""

    def test_lmstudio_client(self):
        """LMStudio client creado."""
        with patch('openai.OpenAI'):
            client = _get_lmstudio_client()
            assert client is not None


class TestIsAvailable:
    """Tests para is_ollama_available() e is_lmstudio_available()."""

    def test_ollama_available_true(self):
        """Ollama disponible."""
        with patch('socket.socket') as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value = mock_instance
            mock_instance.connect = MagicMock()
            mock_instance.close = MagicMock()
            assert is_ollama_available() is True

    def test_ollama_available_false_socket_error(self):
        """Ollama no disponible - socket error."""
        with patch('socket.socket') as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value = mock_instance
            mock_instance.connect.side_effect = OSError("Connection refused")
            assert is_ollama_available() is False

    def test_lmstudio_available_true(self):
        """LMStudio disponible."""
        with patch('socket.socket') as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value = mock_instance
            mock_instance.connect = MagicMock()
            mock_instance.close = MagicMock()
            assert is_lmstudio_available() is True

    def test_lmstudio_available_false(self):
        """LMStudio no disponible."""
        with patch('socket.socket') as mock_socket:
            mock_instance = MagicMock()
            mock_socket.return_value = mock_instance
            mock_instance.connect.side_effect = OSError("Connection refused")
            assert is_lmstudio_available() is False


class TestGetModelo:
    """Tests para get_modelo()."""

    def test_modelo_ollama(self):
        """Modelo Ollama."""
        with patch('src.cliente.get_provider', return_value=Provider.OLLAMA):
            assert get_modelo() == Config.MODEL_OLLAMA

    def test_modelo_lmstudio(self):
        """Modelo LMStudio."""
        with patch('src.cliente.get_provider', return_value=Provider.LMSTUDIO):
            assert get_modelo() == Config.MODEL_LMSTUDIO

    def test_modelo_openai(self):
        """Modelo OpenAI."""
        with patch('src.cliente.get_provider', return_value=Provider.OPENAI):
            assert get_modelo() == Config.MODEL_OPENAI

    def test_modelo_huggingface(self):
        """Modelo HuggingFace."""
        with patch('src.cliente.get_provider', return_value=Provider.HUGGINGFACE):
            assert get_modelo() == Config.MODEL_HF

    def test_modelo_default(self):
        """Modelo por defecto si provider no reconocido."""
        with patch('src.cliente.get_provider', return_value=Provider.OLLAMA):
            with patch.object(Config, 'PROVIDER', 'unknown'):
                assert get_modelo() == Config.MODEL_OLLAMA


class TestGetProviderName:
    """Tests para get_provider_name()."""

    def test_provider_name_ollama(self):
        """Nombre del proveedor Ollama."""
        with patch('src.cliente.get_provider', return_value=Provider.OLLAMA):
            assert get_provider_name() == "ollama"

    def test_provider_name_openai(self):
        """Nombre del proveedor OpenAI."""
        with patch('src.cliente.get_provider', return_value=Provider.OPENAI):
            assert get_provider_name() == "openai"

    def test_provider_name_huggingface(self):
        """Nombre del proveedor HuggingFace."""
        with patch('src.cliente.get_provider', return_value=Provider.HUGGINGFACE):
            assert get_provider_name() == "huggingface"

    def test_provider_name_lmstudio(self):
        """Nombre del proveedor LMStudio."""
        with patch('src.cliente.get_provider', return_value=Provider.LMSTUDIO):
            assert get_provider_name() == "lmstudio"