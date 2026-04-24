import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def texto_ejemplo():
    """Texto de ejemplo para tests."""
    return "Me gusta este producto, es genial"


@pytest.fixture
def texto_vario():
    """Texto con róż característiques."""
    return "Llevo tres días intentando contactar con soporte y nadie responde. Mi pedido #12345 debería haber llegado el martes."


@pytest.fixture
def resultado_ejemplo():
    """Resultado NLP de ejemplo."""
    return {
        "sentimiento": {"sentimiento": "negativo", "puntuacion": 0.2},
        "entidades": {"personas": [], "lugares": []},
        "intencion": {"intencion_principal": "queja", "urgencia": "alta"},
        "clasificacion": {"tema": "soporte", "prioridad": 1},
        "resumen": {"ultracorto": "Resumen", "medio": ["punto1"], "detallado": "detallado"}
    }