"""
Configuración automática de Tesseract OCR
"""
import os
import json
import subprocess
from pathlib import Path
from src.logger import get_logger
from src.config.exception_handler import ExceptionHandler

logger = get_logger(__name__)

logger.info("🔧 ============ CONFIGURANDO TESSERACT ============")

# ============================================================
# TESSERACT OCR - Configuración automática
# ============================================================

# Cargar rutas de Tesseract desde archivo JSON
def _cargar_rutas_tesseract():
    """Carga las rutas de Tesseract desde el archivo de configuración JSON"""
    ruta_config = Path(__file__).parent.parent / 'tesseract_paths.json'
    try:
        with open(ruta_config, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('tesseract', {}).get('rutas', [])
    except FileNotFoundError as e:
        ExceptionHandler.manejar_error(
            excepcion=e,
            contexto="Cargando rutas de Tesseract",
            datos_adicionales={'Archivo': str(ruta_config)}
        )
        logger.info(f"Usando rutas por defecto")
        return [
            r'C:\Users\Yemi Genderson\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        ]
    except json.JSONDecodeError as e:
        ExceptionHandler.manejar_error(
            excepcion=e,
            contexto="Parseando JSON de Tesseract",
            datos_adicionales={'Archivo': str(ruta_config)}
        )
        return []
    except Exception as e:
        ExceptionHandler.manejar_error(
            excepcion=e,
            contexto="Configurando rutas de Tesseract",
            datos_adicionales={'Archivo': str(ruta_config)}
        )
        return []


TESSERACT_RUTAS = _cargar_rutas_tesseract()

TESSERACT_CMD = None
TESSERACT_ENCONTRADO = False

# Buscar Tesseract en rutas locales
for ruta in TESSERACT_RUTAS:
    if os.path.exists(ruta):
        try:
            resultado = subprocess.run([ruta, '--version'], capture_output=True, text=True, timeout=5)
            if resultado.returncode == 0:
                TESSERACT_CMD = ruta
                TESSERACT_ENCONTRADO = True
                version = resultado.stdout.split('\n')[0]
                logger.info(f"✅ Tesseract encontrado en: {ruta}")
                logger.info(f"Versión: {version}")
                break
        except Exception as e:
            logger.warning(f"⚠️ Error verificando {ruta}: {e}")

# Si no se encontró en rutas locales, buscar en PATH
if not TESSERACT_ENCONTRADO:
    try:
        resultado = subprocess.run(['tesseract', '--version'], capture_output=True, text=True, timeout=5)
        if resultado.returncode == 0:
            TESSERACT_ENCONTRADO = True
            version = resultado.stdout.split('\n')[0]
            logger.info(f"✅ Tesseract encontrado en PATH")
            logger.info(f"Versión: {version}")
            # Obtener ruta completa
            try:
                resultado_where = subprocess.run(['where', 'tesseract'], capture_output=True, text=True)
                if resultado_where.returncode == 0:
                    TESSERACT_CMD = resultado_where.stdout.strip().split('\n')[0]
            except:
                pass
    except Exception as e:
        logger.warning(f"⚠️ Error buscando Tesseract en PATH: {e}")

if TESSERACT_ENCONTRADO:
    logger.info(f"✅ Tesseract configurado correctamente")
else:
    logger.error(f"❌ ADVERTENCIA: Tesseract no encontrado")
    logger.error(f"Descargalo desde: https://github.com/UB-Mannheim/tesseract/wiki")

logger.info("🔧 ============ CONFIGURACION COMPLETADA ============\n")

