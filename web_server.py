from flask import Flask, request, redirect, render_template_string
import oauth_handler
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# HTML para mostrar en los endpoints
SUCCESS_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Discord - Autorización Exitosa</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
        }
        p {
            color: #666;
            font-size: 16px;
            margin: 10px 0;
        }
        .info {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: left;
        }
        .info-item {
            margin: 10px 0;
            font-family: monospace;
        }
        .label {
            font-weight: bold;
            color: #333;
        }
        .value {
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ ¡Autorización Exitosa!</h1>
        <p>El bot ha sido autorizado correctamente en tu servidor.</p>
        <div class="info">
            <div class="info-item">
                <span class="label">Servidor ID:</span> <span class="value">{{ guild_id }}</span>
            </div>
            <div class="info-item">
                <span class="label">Permisos:</span> <span class="value">{{ permissions }}</span>
            </div>
            <div class="info-item">
                <span class="label">Código:</span> <span class="value">{{ code }}</span>
            </div>
        </div>
        <p>El bot ya está disponible en tu servidor y listo para usar.</p>
        <p style="color: #999; font-size: 14px; margin-top: 30px;">Puedes cerrar esta ventana o volver a Discord.</p>
    </div>
</body>
</html>
"""

ERROR_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Discord - Error</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #e74c3c;
            margin-bottom: 10px;
        }
        p {
            color: #666;
            font-size: 16px;
            margin: 10px 0;
        }
        .error-details {
            background: #ffe0e0;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #e74c3c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>❌ Error en la Autorización</h1>
        <p>Ocurrió un error al autorizar el bot.</p>
        <div class="error-details">
            <p><strong>Error:</strong> {{ error }}</p>
        </div>
        <p>Por favor, intenta de nuevo o contacta al administrador.</p>
    </div>
</body>
</html>
"""

HOME_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Personal de Discord</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
        }
        p {
            color: #666;
            font-size: 16px;
            margin: 15px 0;
        }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .commands {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: left;
        }
        .command {
            margin: 10px 0;
            font-family: monospace;
        }
        .cmd {
            color: #667eea;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Bot Personal de Discord</h1>
        <p>Bienvenido al bot personal. Haz clic en el botón de abajo para autorizar el bot en tu servidor de Discord.</p>
        
        <a href="{{ oauth_url }}" class="btn btn-primary">Autorizar Bot en Discord</a>
        
        <div class="commands">
            <h3 style="margin-top: 0;">Comandos disponibles:</h3>
            <div class="command"><span class="cmd">!ping</span> - Muestra la latencia</div>
            <div class="command"><span class="cmd">!hola</span> - Te saluda</div>
            <div class="command"><span class="cmd">!info</span> - Tu información</div>
            <div class="command"><span class="cmd">!canales</span> - Lista de canales</div>
            <div class="command"><span class="cmd">!ayuda</span> - Muestra todos los comandos</div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Página principal"""
    oauth_url = oauth_handler.get_oauth_url()
    return render_template_string(HOME_HTML, oauth_url=oauth_url)

@app.route('/callback')
def callback():
    """Maneja el callback de OAuth2 de Discord"""
    code = request.args.get('code')
    guild_id = request.args.get('guild_id')
    permissions = request.args.get('permissions')
    error = request.args.get('error')

    # Si hay un error
    if error:
        return render_template_string(ERROR_HTML, error=error), 400

    # Si no hay código
    if not code:
        return render_template_string(ERROR_HTML, error='No se recibió código de autorización'), 400

    # Intentar intercambiar el código por un token
    try:
        token_response = oauth_handler.exchange_code_for_token(code)

        if 'error' in token_response:
            return render_template_string(ERROR_HTML, error=token_response.get('error_description', 'Error desconocido')), 400

        # Éxito
        print(f'[OAuth] Bot autorizado en servidor {guild_id}')
        print(f'[OAuth] Token: {token_response.get("access_token", "N/A")[:20]}...')

        return render_template_string(
            SUCCESS_HTML,
            guild_id=guild_id or 'N/A',
            permissions=permissions or 'N/A',
            code=code[:20] + '...' if code else 'N/A'
        )

    except Exception as e:
        print(f'[OAuth Error] {str(e)}')
        return render_template_string(ERROR_HTML, error=f'Error del servidor: {str(e)}'), 500

@app.route('/invite')
def invite():
    """Redirige a la URL de invitación del bot"""
    return redirect(oauth_handler.get_bot_invite_url())

def run_server(host='127.0.0.1', port=8080):
    """Inicia el servidor Flask"""
    print(f'[Web Server] Iniciando servidor en http://{host}:{port}')
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    run_server()

