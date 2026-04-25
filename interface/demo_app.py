import streamlit as st
import time
import sys
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

# Cargar modelo desde .env
dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path)

# Obtener modelo y provider configurados
MODEL = os.getenv("NLP_MODEL_OLLAMA", os.getenv("NLP_MODEL", "qwen2.5:3b"))
PROVIDER = os.getenv("NLP_PROVIDER", "ollama").upper()

# Cargar estilos desde archivo externo
css_path = Path(__file__).parent.parent / "styles" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Config
st.set_page_config(
    page_title="Sistema NLP",
    layout="wide"
)


def formatear_valor(valor):
    """Formatea un valor para que sea legible."""
    # Si es dict con error y raw, devolver el raw limpio
    if isinstance(valor, dict):
        if valor.get("raw"):
            texto = valor.get("raw", "")
            texto = texto.replace("\n", " ").replace("  ", " ").strip()
            return texto[:250] + ("..." if len(texto) > 250 else "")
        if valor.get("error"):
            return "No disponible"
        if not valor:
            return "N/A"
        partes = []
        for k, v in valor.items():
            if v and k not in ["error", "raw"]:
                partes.append(f"{k}: {v}")
        return " | ".join(partes) if partes else "N/A"
    
    if isinstance(valor, list):
        if not valor:
            return "N/A"
        return ", ".join([str(v) for v in valor])
    
    if valor is None or valor == "":
        return "N/A"
    
    return str(valor)

# Sidebar - con modelo card y fecha/hora
with st.sidebar:
    st.markdown("## 📄 Informacion")
    st.markdown("### Capacidades:")
    st.markdown("""
- 🔵 Sentimiento  
- 🟢 Entidades (NER)  
- 🟡 Intencion  
- 🟠 Resumen  
- 🔴 Clasificacion  
""")
    st.markdown("---")
    st.markdown(f'<div class="card-modelo">Modelo: {MODEL}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Requisito:** Ollama corriendo localmente")
    st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Header
st.markdown("# 🧠 Sistema de Analisis NLP")
st.markdown("Demostracion de capacidades: Sentimiento, Entidades, Intencion, Resumen y Clasificacion")
st.markdown("---")

# Layout principal
col1, col2 = st.columns([2, 1])

# Input
with col1:
    st.markdown("## 📝 Texto de entrada")
    
    ejemplos = {
        "Consulta tecnica - Timeout en Python": "¿Alguien sabe como configurar el timeout en una conexion HTTP con Python? Estoy usando la libreria requests y a veces se queda colgado cuando el servidor tarda mas de 10 segundos.",
        "Queja de cliente": "Llevo tres dias intentando contactar con soporte y nadie responde. Mi pedido #12345 deberia haber llegado el martes y aun no ha llegado. Estoy muy molesto porque necesito el producto para un proyecto urgente.",
        "Solicitud de informacion": "Me gustaria saber mas sobre los planes de precios de ustedes. Cuanto cuesta el plan profesional y que incluye?"
    }
    
    ejemplo_seleccionado = st.selectbox("Cargar ejemplo:", list(ejemplos.keys()))
    
    texto = st.text_area(
        "Texto a analizar:",
        value=ejemplos[ejemplo_seleccionado],
        height=150
    )

    # BOTÓN CENTRADO Y ANCHO COMPLETO
    st.markdown("<div style='text-align:center; width:100%;'>", unsafe_allow_html=True)
    analizar = st.button("🚀 ANALIZAR", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if analizar:
        if texto and texto.strip():
            try:
                from src.analizador import analizar_texto
                from almacenamiento.guardar import guardar_resultado
                from src.utils import formatear_resultado
                
                # Iniciar cronómetro
                inicio = time.time()
                
                with st.spinner("Analizando..."):
                    resultados = analizar_texto(texto)
                    guardar_resultado(texto, resultados)
                
                # Tiempo de análisis
                duracion = time.time() - inicio
                
                st.success(f"✅ Analisis completado en {duracion:.2f}s")
                
                tabs = st.tabs(["Sentimiento", "Entidades", "Intencion", "Resumen", "Clasificacion"])
                
                with tabs[0]:
                    sent = resultados.get("sentimiento", {})
                    st.markdown(f"**Sentimiento:** {formatear_valor(sent.get('sentimiento'))}")
                    st.markdown(f"**Puntuacion:** {formatear_valor(sent.get('puntuacion'))}")
                    st.markdown(f"**Emociones:** {formatear_valor(sent.get('emociones'))}")
                    st.markdown(f"**Confianza:** {formatear_valor(sent.get('confianza'))}")
                
                with tabs[1]:
                    ents = resultados.get("entidades", {})
                    for key, val in ents.items():
                        if val:
                            st.markdown(f"**{key.capitalize()}:** {formatear_valor(val)}")
                
                with tabs[2]:
                    inte = resultados.get("intencion", {})
                    for key, val in inte.items():
                        if val:
                            st.markdown(f"**{key}:** {formatear_valor(val)}")
                
                with tabs[3]:
                    res = resultados.get("resumen", {})
                    for nivel, contenido in res.items():
                        st.markdown(f"**{nivel}:** {formatear_valor(contenido)}")
                
                with tabs[4]:
                    clas = resultados.get("clasificacion", {})
                    for key, val in clas.items():
                        if val:
                            st.markdown(f"**{key}:** {formatear_valor(val)}")
                            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Por favor, introduce un texto para analizar.")

# Config - simplificado
with col2:
    st.markdown("## ⚙️ Configuracion")
    guardar = st.checkbox("Guardar en logs/", value=True)
    debug = st.checkbox("Mostrar debug")
    
    if debug and 'resultados' in dir():
        with st.expander("Debug"):
            st.code(formatear_resultado(resultados))