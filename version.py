"""
Script para gestionar la versión de la aplicación
"""
from pathlib import Path


def get_version():
    """Lee la versión desde el archivo VERSION"""
    version_file = Path(__file__).parent / 'VERSION'
    if version_file.exists():
        return version_file.read_text().strip()
    return '0.0.0'


def set_version(new_version):
    """Establece una nueva versión en el archivo VERSION"""
    version_file = Path(__file__).parent / 'VERSION'
    version_file.write_text(f"{new_version}\n")
    print(f"[VERSION] Versión actualizada a: {new_version}")


def increment_version(part='patch'):
    """
    Incrementa la versión

    Args:
        part: 'major', 'minor' o 'patch'
    """
    current = get_version()
    parts = current.split('.')

    if len(parts) != 3:
        print(f"[VERSION] Error: versión inválida: {current}")
        return

    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    elif part == 'patch':
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    set_version(new_version)
    return new_version


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'get':
            print(get_version())
        elif command == 'set':
            if len(sys.argv) > 2:
                set_version(sys.argv[2])
            else:
                print("Uso: python version.py set <version>")
        elif command in ['major', 'minor', 'patch']:
            increment_version(command)
        else:
            print(f"Comando desconocido: {command}")
    else:
        print(f"Versión actual: {get_version()}")
        print("\nUso:")
        print("  python version.py get          - Obtener versión actual")
        print("  python version.py set <v>      - Establecer versión")
        print("  python version.py major        - Incrementar versión mayor")
        print("  python version.py minor        - Incrementar versión menor")
        print("  python version.py patch        - Incrementar versión patch")

