"""NLP CLI - Análisis desde línea de comandos."""

from src.analizador import analizar_texto

EMOJI_SENTIMIENTO = {
    "positivo": "😊",
    "negativo": "😔",
    "neutro": "😐",
}

EMOJI_URGENCIA = {
    "alta": "🔴",
    "media": "🟡",
    "baja": "🟢",
}


def _emoji(mapa: dict, valor, por_defecto: str) -> str:
    """Devuelve el emoji asociado a un valor de forma segura."""
    return mapa.get(str(valor), por_defecto)


def formatear_salida_cli(resultados: dict) -> str:
    """Formatea los resultados de forma limpia y legible."""
    lines = []
    
    # Sentimiento
    sent = resultados.get("sentimiento", {})
    emoji = _emoji(EMOJI_SENTIMIENTO, sent.get("sentimiento"), "😐")
    lines.extend([
        f"  {emoji} SENTIMIENTO: {sent.get('sentimiento', 'N/A').upper()}",
        f"     Puntuación: {sent.get('puntuacion', 'N/A')}",
        f"     Emociones: {', '.join(sent.get('emociones', [])) or 'Ninguna'}",
        f"     Confianza: {sent.get('confianza', 'N/A')}",
        "",
    ])
    
    # Entidades
    ent = resultados.get("entidades", {})
    otros = ent.get("otros", [])
    lines.extend([
        f"  🏷️ ENTIDADES: {', '.join(otros) if otros else 'Ninguna'}",
        "",
    ])
    
    # Intención
    inte = resultados.get("intencion", {})
    urgency = inte.get("urgencia", "N/A")
    emoji_urg = _emoji(EMOJI_URGENCIA, urgency, "🟢")
    lines.extend([
        f"  🎯 INTENCIÓN: {inte.get('intencion_principal', 'N/A').upper()}",
        f"     {emoji_urg} Urgencia: {urgency.upper()}",
        "",
    ])
    
    # Clasificación
    clas = resultados.get("clasificacion", {})
    lines.extend([
        "  🗂️ CLASIFICACIÓN:",
        f"     Tema: {clas.get('tema', 'N/A').upper()}",
        f"     Tipo: {clas.get('tipo', 'N/A').upper()}",
        f"     Canal: {clas.get('canal_adecuado', 'N/A').upper()}",
        f"     Prioridad: {clas.get('prioridad', 'N/A')}",
        "",
    ])
    
    # Resumen
    res = resultados.get("resumen", {})
    resumen_raw = res.get("raw", "")[:200] if res.get("raw") else "N/A"
    # Limitar a primer párrafo
    primer_parrafo = resumen_raw.split('\n')[0][:150]
    lines.extend([
        "  📝 RESUMEN:",
        f"     {primer_parrafo}...",
    ])
    
    return "\n".join(lines)


def ejecutar_cli():
    """CLI interactivo para analizar texto."""
    print("\n💻 CLI Mode - Escribe 'salir' para volver")
    print("-" * 40)
    
    while True:
        try:
            texto = input("\n📝 Texto a analizar (o 'salir'): ").strip()
            
            if texto.lower() in ["salir", "exit", "quit"]:
                break
            
            if not texto:
                print("⚠️  Escribe algo...")
                continue
            
            print("🔄 Analizando...")
            resultados = analizar_texto(texto)
            
            print("\n" + "=" * 45)
            print("📊 RESULTADOS DEL ANÁLISIS")
            print("=" * 45)
            print(formatear_salida_cli(resultados))
            print("=" * 45 + "\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True


if __name__ == "__main__":
    ejecutar_cli()