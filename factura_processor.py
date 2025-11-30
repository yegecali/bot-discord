import os
import aiohttp
import tempfile
import re
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import pytesseract

load_dotenv()

# ============================================================================
# CONFIGURACIÓN AGRESIVA DE TESSERACT
# ============================================================================

print("[TESSERACT DEBUG] ============ INICIO CONFIGURACIÓN ============")
print("[TESSERACT DEBUG] Iniciando búsqueda y configuración de Tesseract...")

# Rutas donde buscar Tesseract (en orden de preferencia - PRIMERO las locales válidas)
rutas_posibles = [
    r'C:\Users\Yemi Genderson\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
]

tesseract_encontrado = False
tesseract_ruta = None

# PASO 1: Buscar en rutas locales CON VERIFICACIÓN ESTRICTA
print("[TESSERACT DEBUG] PASO 1: Buscando en rutas locales...")
for ruta in rutas_posibles:
    print(f"[TESSERACT DEBUG] Comprobando: {ruta}")
    if os.path.exists(ruta):
        print(f"[TESSERACT DEBUG] ✅ ENCONTRADO en: {ruta}")
        # Verificar que se puede ejecutar
        try:
            resultado = subprocess.run([ruta, '--version'], capture_output=True, text=True, timeout=5)
            if resultado.returncode == 0:
                print(f"[TESSERACT DEBUG] ✅ Tesseract está funcionando")
                print(f"[TESSERACT DEBUG] Versión: {resultado.stdout.split(chr(10))[0]}")
                tesseract_ruta = ruta
                tesseract_encontrado = True
                print(f"[TESSERACT DEBUG] ✅ RUTA VÁLIDA ENCONTRADA - NO seguir buscando")
                break
            else:
                print(f"[TESSERACT DEBUG] ❌ Archivo existe pero no es ejecutable o no funciona")
        except Exception as e:
            print(f"[TESSERACT DEBUG] ❌ Error al verificar ejecución: {e}")
    else:
        print(f"[TESSERACT DEBUG] ❌ Ruta no existe: {ruta}")

# PASO 2: Si NO se encontró en rutas locales, verificar PATH
if not tesseract_encontrado:
    print("[TESSERACT DEBUG] PASO 2: Buscando en PATH...")
    try:
        resultado = subprocess.run(['tesseract', '--version'], capture_output=True, text=True, timeout=5)
        if resultado.returncode == 0:
            print(f"[TESSERACT DEBUG] ✅ Tesseract encontrado en PATH")
            print(f"[TESSERACT DEBUG] Versión: {resultado.stdout.split(chr(10))[0]}")
            tesseract_encontrado = True
            # Obtener ruta completa
            try:
                resultado_where = subprocess.run(['where', 'tesseract'], capture_output=True, text=True)
                if resultado_where.returncode == 0:
                    tesseract_ruta = resultado_where.stdout.strip().split('\n')[0]
                    print(f"[TESSERACT DEBUG] Ruta completa desde PATH: {tesseract_ruta}")
            except:
                pass
    except Exception as e:
        print(f"[TESSERACT DEBUG] ❌ Error buscando en PATH: {e}")

# PASO 3: Configurar pytesseract
print("[TESSERACT DEBUG] PASO 3: Configurando pytesseract...")
if tesseract_encontrado and tesseract_ruta:
    try:
        pytesseract.pytesseract.tesseract_cmd = tesseract_ruta
        print(f"[TESSERACT DEBUG] ✅ Configurado tesseract_cmd = {tesseract_ruta}")
    except Exception as e:
        print(f"[TESSERACT DEBUG] ⚠️ Error configurando: {e}")
else:
    print(f"[TESSERACT DEBUG] ⚠️ NO se configuró ruta específica")
    print(f"[TESSERACT DEBUG] pytesseract usará 'tesseract' del PATH")

print(f"[TESSERACT DEBUG] Estado actual: pytesseract.pytesseract.tesseract_cmd = {pytesseract.pytesseract.tesseract_cmd}")
print("[TESSERACT DEBUG] ============ FIN CONFIGURACIÓN ============\n")

async def descargar_imagen(url):
    """Descarga una imagen desde una URL"""
    try:
        print(f"[DESCARGA DEBUG] Iniciando descarga desde: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(f"[DESCARGA DEBUG] Respuesta HTTP: {resp.status}")
                if resp.status == 200:
                    # Guardar en archivo temporal
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                        data = await resp.read()
                        tmp.write(data)
                        print(f"[DESCARGA DEBUG] ✅ Imagen descargada: {tmp.name} ({len(data)} bytes)")
                        return tmp.name
                else:
                    print(f"[DESCARGA DEBUG] ❌ Error HTTP {resp.status}")
    except Exception as e:
        print(f'[DESCARGA DEBUG] ❌ Error descargando imagen: {e}')
        import traceback
        print(traceback.format_exc())
    return None

async def procesar_factura(ruta_imagen):
    """
    Procesa una imagen de factura usando OCR simple (Tesseract)
    Extrae: monto total, fecha, vendedor
    """
    try:
        print(f"[FACTURA DEBUG] Iniciando procesamiento de factura: {ruta_imagen}")

        # Verificar que el archivo existe
        if not os.path.exists(ruta_imagen):
            print(f"[FACTURA DEBUG] ❌ Archivo no existe: {ruta_imagen}")
            return {'error': 'Archivo de imagen no encontrado'}

        print(f"[FACTURA DEBUG] ✅ Archivo existe, tamaño: {os.path.getsize(ruta_imagen)} bytes")

        # Abrir imagen
        print(f"[FACTURA DEBUG] Abriendo imagen con PIL...")
        imagen = Image.open(ruta_imagen)
        print(f"[FACTURA DEBUG] ✅ Imagen abierta. Dimensiones: {imagen.size}, Formato: {imagen.format}")

        # Extraer texto con OCR
        print(f"[FACTURA DEBUG] Iniciando OCR con Tesseract...")
        print(f"[FACTURA DEBUG] Configuración: tesseract_cmd = {pytesseract.pytesseract.tesseract_cmd}")

        try:
            texto = pytesseract.image_to_string(imagen, lang='spa+eng')
            print(f"[FACTURA DEBUG] ✅ OCR completado exitosamente")
            print(f"[FACTURA DEBUG] Texto extraído ({len(texto)} caracteres):")
            print(f"[FACTURA DEBUG] ---\n{texto[:500]}...\n---")
        except Exception as ocr_error:
            print(f"[FACTURA DEBUG] ❌ Error en OCR: {ocr_error}")
            print(f"[FACTURA DEBUG] Tipo de error: {type(ocr_error).__name__}")
            return {'error': f'Error en OCR: {str(ocr_error)}'}

        # Buscar montos (TOTAL, Total, MONTO, etc.)
        print(f"[FACTURA DEBUG] Extrayendo información de la factura...")
        datos = extraer_informacion_factura(texto)
        print(f"[FACTURA DEBUG] ✅ Información extraída: {datos}")

        if not datos.get('monto_total'):
            print(f"[FACTURA DEBUG] ⚠️ No se encontró monto total")
            return {'error': 'No se encontró el monto total en la factura'}

        print(f"[FACTURA DEBUG] ✅ Procesamiento completado exitosamente")
        return datos

    except Exception as e:
        print(f"[FACTURA DEBUG] ❌ Error procesando factura: {e}")
        print(f"[FACTURA DEBUG] Tipo de error: {type(e).__name__}")
        import traceback
        print(f"[FACTURA DEBUG] Traceback completo:")
        print(traceback.format_exc())
        return {'error': f'Error al procesar: {str(e)}'}
    finally:
        # Limpiar archivo temporal
        print(f"[FACTURA DEBUG] Limpiando archivo temporal...")
        if os.path.exists(ruta_imagen):
            try:
                os.remove(ruta_imagen)
                print(f"[FACTURA DEBUG] ✅ Archivo temporal eliminado")
            except Exception as e:
                print(f"[FACTURA DEBUG] ⚠️ Error al eliminar archivo: {e}")

def extraer_informacion_factura(texto):
    """
    Extrae información de la factura del texto OCR
    """
    print(f"[EXTRACCION DEBUG] Iniciando extracción de información")
    print(f"[EXTRACCION DEBUG] Texto recibido ({len(texto)} caracteres)")

    lineas = texto.split('\n')
    print(f"[EXTRACCION DEBUG] Total de líneas: {len(lineas)}")

    # Buscar monto total
    monto_total = None
    moneda = 'S/.'  # Por defecto, usar soles

    # Palabras clave para identificar el total
    palabras_total = ['total', 'monto', 'a pagar', 'importe', 'debe', 'pago']
    print(f"[EXTRACCION DEBUG] Buscando palabras clave: {palabras_total}")

    for idx, linea in enumerate(lineas):
        linea_lower = linea.lower().strip()

        # Si la línea contiene palabra clave de total
        for palabra in palabras_total:
            if palabra in linea_lower:
                print(f"[EXTRACCION DEBUG] ✅ Encontrada palabra clave '{palabra}' en línea {idx}: {linea}")
                # Buscar números en la línea
                numeros = re.findall(r'[S/\.\$€£]?\s*(\d+[.,]\d{2}|\d+)', linea)
                print(f"[EXTRACCION DEBUG] Números encontrados: {numeros}")
                if numeros:
                    # Tomar el último número encontrado (generalmente es el total)
                    monto_str = numeros[-1].replace(',', '.')
                    try:
                        monto_total = float(monto_str)
                        print(f"[EXTRACCION DEBUG] ✅ Monto extraído: {monto_total}")
                        # Detectar moneda
                        if 'S/.' in linea or 's/.' in linea:
                            moneda = 'S/.'
                        elif '$' in linea:
                            moneda = '$'
                        elif '€' in linea:
                            moneda = '€'
                        elif '£' in linea:
                            moneda = '£'
                        print(f"[EXTRACCION DEBUG] Moneda detectada: {moneda}")
                        break
                    except ValueError as ve:
                        print(f"[EXTRACCION DEBUG] ❌ Error convertir monto: {ve}")
                        pass

        if monto_total:
            break

    # Si no se encontró con palabras clave, buscar el número más grande
    if not monto_total:
        print(f"[EXTRACCION DEBUG] ⚠️ No se encontró con palabras clave, buscando números...")
        todos_numeros = re.findall(r'[S/\.\$€£]?\s*(\d+[.,]\d{2}|\d+)', texto)
        print(f"[EXTRACCION DEBUG] Todos los números encontrados: {todos_numeros}")
        if todos_numeros:
            monto_str = todos_numeros[-1].replace(',', '.')
            try:
                monto_total = float(monto_str)
                print(f"[EXTRACCION DEBUG] ✅ Monto (último número): {monto_total}")
            except ValueError as ve:
                print(f"[EXTRACCION DEBUG] ❌ Error convertir último número: {ve}")
                pass

    # Buscar vendedor/comercio (primeras líneas)
    vendedor = 'Comercio'
    print(f"[EXTRACCION DEBUG] Buscando vendedor en primeras 10 líneas...")
    for linea in lineas[:10]:
        if linea.strip() and len(linea.strip()) > 3 and not any(char.isdigit() for char in linea[:5]):
            vendedor = linea.strip()
            print(f"[EXTRACCION DEBUG] ✅ Vendedor encontrado: {vendedor}")
            break

    # Buscar fecha
    fecha = None
    patron_fecha = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
    coincidencia = re.search(patron_fecha, texto)
    if coincidencia:
        fecha = coincidencia.group(1)
        print(f"[EXTRACCION DEBUG] ✅ Fecha encontrada: {fecha}")
    else:
        print(f"[EXTRACCION DEBUG] ⚠️ Fecha no encontrada")

    resultado = {
        'monto_total': monto_total,
        'moneda': moneda,
        'vendedor': vendedor,
        'fecha': fecha,
        'categoría': 'Otros',
        'descripción': f'Compra en {vendedor}'
    }
    print(f"[EXTRACCION DEBUG] ✅ Resultado final: {resultado}")
    return resultado

def extraer_informacion_manual(text):
    """
    Extrae información de texto manual si la IA falla
    """
    # Buscar números (monto)
    numeros = re.findall(r'\$?\d+[.,]\d{2}', text)
    monto = float(numeros[0].replace('$', '').replace(',', '.')) if numeros else None

    return {
        'monto_total': monto,
        'descripción': 'Gasto registrado manualmente',
        'categoría': 'Otros'
    }

