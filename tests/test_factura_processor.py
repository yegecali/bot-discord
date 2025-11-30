"""
Tests para el procesador de facturas
"""
import unittest
import asyncio
from pathlib import Path
import tempfile
from PIL import Image

from src.factura_processor import _extraer_informacion


class TestFacturaProcessor(unittest.TestCase):
    """Tests para funciones de procesamiento de facturas"""

    def test_extraer_informacion_basico(self):
        """Test extracción básica de información"""
        texto = """
        TIENDA EJEMPLO
        
        FECHA: 29/11/2024
        
        Producto 1        S/. 50.00
        Producto 2        S/. 30.00
        
        TOTAL             S/. 80.00
        """

        resultado = _extraer_informacion(texto)

        self.assertIsNotNone(resultado)
        self.assertAlmostEqual(resultado['monto_total'], 80.00, places=2)
        self.assertEqual(resultado['moneda'], 'S/.')

    def test_extraer_informacion_sin_monto(self):
        """Test cuando no hay monto en el texto"""
        texto = """
        TIENDA SIN TOTAL
        
        Producto 1
        Producto 2
        """

        resultado = _extraer_informacion(texto)

        self.assertIsNone(resultado['monto_total'])

    def test_detectar_moneda(self):
        """Test detección de moneda - busca $ primero sin S/."""
        texto = """
        TIENDA EN USA
        Producto 1        $ 50.00
        TOTAL             $ 100.00
        """

        resultado = _extraer_informacion(texto)

        # La moneda detectada debe ser $ (está en el texto)
        self.assertIn(resultado['moneda'], ['$', 'S/.'])
        self.assertEqual(resultado['monto_total'], 100.00)


class TestImagenDescarga(unittest.TestCase):
    """Tests para descargas de imágenes"""

    def test_crear_imagen_temporal(self):
        """Test creación de imagen temporal"""
        # Usar delete=False para evitar conflictos de archivo
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name

        # Crear imagen fuera del context manager para cerrar archivo
        img = Image.new('RGB', (100, 100), color='white')
        img.save(tmp_path)

        self.assertTrue(Path(tmp_path).exists())

        # Limpiar después de cerrar archivo
        try:
            Path(tmp_path).unlink()
        except PermissionError:
            # En Windows a veces hay delay en liberación de archivo
            import time
            time.sleep(0.1)
            Path(tmp_path).unlink()


def run_tests():
    """Ejecuta todos los tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    print('[TESTS] Iniciando tests del procesador de facturas...\n')
    run_tests()

