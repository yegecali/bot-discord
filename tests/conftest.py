"""
Configuración compartida para todos los tests (conftest.py)
"""
import pytest
import os
from pathlib import Path

# Agregar el directorio raíz al path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def test_config():
    """Configuración para todos los tests"""
    return {
        'db_test': ':memory:',  # Base de datos en memoria para tests
        'timeout': 5
    }


@pytest.fixture(autouse=True)
def clean_env():
    """Limpia variables de entorno antes de cada test"""
    yield


def pytest_configure(config):
    """Configuración inicial de pytest"""
    print("\n" + "="*60)
    print("INICIANDO TESTS DEL BOT PERSONAL DE DISCORD")
    print("="*60)


def pytest_unconfigure(config):
    """Configuración final de pytest"""
    print("\n" + "="*60)
    print("TESTS COMPLETADOS")
    print("="*60)

