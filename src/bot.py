"""
Bot de Discord para gestión de gastos
Procesa imágenes de facturas y registra gastos

PUNTO DE ENTRADA PRINCIPAL DEL BOT
"""
import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.config import DISCORD_TOKEN, COMMAND_PREFIX
from src.models import init_db
from src.config.db_persistence import (
    verify_db_exists,
    ensure_db_persistence,
    check_db_permissions
)
from src.controller import registrar_comandos_en_controller, registrar_eventos_en_controller

# Cargar variables de entorno
load_dotenv()

# ============================================================
# INICIALIZAR BD CON PERSISTENCIA
# ============================================================
print("\n[BOT] Inicializando BD con persistencia...")

# Verificar permisos
if not check_db_permissions():
    print("[BOT] ❌ Error de permisos en BD")
    exit(1)

# Verificar que BD existe
verify_db_exists()

# Crear tabla si no existen
init_db()

# Habilitar WAL mode y persistencia
ensure_db_persistence()

print("[BOT] ✅ BD lista para persistencia\n")

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Crear instancia del bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# ============================================================
# REGISTRAR COMANDOS Y EVENTOS
# ============================================================

# Registrar todos los comandos desde el controller
registrar_comandos_en_controller(bot)

# Registrar todos los eventos desde el controller
registrar_eventos_en_controller(bot)


def run_bot():
    """Inicia el bot"""
    if not DISCORD_TOKEN:
        raise ValueError('DISCORD_TOKEN no está configurado en .env')

    print('[BOT] Iniciando Bot Personal de Discord...')
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    run_bot()

