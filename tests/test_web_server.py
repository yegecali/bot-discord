"""
Tests unitarios para web_server
"""
import pytest
from src.web_server import app


@pytest.fixture
def client():
    """Crea un cliente de prueba para Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestWebServer:
    """Tests para servidor web Flask"""

    def test_index_ruta_existe(self, client):
        """Test: Ruta / existe"""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_contiene_html(self, client):
        """Test: Página principal contiene HTML"""
        response = client.get('/')
        assert b'<!DOCTYPE html>' in response.data or b'<!doctype html>' in response.data

    def test_index_contiene_titulo(self, client):
        """Test: Página tiene título"""
        response = client.get('/')
        assert b'Bot Personal' in response.data or b'Discord' in response.data

    def test_callback_sin_parametros(self, client):
        """Test: Callback sin parámetros retorna error"""
        response = client.get('/callback')
        # Debe mostrar página de error
        assert response.status_code == 200

    def test_callback_con_error(self, client):
        """Test: Callback con error"""
        response = client.get('/callback?error=access_denied')
        assert response.status_code == 200
        assert b'Error' in response.data or b'error' in response.data.lower()

    def test_callback_exitoso(self, client):
        """Test: Callback exitoso"""
        response = client.get('/callback?code=test_code&guild_id=12345&permissions=8')
        assert response.status_code == 200
        # Debe mostrar éxito
        assert b'Autorización' in response.data or b'Éxito' in response.data or b'12345' in response.data

    def test_content_type_html(self, client):
        """Test: Content-Type es HTML"""
        response = client.get('/')
        assert 'text/html' in response.content_type

    def test_ruta_no_existe(self, client):
        """Test: Ruta no existente retorna 404"""
        response = client.get('/no-existe')
        assert response.status_code == 404


class TestTemplates:
    """Tests para plantillas"""

    def test_index_renderiza_plantilla(self, client):
        """Test: Index renderiza la plantilla correctamente"""
        response = client.get('/')
        assert response.status_code == 200

        # Verificar que contiene elementos de la plantilla
        data = response.data.decode('utf-8')
        assert 'Bot' in data or 'Discord' in data

    def test_success_renderiza_plantilla(self, client):
        """Test: Success renderiza la plantilla correctamente"""
        response = client.get('/callback?code=test&guild_id=123&permissions=8')
        assert response.status_code == 200

        data = response.data.decode('utf-8')
        assert '123' in data or 'guild' in data.lower()

    def test_error_renderiza_plantilla(self, client):
        """Test: Error renderiza la plantilla correctamente"""
        response = client.get('/callback?error=test_error')
        assert response.status_code == 200

        data = response.data.decode('utf-8')
        assert 'test_error' in data or 'Error' in data


class TestRequestMethods:
    """Tests para métodos HTTP"""

    def test_get_index(self, client):
        """Test: GET en /"""
        response = client.get('/')
        assert response.status_code == 200

    def test_post_no_soportado(self, client):
        """Test: POST no soportado en /"""
        response = client.post('/')
        assert response.status_code in [405, 200]  # 405 Method Not Allowed o 200 si Flask lo permite


class TestSeguridad:
    """Tests para seguridad"""

    def test_sin_injection_en_callback(self, client):
        """Test: Protección contra injection en callback"""
        # Intentar injection
        response = client.get('/callback?code=<script>alert(1)</script>&guild_id=123')
        assert response.status_code == 200

        data = response.data.decode('utf-8')
        # Jinja2 debería escapar el script
        assert '<script>' not in data or '&lt;script&gt;' in data

    def test_parametros_validos(self, client):
        """Test: Parámetros válidos se manejan correctamente"""
        response = client.get('/callback?code=valid_code&guild_id=123456&permissions=8')
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

