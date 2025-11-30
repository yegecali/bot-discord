"""
Procesador de facturas con OCR usando Tesseract
Extrae información de facturas: monto, fecha, vendedor, categoría
"""
import os
import aiohttp
import tempfile
import re
from pathlib import Path
from PIL import Image
import pytesseract

from src.config import TESSERACT_CMD, OCR_IDIOMAS, SIMBOLO_MONEDA

# Configurar Tesseract si fue encontrado
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

async def descargar_imagen(url):
    """
    Descarga una imagen desde una URL

    Args:
        url (str): URL de la imagen

    Returns:
        str: Ruta del archivo temporal descargado, o None si falla
    """
    try:
        print(f"[FACTURA] Descargando imagen desde: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                        data = await resp.read()
                        tmp.write(data)
                        print(f"[FACTURA] ✅ Imagen descargada: {len(data)} bytes")
                        return tmp.name
                else:
                    print(f"[FACTURA] ❌ Error HTTP {resp.status}")
    except Exception as e:
        print(f'[FACTURA] ❌ Error descargando: {e}')
    return None

async def procesar_factura(ruta_imagen):
    """
    Procesa una imagen de factura usando OCR

    Args:
        ruta_imagen (str): Ruta de la imagen a procesar

    Returns:
        dict: Información extraída de la factura
    """
    try:
        print(f"\n[FACTURA] ===== INICIANDO PROCESAMIENTO =====")
        print(f"[FACTURA] Archivo: {ruta_imagen}")

        # Verificar que el archivo existe
        if not os.path.exists(ruta_imagen):
            print(f"[FACTURA] ❌ Archivo no existe")
            return {'error': 'Archivo de imagen no encontrado'}

        print(f"[FACTURA] ✅ Archivo existe ({os.path.getsize(ruta_imagen)} bytes)")

        # Abrir imagen con PIL
        print(f"[FACTURA] Abriendo imagen...")
        imagen = Image.open(ruta_imagen)
        print(f"[FACTURA] ✅ Imagen abierta: {imagen.size} - {imagen.format}")

        # Extraer texto con OCR
        print(f"[FACTURA] Iniciando OCR con Tesseract...")
        print(f"[FACTURA] Idiomas: {OCR_IDIOMAS}")

        try:
            texto = pytesseract.image_to_string(imagen, lang=OCR_IDIOMAS)
            print(f"[FACTURA] ✅ OCR completado ({len(texto)} caracteres)")

            # Mostrar primeras líneas del texto
            lineas_muestra = texto.split('\n')[:5]
            for linea in lineas_muestra:
                if linea.strip():
                    print(f"[FACTURA] > {linea[:80]}")
        except Exception as ocr_error:
            print(f"[FACTURA] ❌ Error OCR: {type(ocr_error).__name__}: {str(ocr_error)}")
            return {'error': f'Error en OCR: {str(ocr_error)}'}

        # Extraer información de la factura
        print(f"[FACTURA] Extrayendo información...")
        datos = _extraer_informacion(texto)
        print(f"[FACTURA] ✅ Información extraída")

        if not datos.get('monto_total'):
            print(f"[FACTURA] ❌ No se encontró monto total")
            return {'error': 'No se encontró el monto total en la factura'}

        print(f"[FACTURA] ✅ Procesamiento exitoso")
        print(f"[FACTURA] ===== PROCESAMIENTO COMPLETADO =====\n")
        return datos

    except Exception as e:
        print(f"[FACTURA] ❌ Error: {type(e).__name__}: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {'error': f'Error: {str(e)}'}
    finally:
        # Limpiar archivo temporal
        try:
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
                print(f"[FACTURA] ✅ Archivo temporal limpiado")
        except Exception as e:
            print(f"[FACTURA] ⚠️ Error limpiando: {e}")

def _extraer_informacion(texto):
    """
    Extrae información de la factura del texto OCR

    Args:
        texto (str): Texto extraído por OCR

    Returns:
        dict: Información de la factura
    """
    print(f"[EXTRACCION] Analizando {len(texto)} caracteres")

    lineas = [l.strip() for l in texto.split('\n')]
    print(f"[EXTRACCION] Total de líneas: {len(lineas)}")

    # Buscar monto total
    monto_total = None
    moneda = SIMBOLO_MONEDA

    # Palabras clave para el total
    palabras_total = ['total', 'monto', 'a pagar', 'importe', 'debe', 'pago', 'subtotal']

    print(f"[EXTRACCION] Buscando palabras clave...")
    for idx, linea in enumerate(lineas):
        linea_lower = linea.lower()

        for palabra in palabras_total:
            if palabra in linea_lower and not monto_total:
                print(f"[EXTRACCION] > Línea {idx}: '{palabra}' - {linea[:60]}")

                # Extraer números
                numeros = re.findall(r'[S/\.\$€£]?\s*(\d+[.,]\d{2}|\d+)', linea)
                if numeros:
                    try:
                        monto_str = numeros[-1].replace(',', '.')
                        monto_total = float(monto_str)
                        print(f"[EXTRACCION] ✅ Monto: {SIMBOLO_MONEDA} {monto_total:.2f}")

                        # Detectar moneda
                        if 'S/.' in linea or 's/.' in linea:
                            moneda = 'S/.'
                        elif '$' in linea:
                            moneda = '$'
                        elif '€' in linea:
                            moneda = '€'
                        break
                    except ValueError:
                        pass

    # Si no se encontró, buscar el número más grande
    if not monto_total:
        print(f"[EXTRACCION] ⚠️ No encontrado con palabras clave, buscando números...")
        numeros = re.findall(r'(\d+[.,]\d{2})', texto)
        if numeros:
            try:
                monto_str = numeros[-1].replace(',', '.')
                monto_total = float(monto_str)
                print(f"[EXTRACCION] ✅ Monto (último número): {SIMBOLO_MONEDA} {monto_total:.2f}")
            except ValueError:
                pass

    # Buscar vendedor (primeras líneas no vacías)
    vendedor = 'Comercio'
    print(f"[EXTRACCION] Buscando vendedor...")
    for linea in lineas:
        if linea and len(linea) > 3 and not re.search(r'^\d+', linea):
            vendedor = linea
            print(f"[EXTRACCION] ✅ Vendedor: {vendedor}")
            break

    # Buscar fecha (formato dd/mm/yyyy o dd-mm-yyyy)
    fecha = None
    patron_fecha = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
    match = re.search(patron_fecha, texto)
    if match:
        fecha = match.group(1)
        print(f"[EXTRACCION] ✅ Fecha: {fecha}")

    # Búsqueda de items (líneas con S/. o números)
    items = []
    print(f"[EXTRACCION] Extrayendo items...")
    for linea in lineas:
        if re.search(r'S/\.\s*\d+[.,]\d{2}', linea) or re.search(r'^\d+\s+', linea):
            items.append(linea)
    print(f"[EXTRACCION] ✅ Items encontrados: {len(items)}")

    resultado = {
        'monto_total': monto_total,
        'moneda': moneda,
        'vendedor': vendedor,
        'fecha': fecha,
        'categoría': 'Compras',
        'descripción': f'Compra en {vendedor}',
        'items': items
    }

    print(f"[EXTRACCION] ✅ Resumen:")
    print(f"[EXTRACCION]   - Monto: {moneda} {monto_total:.2f}" if monto_total else "[EXTRACCION]   - Monto: No encontrado")
    print(f"[EXTRACCION]   - Vendedor: {vendedor}")
    print(f"[EXTRACCION]   - Fecha: {fecha or 'No encontrada'}")
    print(f"[EXTRACCION]   - Items: {len(items)}")

    return resultado

