"""
Servidor web Flask para OAuth2 de Discord
Maneja el callback de autorización del bot
"""
from flask import Flask, request, render_template
from pathlib import Path
from src.oauth_handler import get_oauth_url
from src.config import ExceptionHandler
from src.utils import get_logger
import os
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)

# Configurar Flask con carpeta de templates
TEMPLATE_DIR = Path(__file__).parent / 'templates'
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

# Manejador global de errores Flask
@app.errorhandler(Exception)
def manejar_error_global(error):
    """Maneja todos los errores en Flask"""
    logger.error(f"Error HTTP no manejado: {error}", exc_info=True)

    # Usar ExceptionHandler para crear respuesta
    resultado = ExceptionHandler.manejar_error(
        excepcion=error,
        contexto="Error en servidor web",
        datos_adicionales={
            'URL': request.url,
            'Método': request.method,
            'IP': request.remote_addr,
        }
    )

    # Retornar plantilla Markdown de error
    markdown_error = ExceptionHandler.crear_plantilla_error_markdown(
        excepcion=error,
        contexto="Error en servidor web",
        datos_adicionales={
            'URL': request.url,
            'Método': request.method,
            'IP': request.remote_addr,
        }
    )

    return f"<pre>{markdown_error}</pre>", 500

@app.route('/')
def index():
    """Página principal con instrucciones"""
    try:
        url_oauth = get_oauth_url()
        logger.info("📄 Renderizando página principal")
        return render_template('index.html', oauth_url=url_oauth)
    except Exception as e:
        markdown_error = ExceptionHandler.crear_plantilla_error_markdown(
            e,
            contexto="Cargando página principal"
        )
        return f"<pre>{markdown_error}</pre>", 500

@app.route('/callback')
def callback():
    """Callback de OAuth2 después de autorización"""
    try:
        code = request.args.get('code')
        guild_id = request.args.get('guild_id')
        permissions = request.args.get('permissions')
        error = request.args.get('error')

        logger.info("📍 Callback recibido")

        if error:
            logger.error(f"❌ Error en callback: {error}")
            return render_template('error.html', error=error)

        if code and guild_id:
            logger.info(f"✅ Autorización exitosa - Guild ID: {guild_id}, Permisos: {permissions}")
            return render_template('success.html', guild_id=guild_id, permissions=permissions)

        logger.warning("⚠️ Parámetros faltantes en callback")
        return render_template('error.html', error='Parámetros faltantes')

    except Exception as e:
        markdown_error = ExceptionHandler.crear_plantilla_error_markdown(
            e,
            contexto="Procesamiento de callback OAuth2"
        )
        return f"<pre>{markdown_error}</pre>", 500

def run_server(host='localhost', port=8080):
    """
    Inicia el servidor Flask

    Args:
        host (str): Host del servidor
        port (int): Puerto del servidor
    """
    try:
        logger.info(f"🚀 Iniciando servidor en http://{host}:{port}")
        app.run(host=host, port=port, debug=False)
    except Exception as e:
        ExceptionHandler.manejar_error(e, contexto="Iniciando servidor Flask")

