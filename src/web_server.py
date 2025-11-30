"""
Servidor web Flask para OAuth2 de Discord
Maneja el callback de autorización del bot
"""
from flask import Flask, request, render_template
from pathlib import Path
from src.oauth_handler import get_oauth_url
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar Flask con carpeta de templates
TEMPLATE_DIR = Path(__file__).parent / 'templates'
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

@app.route('/')
def index():
    """Página principal con instrucciones"""
    url_oauth = get_oauth_url()
    print(f"[WEB] 📄 Renderizando página principal")
    return render_template('index.html', oauth_url=url_oauth)

@app.route('/callback')
def callback():
    """Callback de OAuth2 después de autorización"""
    code = request.args.get('code')
    guild_id = request.args.get('guild_id')
    permissions = request.args.get('permissions')
    error = request.args.get('error')

    print(f"[WEB] 📍 Callback recibido")

    if error:
        print(f"[WEB] ❌ Error en callback: {error}")
        return render_template('error.html', error=error)

    if code and guild_id:
        print(f"[WEB] ✅ Autorización exitosa")
        print(f"[WEB] Guild ID: {guild_id}")
        print(f"[WEB] Permisos: {permissions}")
        return render_template('success.html', guild_id=guild_id, permissions=permissions)

    print(f"[WEB] ⚠️ Parámetros faltantes en callback")
    return render_template('error.html', error='Parámetros faltantes')

def run_server(host='localhost', port=8080):
    """
    Inicia el servidor Flask

    Args:
        host (str): Host del servidor
        port (int): Puerto del servidor
    """
    print(f"[WEB] Iniciando servidor en http://{host}:{port}")
    app.run(host=host, port=port, debug=False)

