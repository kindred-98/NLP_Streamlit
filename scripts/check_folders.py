import os
import sys

REQUIRED_DIRS = [
    "src",
    "almacenamiento",
    "interface",
    "tests",
    "resultados"
]

REQUIRED_FILES = [
    "main.py",
    "requirements.txt"
]

def check_folders():
    """Verifica la estructura de carpetas del proyecto."""
    errors = []
    
    for d in REQUIRED_DIRS:
        if not os.path.isdir(d):
            errors.append(f"Falta la carpeta: {d}")
    
    for f in REQUIRED_FILES:
        if not os.path.isfile(f):
            errors.append(f"Falta el archivo: {f}")
    
    if errors:
        print("ERROR: Errores encontrados:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    
    print("OK: Estructura correcta")
    sys.exit(0)


if __name__ == "__main__":
    check_folders()