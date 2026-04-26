# 🧠 Sistema de Análisis NLP con Ollama + Streamlit

_Aplicación web de procesamiento de lenguaje natural (NLP) con modelo local usando Ollama and Streamlit._

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)](https://streamlit.io)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/tu-usuario/NLP_Streamlit)
[![Tests](https://img.shields.io/badge/Tests-143%20passed-green)](https://pytest.org)
[![Coverage](https://img.shields.io/badge/coverage-96%25-green)](https://coverage.io)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![CI](https://github.com/tu-usuario/NLP_Streamlit/actions/workflows/ci.yml/badge.svg)](https://github.com/tu-usuario/NLP_Streamlit/actions)

---

## 📸 Demo

![Demo de la aplicación](Docs/InterfazNueva.png)

---

## ⚡ Quick Start (TL;DR)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar Ollama (en otra terminal)
ollama serve

# 3. Correr la app
streamlit run interface/demo_app.py
```

_¿Fácil?:_arrow_right: Abre **http://localhost:8501** y listo.

---

## 📋 Tabla de Contenidos

1. [Demo](#-demo)
2. [Quick Start](#-quick-start-tldr)
3. [¿Qué es esta app?](#-qué-es-esta-app)
4. [Características](#-características)
5. [Requisitos Previos](#-requisitos-previos)
6. [Instalación](#-instalación)
7. [Configuración](#-configuración)
8. [Cómo Usar](#-cómo-usar)
9. [Estructura del Proyecto](#-estructura-del-proyecto)
10. [Desarrollo](#-desarrollo)
11. [Documentación Adicional](#-documentación-adicional)
12. [Changelog](#-changelog)
13. [Código de Conducta](#-código-de-conducta)
14. [Política de Seguridad](#-política-de-seguridad)
15. [Soporte](#-soporte)
16. [Contribuir](#-contribuir)
17. [Autor](#-autor)
18. [Licencia](#-licencia)

---

## 🧠 ¿Qué es esta app?

Esta es una **aplicación de análisis de texto basada en inteligencia artificial** que procesa lenguaje natural utilizando modelos locales de Ollama (como qwen2.5, llama3, etc.). No requiere conexión a APIs externas ni pagos — todo funciona offline en tu computadora.

La app analiza cualquier texto que le ingrenses y te devuelve:

- **Sentimiento**: ¿El tono es positivo, negativo o neutral?
- **Entidades**: ¿Qué personas, lugares, tecnologías, conceptos aparecen?
- **Intención**: ¿Qué quiere hacer el usuario? (información, soporte, compra,...)
- **Resumen**: Versión corta del texto (3 niveles: corto, medio, detallado)
- **Clasificación**: Tema, tipo, prioridad y canal recomendado

### 🎯 Para qué sirve?

| Caso de uso | Ejemplo |
|------------|---------|
| **Soporte técnico** | Analizar tickets de usuarios para detectar urgencia y categoría |
| **Análisis de feedback** | Procesar reseñas o comentarios de clientes |
| **Clasificación automática** | Organizar documentos o tickets por tema/prioridad |
| **Asistencia IA** | Resumir conversaciones o transcripciones |
| **Educación** | Extraer entidades y conceptos técnicos de textos |

---

## ✨ Características

| Característica | Descripción |
|---------------|------------|
| 🤖 **Modelos locales** | Funciona con Ollama (no requiere API externa) |
| 🌐 **Multidioma** | Español, Inglés, Alemán |
| 🎨 **Interfaz moderna** | Tema oscuro/claro automático con Streamlit |
| 🔴 **Botón rojo** | Diseño profesionales estilo SaaS |
| 📊 **Dashboard** | Tarjetas con resultados en tiempo real |
| 📥 **Descarga** | Exportar resultados en JSON o TXT |
| 💾 **Historial** | Guardar y recuperar análisis anteriores |
| ⏱️ **Rápido** | Análisis paralelo en ~3-5 segundos |
| 🧪 **Tests** | 143 tests con 96% de cobertura |
| 🔒 **Seguro** | Scan de seguridad con Bandit |

---

## 📦 Requisitos Previos

### Software necesario

| Requisito | Versión | Para qué |
|----------|--------|---------|
| **Python** | 3.10, 3.11, 3.12, 3.13 | Ejecutar la app |
| **Ollama** | Última versión | Correr modelos locales |

### Instalar Ollama

```bash
# Mac/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows (desde PowerShell)
winget install Ollama.Ollama
```

### Descargar modelo

```bash
# Recomendado: qwen2.5 (rápido y preciso)
ollama pull qwen2.5:3b

# Alternativas (más grandes)
ollama pull llama3.2
ollama pull mistral
```

---

## 🚀 Instalación

### 1. Clonar el proyecto

```bash
git clone <tu-repo-url>
cd NLP_Streamlit
```

### 2. Crear entorno virtual (recomendado)

```bash
# Crear entorno
python -m venv venv

# Activar
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar instalación

```bash
# Ver que Ollama funciona
ollama list

# Probar que Python tiene las dependencias
python -c "import streamlit; print('OK')"
```

---

## ⚙️ Configuración

### Archivo .env

Crear un archivo `.env` en la raíz del proyecto:

```bash
# Copia el ejemplo
cp .env.example .env
```

### Variables disponibles

| Variable | Default | Descripción |
|----------|---------|-----------|
| `NLP_PROVIDER` | `ollama` | Proveedor: ollama, openai, huggingface, lmstudio |
| `NLP_MODEL_OLLAMA` | `qwen2.5:3b` | Modelo para Ollama |
| `NLP_MODEL_OPENAI` | `gpt-4o-mini` | Modelo para OpenAI (si usas) |
| `NLP_MODEL_LMSTUDIO` | `tinyllama-1.1b` | Modelo para LMStudio |
| `OLLAMA_URL` | `http://localhost:11434/v1` | URL de Ollama |
| `LMSTUDIO_URL` | `http://localhost:1234/v1` | URL de LMStudio |
| `OPENAI_API_KEY` | _(vacío)_ | Tu API key de OpenAI |

### Ejemplo .env

```bash
# Proveedor local (recomendado)
NLP_PROVIDER=ollama
NLP_MODEL_OLLAMA=qwen2.5:3b
```

---

## 📖 Cómo Usar

### Opción 1: Interfaz Web (Recomendado)

```bash
streamlit run interface/demo_app.py
```

Luego abre: **http://localhost:8501**

#### Guía de la interfaz

```
┌─────────────────────────────────────────────────────────┐
│  🌐 Selector de idioma: ES | EN | DE                    │
│  🤖 Selector de modelo: qwen2.5:3b (de Ollama)          │
│                                                         │
│  📄 Información                                         │
│  - 🔵 Sentimiento                                       │
│  - 🟢 Entidades (NER)                                   │
│  - 🟡 Intención                                         │
│  - 🟠 Resumen (3 niveles)                               │
│  - 🔴 Clasificación                                     │
│                                                         │
│  ☐ Guardar en logs/                                     │
│  ☐ Mostrar debug                                        │
│                                                         │
│  📥 Descargar: [JSON] [TXT]                             │
├─────────────────────────────────────────────────────────┤
│  # 🧠 Sistema de Análisis NLP                           │
│                                                         │
│  [📝 Texto de entrada....................] [ANALIZAR]   │
│                                                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐                    │
│  │Sentim.  │ │Entidades│ │Intención│                    │
│  └─────────┘ └─────────┘ └─────────┘                    │
│                                                         │
│  ┌─────────┐ ┌─────────┐                                │
│  │Resumen  │ │Clasif.  │                                │
│  └─────────┘ └─────────┘                                │
└─────────────────────────────────────────────────────────┘
```

### Opción 2: Línea de comandos (CLI)

```bash
# Analizar un texto
python main.py "Tengo un problema con el timeout en Python"

# Analizar y guardar resultado
python main.py "Mi pedido no llegó" --guardar

# Ver historial de análisis
python main.py --listar

# Leer análisis específico
python main.py --leer analisis_2024-01-15_123456.json
```

### Ejemplo de salida

```json
{
  "sentimiento": {
    "sentimiento": "negativo",
    "puntuacion": 0.7,
    "emociones": ["frustracion", "impaciencia"],
    "confianza": 0.9
  },
  "entidades": {
    "personas": [],
    "organizaciones": [],
    "lugares": [],
    "fechas": [],
    "cantidades": [],
    "otros": ["Python", "timeout", "HTTP"]
  },
  "intencion": {
    "intencion_principal": "soporte",
    "subcategoria": "conexión",
    "urgencia": "alta",
    "accion_sugerida": "verificar logs"
  },
  "clasificacion": {
    "tema": "tecnico",
    "tipo": "pregunta",
    "canal_adecuado": "chat",
    "prioridad": 2
  },
  "resumen": "El usuario tiene un problema de timeout"
}
```

---

## 📂 Estructura del Proyecto

```
NLP_Streamlit/
├── main.py                    # Entry point CLI
├── requirements.txt           # Dependencias Python
├── .env.example              # Ejemplo de configuración
├── .github/workflows/ci.yml # CI/CD GitHub Actions
│
├── src/                      # Núcleo NLP
│   ├── __init__.py
│   ├── cliente.py            # Conexión a Ollama/OpenAI
│   ├── analizador.py        # Orquestador principal
│   ├── niveles.py          # Funciones de análisis (prompts)
│   ├── utils.py             # Utilidades (parseo JSON)
│   └── config.py            # Configuración y logging
│
├── interface/                # Interfaz Streamlit
│   └── demo_app.py          # App principal
│
├── almacenamiento/              # Persistencia
│   ├── guardar.py          # Guardar resultados
│   ├── leer.py            # Leer resultados
│   └── __init__.py
│
├── menu/                    # Menú CLI
│   ├── cli.py
│   └── menu_principal.py
│
├── styles/                  # Estilos CSS
│   └── style.css
│
├── scripts/                 # Scripts utility
│   └── check_folders.py
│
├── tests/                   # Tests unitarios
│   ├── test_cliente.py
│   ├── test_niveles.py
│   ├── test_utils.py
│   ├── test_analizador.py
│   ├── test_guardar.py
│   ├── test_leer.py
│   ├── test_integracion.py
│   └── conftest.py
│
├── resultados/              # Análisis guardados (auto-creado)
│   ├── txt/
│   └── json/
│
├── Docs/                   # Documentación
│   ├── arquitectura.md
│   ├── api_referencia.md
│   ├── almacenamiento.md
│   ├── streamlit_guia.md
│   └── Bloque_Resuelto/
│
└── .gitignore
```

---

## 📚 Documentación Adicional

| Documento | Descripción |
|----------|-------------|
| [Arquitectura](Docs/arquitectura.md) | Diseño técnico del sistema |
| [Almacenamiento](Docs/almacenamiento.md) | Cómo se guardan los datos |
| [API Referencia](Docs/api_referencia.md) | Referencia de funciones |
| [Guía Streamlit](Docs/streamlit_guia.md) | Tips de Streamlit |

---

## 🔧 Desarrollo

### Ejecutar tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest --cov=src --cov=almacenamiento --cov-report=term-missing
```

### Linting

```bash
# Verificar código
ruff check .

# Arreglar errores automáticos
ruff check --fix
```

### Seguridad

```bash
# Scan de seguridad
bandit -r src
```

### CI/CD

El proyecto incluye GitHub Actions que corre automáticamente:
- ✅ Linting (ruff)
- ✅ Tests (pytest)
- ✅ Cobertura (80% mínimo)
- ✅ Seguridad (bandit)

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva`)
3. Commit tus cambios (`git commit -am 'Agrega nueva feature'`)
4. Push a la rama (`git push origin feature/nueva`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la licencia **MIT**. Ver [LICENSE](LICENSE) para más detalles.

---

## ❓ FAQ

### ¿Puedo usar otro modelo?

Sí, cambia `NLP_MODEL_OLLAMA` en `.env`:

```bash
NLP_MODEL_OLLAMA=llama3.2
NLP_MODEL_OLLAMA=mistral
NLP_MODEL_OLLAMA=phi3
```

### ¿Necesito internet?

Solo para instalar dependencias. El modelo corre offline.

### ¿Cuánta RAM necesito?

| Modelo | RAM mínima |
|--------|------------|
| qwen2.5:3b | ~4 GB |
| llama3.2 | ~4 GB |
| mistral | ~4 GB |
| phi3 | ~2 GB |

### ¿Error "Connection refused"?

Asegúrate que Ollama está corriendo:

```bash
ollama serve
```

### ¿Cómo cambio el idioma?

En la sidebar hay un selector: **ES | EN | DE**


---

## 🔄 Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.

### [v1.0.0] - 2026-04-26

#### Added
- 🎉 Lanzamiento inicial
- 📊 Análisis de sentimiento (positivo/negativo/neutral)
- 🏷️ Extracción de entidades (NER) - personas, lugares, tecnologías, conceptos
- 🎯 Detección de intención (información, soporte, compra, queja, sugerencia)
- 📝 Resumen en 3 niveles (corto, medio, detallado)
- 🗂️ Clasificación multicategoría (tema, tipo, prioridad, canal)
- 🌐 Interfaz multidioma (ES, EN, DE)
- 🎨 Interfaz Streamlit con tema oscuro/claro automático
- 💾 Sistema de guardado automático (JSON + TXT)
- 📥 Descarga de resultados
- 🖥️ CLI y Web
- 🧪 143 tests con 96% cobertura
- 🔒 Security scan con Bandit
- ⚙️ CI/CD con GitHub Actions

#### Known Issues
- El modelo puede dar respuestas incompletas con textos muy largos
- Requiere Ollama corriendo localmente

---

## 📜 Código de Conducta

Este proyecto adhere al Covenant de Contributor. Al participar, te comprometes a uphold este código.

### Our Pledge

Nosotros como miembros, líderes y contribuidores pledge a hacer de la participación en nuestra comunidad una experiencia libre de acoso para todos.

### Our Standards

Ejemplos de comportamiento que contribuyen a un ambiente positivo:
- ✅ Usar lenguaje acogedor e inclusivo
- ✅ Respetar opiniones y experiencias diferentes
- ✅ Aceptar críticas constructivas con gracia
- ✅ Enfocarse en lo que es mejor para la comunidad
- ✅ Mostrar empatía hacia otros miembros

Ejemplos de comportamiento inaceptable:
- ❌ Comentarios acosadores o discriminatorios
- ❌ Comentarios insultantes o degradantes
- ❌ Ataques personales o políticos
- ❌ Acoso público o privado
- ❌ Información privada de otros sin permiso

### Our Responsibilities

Los líderes del proyecto son responsables de clarificar los estándares de comportamiento aceptable y deben tomar acción correctiva apropiada ante instancias de comportamiento inaceptable.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the community leaders at tu@email.com. All complaints will be reviewed and investigated fairly.

---

## 🔐 Política de Seguridad

### Supported Versions

| Versión | Soportada |
|---------|----------|
| 1.0.x | ✅ Sí |

### Reported a Vulnerabilities

Si encontrás una vulnerabilidad de seguridad, por favor repórtala por email a **angelechenique134@email.com** en lugar de abrir un issue público.

Por favor incluye:
1. Título descriptivo
2. Descripción completa
3. Pasos para reproducir
4. Posible solución (si la conocés)

### Response Timeline
- ✅ Acknowledgment: 24-48 horas
- ✅ Propuesta de fix: 7 días
- ✅ Release del fix: según gravedad

---

## 💬 Soporte

### Cómo obtener ayuda

| Canal | Cuándo usar | Tiempo de respuesta |
|-------|------------|-----------------|
| **GitHub Issues** | Bugs, feature requests | 24-48 horas |
| **Email** | Seguridad / privado | 24 horas |
| **Discussions** | Preguntas generales | 48 horas |

### Cómo apoyar el proyecto

| Forma | Cómo |
|-------|------|
| ⭐ **Star** | Dale una estrella en GitHub |
| 🍴 **Fork** | Hacé tu propio derivado |
| 📢 **Compartir** | Repostéalo en redes |
| 💡 **Ideas** | Abrí una discusión con sugerencias |
| 🐛 **Bug report** | Reportá issues con detalles |
| 📝 **Docs** | Mejora la documentación |

### Antes de pedir ayuda

1. 📖 Lee el README completo
2. 🔍 Busca en Issues existentes
3. 🧪 Verifica con los tests (`pytest tests/`)

### Información a incluir en tu Issue

```markdown
### Descripción
[Descripción clara del problema]

### Pasos para reproducir
1. npm install
2. streamlit run interface/demo_app.py
3. Escribo "texto de prueba"

### Comportamiento esperado
[Lo que esperás que pase]

### Comportamiento real
[Lo que realmente pasa]

### Environment
- OS: [Windows/Mac/Linux]
- Python: 3.x
- Ollama: versión
```

---

## ⭐ Créditos

- [Ollama](https://ollama.com) - Modelos locales
- [Streamlit](https://streamlit.io) - Interfaz web
- [OpenAI](https://openai.com) - Compatibilidad API

---

## 👤 Autor

**Nombre**: Angel.DEV

**Email**: angelechenique134@email.com

**GitHub**: https://github.com/kindred-98

**LinkedIn**: https://www.linkedin.com/in/kindred98/

_¿Te gusta este proyecto? Dale ⭐ en GitHub!_