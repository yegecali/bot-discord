"""
Configuración automática de Tesseract OCR
"""
import os
import json
import subprocess
from pathlib import Path

print("[CONFIG] ============ CONFIGURANDO TESSERACT ============")

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
    except Exception as e:
        print(f"[CONFIG] [WARN] Error cargando {ruta_config}: {e}")
        print(f"[CONFIG] Usando rutas por defecto")
        return [
            r'C:\Users\Yemi Genderson\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        ]


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
                print(f"[CONFIG] [OK] Tesseract encontrado en: {ruta}")
                print(f"[CONFIG] Versi{chr(243)}n: {version}")
                break
        except Exception as e:
            print(f"[CONFIG] [WARN] Error verificando {ruta}: {e}")

# Si no se encontró en rutas locales, buscar en PATH
if not TESSERACT_ENCONTRADO:
    try:
        resultado = subprocess.run(['tesseract', '--version'], capture_output=True, text=True, timeout=5)
        if resultado.returncode == 0:
            TESSERACT_ENCONTRADO = True
            version = resultado.stdout.split('\n')[0]
            print(f"[CONFIG] [OK] Tesseract encontrado en PATH")
            print(f"[CONFIG] Versi{chr(243)}n: {version}")
            # Obtener ruta completa
            try:
                resultado_where = subprocess.run(['where', 'tesseract'], capture_output=True, text=True)
                if resultado_where.returncode == 0:
                    TESSERACT_CMD = resultado_where.stdout.strip().split('\n')[0]
            except:
                pass
    except Exception as e:
        print(f"[CONFIG] [WARN] Error buscando Tesseract en PATH: {e}")

if TESSERACT_ENCONTRADO:
    print(f"[CONFIG] [OK] Tesseract configurado correctamente")
else:
    print(f"[CONFIG] [ERROR] ADVERTENCIA: Tesseract no encontrado")
    print(f"[CONFIG] Descargalo desde: https://github.com/UB-Mannheim/tesseract/wiki")

print("[CONFIG] ============ CONFIGURACION COMPLETADA ============\n")

