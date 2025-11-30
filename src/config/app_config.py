"""
Configuración de aplicación (Discord, Web, etc)
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ============================================================
# DISCORD
# ============================================================
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '!'

# ============================================================
# WEB SERVER
# ============================================================
WEB_HOST = 'localhost'
WEB_PORT = 8080

# ============================================================
# MONEDA
# ============================================================
MONEDA_DEFECTO = "PEN"  # Soles peruanos
SIMBOLO_MONEDA = "S/."

# ============================================================
# IDIOMA OCR
# ============================================================
OCR_IDIOMAS = 'spa+eng'  # Español + Inglés

