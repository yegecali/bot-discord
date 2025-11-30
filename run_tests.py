"""
Script para ejecutar todos los tests del proyecto
"""
import sys
import unittest
from pathlib import Path

# Agregar el directorio padre al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_all_tests():
    """Ejecuta todos los tests del proyecto"""
    print('[TEST RUNNER] ===== EJECUTANDO TODOS LOS TESTS =====\n')

    # Descubrir y ejecutar tests
    loader = unittest.TestLoader()
    start_dir = str(project_root / 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print('\n[TEST RUNNER] ===== RESUMEN =====')
    print(f'[TEST RUNNER] Tests ejecutados: {result.testsRun}')
    print(f'[TEST RUNNER] Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}')
    print(f'[TEST RUNNER] Fallos: {len(result.failures)}')
    print(f'[TEST RUNNER] Errores: {len(result.errors)}')

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

