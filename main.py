"""NLP Streamlit - CLI Entry Point."""

import sys
import argparse
from src.analizador import analizar_texto
from src.utils import validar_texto, formatear_resultado
from almacenamiento.guardar import guardar_resultado
from almacenamiento.leer import listar_analisis, leer_ultimo


def main():
    """Punto de entrada CLI."""
    parser = argparse.ArgumentParser(description="NLP CLI - Análisis de texto")
    parser.add_argument("texto", nargs="?", help="Texto a analizar")
    parser.add_argument("--guardar", "-g", action="store_true", help="Guardar resultados")
    parser.add_argument("--listar", "-l", action="store_true", help="Listar análisis guardados")
    parser.add_argument("--ultimo", "-u", action="store_true", help="Ver último análisis")
    args = parser.parse_args()
    
    if args.listar:
        analisis = listar_analisis()
        print(f"Encontrados: {len(analisis)} análisis\n")
        for a in analisis[:10]:
            print(f"  {a['archivo']} - {a['texto'][:50]}...")
        return
    
    if args.ultimo:
        ultimo = leer_ultimo()
        if ultimo:
            print(formatear_resultado(ultimo))
        else:
            print("No hay análisis guardados")
        return
    
    if not args.texto:
        print("Usage: python main.py <texto> [--guardar]")
        return
    
    if not validar_texto(args.texto):
        print("Error: Texto inválido (mínimo 4 caracteres)")
        sys.exit(1)
    
    print("Analizando...")
    resultados = analizar_texto(args.texto)
    print(formatear_resultado(resultados))
    
    if args.guardar:
        rutas = guardar_resultado(args.texto, resultados)
        print(f"\nGuardado en: {rutas}")


if __name__ == "__main__":
    main()