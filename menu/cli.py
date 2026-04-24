"""NLP CLI - Análisis desde línea de comandos."""

from src.analizador import analizar_texto
from src.utils import formatear_resultado


def ejecutar_cli():
    """CLI interactivo para analizar texto."""
    print("\n💻 CLI Mode - Escribe 'salir' para volver")
    print("-" * 40)
    
    while True:
        try:
            texto = input("\nTexto a analizar (o 'salir'): ").strip()
            
            if texto.lower() in ["salir", "exit", "quit"]:
                break
            
            if not texto:
                print("⚠️  Escribe algo...")
                continue
            
            print("🔄 Analizando...")
            resultados = analizar_texto(texto)
            print("\n" + "=" * 40)
            print(formatear_resultado(resultados))
            print("=" * 40 + "\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True


if __name__ == "__main__":
    ejecutar_cli()