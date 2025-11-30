import asyncio
import threading
from web_server import run_server
from bot import bot
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

def run_web_server():
    """Ejecuta el servidor web en un thread separado"""
    run_server()

if __name__ == '__main__':
    # Iniciar servidor web en un thread
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    # Iniciar el bot de Discord
    print('[Main] Iniciando Bot Personal de Discord...')
    print('[Main] Web server disponible en http://localhost:8080')
    bot.run(DISCORD_TOKEN)

