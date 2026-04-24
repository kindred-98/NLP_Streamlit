"""NLP - Menú Principal."""

import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()


MODELOS = {
    "1": ("qwen2.5:3b", "Qwen 2.5 - Más rápido (1.9 GB)"),
    "2": ("llama3.2", "Llama 3.2 - Mejor calidad (2.0 GB)"),
    "3": ("mistral", "Mistral - Balance (4.4 GB)"),
}


def mostrar_menu_modelos():
    print("\n" + "=" * 50)
    print("🧠  SELECCIONA MODELO")
    print("=" * 50)
    for key, (nombre, desc) in MODELOS.items():
        print(f"  {key}️⃣  {nombre:12} - {desc}")
    print("\n" + "-" * 50)


def seleccionar_modelo() -> str:
    """Permite seleccionar el modelo."""
    mostrar_menu_modelos()
    opcion = input("Modelo [1-3]: ").strip()
    
    if opcion in MODELOS:
        modelo = MODELOS[opcion][0]
        
        # Actualizar .env
        with open(".env", "r", encoding="utf-8") as f:
            contenido = f.read()
        
        contenido = contenido.replace(
            "NLP_MODEL_OLLAMA=llama3.2",
            f"NLP_MODEL_OLLAMA={modelo}"
        ).replace(
            "NLP_MODEL_OLLAMA=mistral",
            f"NLP_MODEL_OLLAMA={modelo}"
        ).replace(
            "NLP_MODEL_OLLAMA=qwen2.5:3b",
            f"NLP_MODEL_OLLAMA={modelo}"
        )
        
        # Si no existe, añadir
        if "NLP_MODEL_OLLAMA=" not in contenido:
            contenido += f"\nNLP_MODEL_OLLAMA={modelo}"
        
        with open(".env", "w", encoding="utf-8") as f:
            f.write(contenido)
        
        print(f"\n✅ Modelo seleccionado: {modelo}")
        return modelo
    
    print("\n❌ Opción no válida.")
    return None


def mostrar_menu():
    print("\n" + "=" * 50)
    print("🧠  SISTEMA NLP - MENÚ PRINCIPAL")
    print("=" * 50)
    print("\nSelecciona una opción:")
    print("  1️⃣  GUI (Streamlit)     - Interfaz web")
    print("  2️⃣  CLI               - Línea de comandos")
    print("  3️⃣  ElegirModelo     - Cambiar modelo")
    print("  4️⃣  Salir            - Salir del programa")
    print("\n" + "-" * 50)


def ejecutar_opcion(opcion: str) -> bool:
    """Ejecuta la opción seleccionada."""
    
    if opcion == "1":
        print("\n🚀 Iniciando GUI...")
        print("   URL: http://localhost:8501")
        print("   Presiona Ctrl+C para salir\n")
        
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", 
                "interface/demo_app.py"
            ], check=True)
        except KeyboardInterrupt:
            print("\n👤 GUI cerrada.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return True
    
    elif opcion == "2":
        print("\nEjecutando CLI...")
        from menu.cli import ejecutar_cli
        ejecutar_cli()
        return True
    
    elif opcion == "3":
        print("\n📦 Seleccionando modelo...")
        seleccionar_modelo()
        return True
    
    elif opcion == "4":
        print("\n👋 ¡Hasta luego!\n")
        return False
    
    else:
        print("\n❌ Opción no válida.")
        return True


def main():
    """Menú principal."""
    while True:
        mostrar_menu()
        opcion = input("Opcion [1-4]: ").strip()
        
        if not ejecutar_opcion(opcion):
            break


if __name__ == "__main__":
    main()