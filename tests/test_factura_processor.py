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
        """Test detección de moneda"""
        texto = """
        COMPRA EN TIENDA
        TOTAL USD 100.00
        """

        resultado = _extraer_informacion(texto)

        self.assertEqual(resultado['moneda'], '$')


class TestImagenDescarga(unittest.TestCase):
    """Tests para descargas de imágenes"""

    def test_crear_imagen_temporal(self):
        """Test creación de imagen temporal"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            # Crear imagen simple
            img = Image.new('RGB', (100, 100), color='white')
            img.save(tmp.name)

            self.assertTrue(Path(tmp.name).exists())

            # Limpiar
            Path(tmp.name).unlink()


def run_tests():
    """Ejecuta todos los tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    print('[TESTS] Iniciando tests del procesador de facturas...\n')
    run_tests()

