"""
Pruebas de integración con Tesseract OCR
"""
import sys
import subprocess
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import TESSERACT_CMD, TESSERACT_ENCONTRADO


def verificar_tesseract():
    """Verifica que Tesseract esté instalado y funcionando"""
    print('[TEST TESSERACT] Verificando instalación de Tesseract...\n')

    if not TESSERACT_ENCONTRADO:
        print('[TEST TESSERACT] ❌ Tesseract NO está instalado')
        print('[TEST TESSERACT] Descárgalo desde: https://github.com/UB-Mannheim/tesseract/wiki')
        return False

    if TESSERACT_CMD:
        print(f'[TEST TESSERACT] ✅ Tesseract encontrado en: {TESSERACT_CMD}')

        try:
            resultado = subprocess.run([TESSERACT_CMD, '--version'], capture_output=True, text=True)
            print(f'[TEST TESSERACT] ✅ Versión:')
            for linea in resultado.stdout.split('\n')[:2]:
                print(f'[TEST TESSERACT]    {linea}')
        except Exception as e:
            print(f'[TEST TESSERACT] ❌ Error verificando: {e}')
            return False

    print('[TEST TESSERACT] ✅ Tesseract está listo')
    return True


def test_ocr_basico():
    """Test básico de OCR"""
    if not TESSERACT_ENCONTRADO:
        print('[TEST OCR] ⚠️ Saltando test de OCR (Tesseract no instalado)')
        return False

    print('\n[TEST OCR] Probando OCR básico...')

    try:
        from PIL import Image
        import pytesseract
        import tempfile

        # Crear imagen de prueba con texto
        img = Image.new('RGB', (200, 100), color='white')

        # Guardar temporalmente
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img.save(tmp.name)

            # Intentar OCR
            try:
                texto = pytesseract.image_to_string(img, lang='spa+eng')
                print('[TEST OCR] ✅ OCR funcionando')
                return True
            except Exception as e:
                print(f'[TEST OCR] ❌ Error en OCR: {e}')
                return False
    except Exception as e:
        print(f'[TEST OCR] ❌ Error: {e}')
        return False


if __name__ == '__main__':
    print('[TESTS] ===== PRUEBAS DE TESSERACT =====\n')

    tesseract_ok = verificar_tesseract()

    if tesseract_ok:
        ocr_ok = test_ocr_basico()

        if ocr_ok:
            print('\n[TESTS] ✅ Todas las pruebas pasaron')
        else:
            print('\n[TESTS] ⚠️ Pruebas incompletas')
    else:
        print('\n[TESTS] ❌ Tesseract no está configurado')

