# NLP con Ollama + Streamlit

Aplicación web de procesamiento de lenguaje natural (NLP) con modelo local.

## Descripción

Sistema de análisis NLP que procesa texto en tiempo real utilizando un modelo local (Ollama).

Incluye:
- Análisis de sentimiento
- Extracción de entidades (NER)
- Detección de intención
- Resumen automático (3 niveles)
- Clasificación de texto

## Requisitos

- Python 3.11+
- [Ollama](https://ollama.com) instalado y ejecutándose

## Instalación

```bash
git clone <repo-url>
cd NLP_Streamlit
pip install -r requirements.txt

# En otra terminal: iniciar Ollama
ollama serve

# Descargar modelo (si no lo tienes)
ollama pull qwen2.5:0.5b
```

## Configuración

Crear archivo `.env` en la raíz del proyecto:

```
OPENAI_API_KEY=ollama
MODELO_NLP=qwen2.5:0.5b
```

## Uso — Interfaz Web

```bash
streamlit run interface/demo_app.py
```

Abre `http://localhost:8501` en el navegador.

## Uso — CLI

```bash
# Analizar texto
python main.py "Texto a analizar"

# Analizar y guardar resultado
python main.py "Texto a analizar" --guardar

# Listar análisis guardados
python main.py --listar
```

## Tests

```bash
pytest tests/ -v
```

## Estructura del Proyecto

```
NLP_Streamlit/
├── main.py                    # CLI entrypoint
├── src/                    # Lógica NLP
│   ├── cliente.py          # Cliente Ollama/OpenAI
│   ├── analizador.py     # Orquestador
│   ├── niveles.py       # Funciones NLP
│   └── utils.py        # Helpers
├── almacenamiento/            # Persistencia
│   ├── guardar.py
│   └── leer.py
├── interface/            # Interfaz Streamlit
│   └── demo_app.py
├── tests/               # Tests unitarios
├── docs/                # Documentación
├── resultados/           # Análisis guardados
│   ├── txt/
│   └── json/
├── .github/workflows/    # CI/CD
└── scripts/             # Scripts utility
```

## Pipeline CI/CD

El proyecto usa GitHub Actions para:
- Linting (ruff)
- Tests (pytest)
- Cobertura
- Seguridad (bandit)

## Almacenamiento

Los análisis se guardan automáticamente en:
- `resultados/txt/` — Formato legible
- `resultados/json/` — Formato estructurado

Cada archivo tiene timestamp único para evitar sobrescritura.

## Documentación

- [Arquitectura](docs/arquitectura.md)
- [Almacenamiento](docs/almacenamiento.md)
- [API Referencia](docs/api_referencia.md)
- [Guía Streamlit](docs/streamlit_guia.md)

## Licencia

MIT