"""
Punto de entrada principal del Bot Personal de Discord
Inicia el servidor web OAuth2 y el bot en paralelo
"""
import asyncio
import threading
import sys
from src.web_server import run_server
from src.bot import bot, run_bot
from src.config import WEB_HOST, WEB_PORT, LoggerConfig
from src.utils import get_logger

# Inicializar logging centralizado
LoggerConfig.initialize(level='INFO', enable_file=True, enable_console=True)
logger = get_logger(__name__)

def run_web_server():
    """Ejecuta el servidor web en un thread separado"""
    try:
        logger.info(f'🚀 Iniciando servidor web en http://{WEB_HOST}:{WEB_PORT}')
        run_server(host=WEB_HOST, port=WEB_PORT)
    except Exception as e:
        logger.error(f'❌ Error en servidor web: {e}')
        sys.exit(1)

def main():
    """Función principal"""
    logger.info('=' * 50)
    logger.info('🤖 BOT PERSONAL DE DISCORD')
    logger.info('=' * 50)
    logger.info('🔧 Iniciando servicios...\n')

    # Iniciar servidor web en thread separado
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    # Pequeña pausa para que el servidor web inicie
    import time
    time.sleep(1)

    # Iniciar bot de Discord
    print('[MAIN] Iniciando bot de Discord...\n')
    try:
        run_bot()
    except KeyboardInterrupt:
        print('\n[MAIN] Bot detenido por el usuario')
    except Exception as e:
        print(f'\n[MAIN] ❌ Error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()

