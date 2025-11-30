import requests
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:8080/callback')

def exchange_code_for_token(code):
    """Intercambia el código de autorización por un token de acceso"""
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'bot'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    return response.json()

def get_bot_invite_url(permissions=8):
    """Genera la URL de invitación del bot"""
    return f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions={permissions}&scope=bot'

def get_oauth_url(permissions=8):
    """Genera la URL de OAuth2 para autorización"""
    return f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=bot&permissions={permissions}'

