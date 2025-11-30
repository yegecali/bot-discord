"""
Script de inicio del proyecto
Ejecuta todos los pasos necesarios para iniciar el bot
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Imprime encabezado"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python():
    """Verifica versión de Python"""
    print_header("1️⃣ Verificando Python")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")
        return True
    print(f"❌ Se requiere Python 3.8+, tienes {version.major}.{version.minor}")
    return False

def check_venv():
    """Verifica entorno virtual"""
    print_header("2️⃣ Verificando Entorno Virtual")
    venv_path = Path(".venv")
    if venv_path.exists():
        print("✅ Entorno virtual existe")
        return True
    print("⚠️ Entorno virtual no existe")
    print("📝 Crear con: python -m venv .venv")
    return False

def check_env_file():
    """Verifica archivo .env"""
    print_header("3️⃣ Verificando .env")
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path) as f:
            content = f.read()
            if "DISCORD_TOKEN" in content:
                print("✅ Archivo .env existe")
                return True
    print("❌ Archivo .env no encontrado o incompleto")
    print("📝 Crear .env con:")
    print("   DISCORD_TOKEN=tu_token")
    print("   CLIENT_ID=tu_id")
    print("   CLIENT_SECRET=tu_secret")
    return False

def check_dependencies():
    """Verifica dependencias"""
    print_header("4️⃣ Verificando Dependencias")
    try:
        import discord
        import sqlalchemy
        import flask
        print("✅ Discord.py OK")
        print("✅ SQLAlchemy OK")
        print("✅ Flask OK")
        return True
    except ImportError as e:
        print(f"❌ Falta: {e}")
        print("📝 Instalar con: pip install -r requirements.txt")
        return False

def check_tesseract():
    """Verifica Tesseract"""
    print_header("5️⃣ Verificando Tesseract")
    try:
        result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract encontrado")
            return True
    except:
        pass
    print("⚠️ Tesseract no encontrado en PATH")
    print("📝 Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki")
    return False

def check_database():
    """Verifica base de datos"""
    print_header("6️⃣ Inicializando Base de Datos")
    try:
        from src.models import init_db
        init_db()
        print("✅ Base de datos inicializada")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def start_bot():
    """Inicia el bot"""
    print_header("7️⃣ Iniciando Bot")
    print("🚀 Ejecutando: python src/bot.py\n")
    try:
        import src.bot
        src.bot.run_bot()
    except KeyboardInterrupt:
        print("\n\n✅ Bot detenido correctamente")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("  🤖 BOT PERSONAL DE DISCORD - INICIO")
    print("="*60)

    checks = [
        ("Python", check_python),
        ("Entorno Virtual", check_venv),
        ("Archivo .env", check_env_file),
        ("Dependencias", check_dependencies),
        ("Tesseract", check_tesseract),
        ("Base de Datos", check_database),
    ]

    results = []
    for name, check in checks:
        try:
            result = check()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            results.append((name, False))

    print_header("📊 RESUMEN")
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    critical_ok = all([
        results[0][1],  # Python
        results[1][1],  # Venv
        results[2][1],  # .env
        results[3][1],  # Dependencies
    ])

    if not critical_ok:
        print("\n❌ Faltan requisitos críticos")
        print("📝 Consulta COMO_INICIAR.md para más información")
        sys.exit(1)

    print("\n✅ Todos los requisitos críticos cumplidos")
    print("🚀 Iniciando bot...\n")

    start_bot()

if __name__ == "__main__":
    main()

