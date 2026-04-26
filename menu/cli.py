"""NLP CLI - Análisis desde línea de comandos."""

from src.analizador import analizar_texto


def formatear_salida_cli(resultados: dict) -> str:
    """Formatea los resultados de forma limpia y legible."""
    lines = []
    
    # Sentimiento
    sent = resultados.get("sentimiento", {})
    emoji = "😊" if sent.get("sentimiento") == "positivo" else "😔" if sent.get("sentimiento") == "negativo" else "😐"
    lines.append(f"  {emoji} SENTIMIENTO: {sent.get('sentimiento', 'N/A').upper()}")
    lines.append(f"     Puntuación: {sent.get('puntuacion', 'N/A')}")
    lines.append(f"     Emociones: {', '.join(sent.get('emociones', [])) or 'Ninguna'}")
    lines.append(f"     Confianza: {sent.get('confianza', 'N/A')}")
    lines.append("")
    
    # Entidades
    ent = resultados.get("entidades", {})
    otros = ent.get("otros", [])
    lines.append(f"  🏷️ ENTIDADES: {', '.join(otros) if otros else 'Ninguna'}")
    lines.append("")
    
    # Intención
    inte = resultados.get("intencion", {})
    urgency = inte.get("urgencia", "N/A")
    emoji_urg = "🔴" if urgency == "alta" else "🟡" if urgency == "media" else "🟢"
    lines.append(f"  🎯 INTENCIÓN: {inte.get('intencion_principal', 'N/A').upper()}")
    lines.append(f"     {emoji_urg} Urgencia: {urgency.upper()}")
    lines.append("")
    
    # Clasificación
    clas = resultados.get("clasificacion", {})
    lines.append("  🗂️ CLASIFICACIÓN:")
    lines.append(f"     Tema: {clas.get('tema', 'N/A').upper()}")
    lines.append(f"     Tipo: {clas.get('tipo', 'N/A').upper()}")
    lines.append(f"     Canal: {clas.get('canal_adecuado', 'N/A').upper()}")
    lines.append(f"     Prioridad: {clas.get('prioridad', 'N/A')}")
    lines.append("")
    
    # Resumen
    res = resultados.get("resumen", {})
    resumen_raw = res.get("raw", "")[:200] if res.get("raw") else "N/A"
    lines.append("  📝 RESUMEN:")
    # Limitar a primer párrafo
    primer_parrafo = resumen_raw.split('\n')[0][:150]
    lines.append(f"     {primer_parrafo}...")
    
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