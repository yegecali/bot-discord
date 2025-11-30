"""
Tests para la base de datos
"""
import unittest
import sqlite3
from pathlib import Path
import tempfile
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import (
    registrar_gasto, obtener_gastos_usuario, obtener_total_gastos,
    obtener_gastos_por_categoria, eliminar_gasto
)


class TestDatabase(unittest.TestCase):
    """Tests para funciones de base de datos"""

    def setUp(self):
        """Preparación antes de cada test"""
        self.usuario_id = 123456789

    def test_registrar_gasto(self):
        """Test registro de gasto"""
        gasto_id = registrar_gasto(
            usuario_id=self.usuario_id,
            descripcion='Test gasto',
            monto=50.00,
            categoria='Pruebas'
        )

        self.assertIsNotNone(gasto_id)
        self.assertGreater(gasto_id, 0)

    def test_obtener_gastos_usuario(self):
        """Test obtención de gastos del usuario"""
        # Registrar gastos
        registrar_gasto(self.usuario_id, 'Gasto 1', 100.00, 'Pruebas')
        registrar_gasto(self.usuario_id, 'Gasto 2', 50.00, 'Pruebas')

        gastos = obtener_gastos_usuario(self.usuario_id)

        self.assertGreater(len(gastos), 0)

    def test_obtener_total_gastos(self):
        """Test cálculo del total de gastos"""
        # Registrar gastos
        registrar_gasto(self.usuario_id, 'Gasto 1', 100.00, 'Pruebas')
        registrar_gasto(self.usuario_id, 'Gasto 2', 50.00, 'Pruebas')

        total = obtener_total_gastos(self.usuario_id, dias=365)

        self.assertGreater(total, 0)

    def test_obtener_gastos_por_categoria(self):
        """Test agrupación por categoría"""
        registrar_gasto(self.usuario_id, 'Comida', 50.00, 'Alimentación')
        registrar_gasto(self.usuario_id, 'Taxi', 30.00, 'Transporte')

        categorias = obtener_gastos_por_categoria(self.usuario_id, dias=365)

        self.assertGreater(len(categorias), 0)

    def test_eliminar_gasto(self):
        """Test eliminación de gasto"""
        gasto_id = registrar_gasto(self.usuario_id, 'Gasto a eliminar', 100.00)

        resultado = eliminar_gasto(gasto_id, self.usuario_id)

        self.assertTrue(resultado)


if __name__ == '__main__':
    print('[TESTS] Iniciando tests de base de datos...\n')
    unittest.main(argv=[''], exit=False, verbosity=2)

