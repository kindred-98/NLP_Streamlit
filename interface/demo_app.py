import streamlit as st
import time
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path)

MODEL = os.getenv("NLP_MODEL_OLLAMA", os.getenv("NLP_MODEL", "qwen2.5:3b"))
PROVIDER = os.getenv("NLP_PROVIDER", "ollama").upper()

css_path = Path(__file__).parent.parent / "styles" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Sistema NLP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# JavaScript para detectar y aplicar tema
theme_script = """
<script>
(function() {
    var observer = new MutationObserver(function() {
        var html = document.documentElement;
        var body = document.body;
        
        var bgColor = getComputedStyle(body).backgroundColor;
        var rgb = bgColor.match(/\\d+/g);
        
        if (rgb && rgb.length >= 3) {
            var brightness = (parseInt(rgb[0]) * 299 + parseInt(rgb[1]) * 587 + parseInt(rgb[2]) * 114;
            if (brightness < 128) {
                html.setAttribute('data-theme', 'dark');
            } else {
                html.setAttribute('data-theme', 'light');
            }
        }
    });
    
    observer.observe(document.body, { 
        attributes: true, 
        attributeFilter: ['style', 'class'],
        subtree: true 
    });
    
    var bgColor = getComputedStyle(document.body).backgroundColor;
    var rgb = bgColor.match(/\\d+/g);
    if (rgb && rgb.length >= 3) {
        var brightness = (parseInt(rgb[0])) * 299 + parseInt(rgb[1]) * 587 + parseInt(rgb[2]) * 114;
        document.documentElement.setAttribute('data-theme', brightness < 128 ? 'dark' : 'light');
    }
})();
</script>
"""
st.markdown(theme_script, unsafe_allow_html=True)


# Constantes
DIV_CLOSE = '</div>'
ESTADO_MODELO = '### Estado del Modelo'
CARD_MODELO = '<div class="card-modelo">'


def formatear_valor(valor):
    """Formatea un valor para que sea legible."""
    if isinstance(valor, dict):
        if valor.get("raw"):
            texto = valor.get("raw", "")
            texto = texto.replace("\n", " ").replace("  ", " ").strip()
            return texto[:250] + ("..." if len(texto) > 250 else "")
        if valor.get("error"):
            return "No disponible"
        if not valor:
            return "N/A"
        
        for key, val in valor.items():
            if isinstance(val, dict):
                partes = []
                for k, v in val.items():
                    if v and k not in ["error", "raw"]:
                        if isinstance(v, list) and v:
                            partes.append(f"{k}: {', '.join(str(x) for x in v)}")
                        else:
                            partes.append(f"{k}: {v}")
                return " | ".join(partes) if partes else "N/A"
        
        partes = []
        for k, v in valor.items():
            if v and k not in ["error", "raw"]:
                if isinstance(v, list) and v:
                    partes.append(f"{k}: {', '.join(str(x) for x in v)}")
                else:
                    partes.append(f"{k}: {v}")
        return " | ".join(partes) if partes else "N/A"
    
    if isinstance(valor, list):
        if not valor:
            return "N/A"
        return ", ".join([str(v) for v in valor])
    
    if valor is None or valor == "":
        return "N/A"
    
    return str(valor)


IDIOMAS = {
    "ES": "Español",
    "EN": "English",
    "DE": "Deutsch",
    "PT": "Português",
    "FR": "Français"
}

TEXTOS = {
    "ES": {
        "titulo": "Análisis de Texto con IA",
        "entrada": "Texto de entrada",
        "analizar": "ANALIZAR",
        "sentimiento": "Sentimiento",
        "entidades": "Entidades (NER)",
        "intencion": "Intención",
        "resumen": "Resumen",
        "clasificacion": "Clasificación"
    },
    "EN": {
        "titulo": "AI Text Analysis",
        "entrada": "Input text",
        "analizar": "ANALYZE",
        "sentimiento": "Sentiment",
        "entidades": "Entities (NER)",
        "intencion": "Intent",
        "resumen": "Summary",
        "clasificacion": "Classification"
    },
    "DE": {
        "titulo": "KI-Textanalyse",
        "entrada": "Eingabetext",
        "analizar": "ANALYSIEREN",
        "sentimiento": "Stimmung",
        "entidades": "Entitäten (NER)",
        "intencion": "Absicht",
        "resumen": "Zusammenfassung",
        "clasificacion": "Klassifizierung"
    },
    "PT": {
        "titulo": "Análise de Texto com IA",
        "entrada": "Texto de entrada",
        "analizar": "ANALISAR",
        "sentimiento": "Sentimento",
        "entidades": "Entidades (NER)",
        "intencion": "Intenção",
        "resumen": "Resumo",
        "clasificacao": "Classificação"
    },
    "FR": {
        "titulo": "Analyse de Texte IA",
        "entrada": "Texte d'entrée",
        "analyser": "ANALYSER",
        "sentiment": "Sentiment",
        "entites": "Entités (NER)",
        "intention": "Intention",
        "resumen": "Résumé",
        "classification": "Classification"
    }
}

# Obtener modelo activo de Ollama
try:
    import requests
    resp = requests.get("http://localhost:11434/api/tags", timeout=2)
    if resp.status_code == 200:
        models = resp.json().get("models", [])
        MODELO_ACTIVO = models[0]["name"] if models else MODEL
        MODELOS_DISPONIBLES = [m["name"] for m in models] if models else [MODEL]
    else:
        MODELO_ACTIVO = MODEL
        MODELOS_DISPONIBLES = [MODEL]
except Exception:
    MODELO_ACTIVO = MODEL
    MODELOS_DISPONIBLES = [MODEL]


with st.sidebar:
    idioma_seleccionado = st.selectbox("🌐 Idioma:", list(IDIOMAS.keys()), format_func=lambda x: IDIOMAS[x], index=0)
    txt = TEXTOS.get(idioma_seleccionado, TEXTOS["ES"])
    
    st.markdown("---")
    modelo_seleccionado = st.selectbox("🤖 Modelo:", MODELOS_DISPONIBLES, index=0, key="modelo_select")
    
    st.markdown("## 📄 Información")
    st.markdown("### Capacidades:")
    st.markdown(f"""
- 🔵 {txt["sentimiento"]}  
- 🟢 {txt["entidades"]}  
- 🟡 {txt["intencion"]}  
- 🟠 {txt["resumen"]}  
- 🔴 {txt["clasificacion"]}  
""")
    st.markdown("---")
    guardar = st.checkbox("Guardar en logs/", value=True)
    debug = st.checkbox("Mostrar debug")
    st.markdown("---")
    st.markdown("**📥 Descargar resultado:**")
    
    if 'resultados' in st.session_state and st.session_state.resultados:
        descarga = st.selectbox("Formato:", ["JSON", "TXT"], label_visibility="collapsed")
        
        import json
        if descarga == "JSON":
            st.download_button(
                "Descargar JSON",
                data=json.dumps(st.session_state.resultados, indent=2, ensure_ascii=False),
                file_name="analisis.json",
                mime="application/json"
            )
        else:
            from src.utils import formatear_resultado
            st.download_button(
                "Descargar TXT",
                data=formatear_resultado(st.session_state.resultados),
                file_name="analisis.txt",
                mime="text/plain"
            )
    else:
        st.caption("⚠️ Sin resultados para descargar")
    
    from datetime import datetime
    st.markdown("---")
    st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


st.markdown(f"# 🧠 {txt['titulo']}")
st.markdown("Demostración de capacidades: Sentimiento, Entidades, Intención, Resumen y Clasificación")
st.markdown("---")

col1, col2 = st.columns([2, 1])


with col1:
    st.markdown(f"## 📝 {txt['entrada']}")
    
    ejemplos = {
        "Consulta técnica - Timeout en Python": "¿Alguien sabe como configurar el timeout en una conexión HTTP con Python? Estoy usando la librería requests y a veces se queda colgado cuando el servidor tarda más de 10 segundos.",
        "Queja de cliente": "Llevo tres días intentando contactar con soporte y nadie responde. Mi pedido #12345 debería haber llegado el martes y aún no ha llegado. Estoy muy molesto porque necesito el producto para un proyecto urgente.",
        "Solicitud de información": "Me gustaría saber más sobre los planes de precios de ustedes. Cuánto cuesta el plan profesional y qué incluye?"
    }
    
    ejemplo_seleccionado = st.selectbox("Cargar ejemplo:", list(ejemplos.keys()), key="ejemplo_select")
    
    with st.form(key="analisis_form"):
        texto = st.text_area(
            "Texto a analizar:",
            value=ejemplos[ejemplo_seleccionado],
            height=150,
            key="texto_input"
        )
        
        st.markdown("<div style='text-align:center; width:100%;'>", unsafe_allow_html=True)
        analizar = st.form_submit_button(f"🚀 {txt['analizar']}", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if analizar:
        if texto and texto.strip():
            with col2:
                status_container = st.container()
                with status_container:
                    st.markdown(ESTADO_MODELO)
                    st.markdown(CARD_MODELO, unsafe_allow_html=True)
                    st.markdown("**Analizando:**")
                    st.markdown("⏳ Sentimiento")
                    st.markdown("⏳ Entidades (NER)")
                    st.markdown("⏳ Intención")
                    st.markdown("⏳ Resumen")
                    st.markdown("⏳ Clasificación")
                    st.markdown(DIV_CLOSE, unsafe_allow_html=True)
            
            try:
                from src.analizador import analizar_texto
                from almacenamiento.guardar import guardar_resultado
                
                inicio = time.time()
                resultados = analizar_texto(texto, modelo=modelo_seleccionado)
                st.session_state.resultados = resultados
                if guardar:
                    guardar_resultado(texto, resultados)
                
                duracion = time.time() - inicio
                
                with col2:
                    status_container.empty()
                    with status_container:
                        st.markdown(ESTADO_MODELO)
                        st.markdown(CARD_MODELO, unsafe_allow_html=True)
                        st.markdown(f"**Completado en:** {duracion:.2f}s ✅")
                        st.markdown(f"**Modelo:** {modelo_seleccionado}")
                        st.markdown(f"**Proveedor:** {PROVIDER}")
                        st.markdown(DIV_CLOSE, unsafe_allow_html=True)
                
                tabs = st.tabs([txt["sentimiento"], txt["entidades"], txt["intencion"], txt["resumen"], txt["clasificacion"]])
                
                with tabs[0]:
                    sent = resultados.get("sentimiento", {})
                    if isinstance(sent, dict):
                        for k, v in sent.items():
                            if v and k != "error":
                                st.markdown(f"**{k.title()}:** {formatear_valor(v)}")
                    else:
                        st.markdown(f"**Resultado:** {formatear_valor(sent)}")
                
                with tabs[1]:
                    ents = resultados.get("entidades", {})
                    if ents:
                        for key, val in ents.items():
                            if val:
                                st.markdown(f"**{key.title()}:** {formatear_valor(val)}")
                    else:
                        st.markdown("No se detectaron entidades")
                
                with tabs[2]:
                    inte = resultados.get("intencion", {})
                    if isinstance(inte, dict):
                        for k, v in inte.items():
                            if v and k != "error":
                                st.markdown(f"**{k.title()}:** {formatear_valor(v)}")
                    else:
                        st.markdown(f"**Resultado:** {formatear_valor(inte)}")
                
                with tabs[3]:
                    res = resultados.get("resumen", {})
                    if isinstance(res, dict):
                        for nivel, contenido in res.items():
                            if contenido:
                                st.markdown(f"**{nivel.upper()}:** {formatear_valor(contenido)}")
                    else:
                        st.markdown(f"**Resumen:** {formatear_valor(res)}")
                
                with tabs[4]:
                    clas = resultados.get("clasificacion", {})
                    if isinstance(clas, dict):
                        for k, v in clas.items():
                            if v and k != "error":
                                st.markdown(f"**{k.title()}:** {formatear_valor(v)}")
                    else:
                        st.markdown(f"**Resultado:** {formatear_valor(clas)}")
            
            except Exception as e:
                with col2:
                    status_container.empty()
                    with status_container:
                        st.markdown(ESTADO_MODELO)
                        st.markdown('<div class="card-modelo" style="border-color: red;">', unsafe_allow_html=True)
                        st.markdown(f"❌ **Error:** {str(e)}")
                        st.markdown(DIV_CLOSE, unsafe_allow_html=True)
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Por favor, introduce un texto para analizar.")