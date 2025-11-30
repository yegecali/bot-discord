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

from src.config import TESSERACT_CMD, OCR_IDIOMAS, SIMBOLO_MONEDA, ocr_config

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
    Extrae información de la factura del texto OCR con múltiples criterios

    Args:
        texto (str): Texto extraído por OCR

    Returns:
        dict: Información de la factura
    """
    print(f"[EXTRACCION] Analizando {len(texto)} caracteres")

    lineas = [l.strip() for l in texto.split('\n')]
    print(f"[EXTRACCION] Total de líneas: {len(lineas)}")

    # ================================================================
    # EXTRACCIÓN DE MONTO TOTAL
    # ================================================================
    monto_total = _extraer_monto(lineas, texto)
    moneda = _detectar_moneda(texto)

    # ================================================================
    # EXTRACCIÓN DE VENDEDOR
    # ================================================================
    vendedor = _extraer_vendedor(lineas, texto)

    # ================================================================
    # EXTRACCIÓN DE FECHA
    # ================================================================
    fecha = _extraer_fecha(lineas, texto)

    # ================================================================
    # EXTRACCIÓN DE DESCRIPCIÓN
    # ================================================================
    descripcion = _extraer_descripcion(lineas, vendedor, texto)

    # ================================================================
    # EXTRACCIÓN DE CATEGORÍA
    # ================================================================
    categoria = _detectar_categoria(descripcion, texto)

    # Búsqueda de items (líneas con moneda o números)
    items = []
    print(f"[EXTRACCION] Extrayendo items...")
    for linea in lineas:
        if re.search(r'S/\.\s*\d+[.,]\d{2}', linea) or re.search(r'\$\s*\d+[.,]\d{2}', linea):
            items.append(linea)
    print(f"[EXTRACCION] ✅ Items encontrados: {len(items)}")

    resultado = {
        'monto_total': monto_total,
        'moneda': moneda,
        'vendedor': vendedor,
        'fecha': fecha,
        'categoría': categoria,
        'descripción': descripcion,
        'items': items
    }

    print(f"[EXTRACCION] ✅ Resumen:")
    print(f"[EXTRACCION]   - Monto: {moneda} {monto_total:.2f}" if monto_total else "[EXTRACCION]   - Monto: No encontrado")
    print(f"[EXTRACCION]   - Vendedor: {vendedor}")
    print(f"[EXTRACCION]   - Fecha: {fecha or 'No encontrada'}")
    print(f"[EXTRACCION]   - Descripción: {descripcion}")
    print(f"[EXTRACCION]   - Categoría: {categoria}")
    print(f"[EXTRACCION]   - Items: {len(items)}")

    return resultado


def _extraer_monto(lineas, texto_completo):
    """Extrae el monto total usando múltiples criterios"""
    print(f"[MONTO] Iniciando búsqueda de monto...")

    monto_total = None
    palabras_total = ocr_config.get_palabras_total()

    # Criterio 1: Palabras clave específicas
    print(f"[MONTO] Criterio 1: Palabras clave {palabras_total}")
    for idx, linea in enumerate(lineas):
        linea_lower = linea.lower()
        for palabra in palabras_total:
            if palabra in linea_lower and not monto_total:
                print(f"[MONTO] > Encontrada palabra '{palabra}' en línea {idx}")
                monto_total = _extraer_numero(linea)
                if monto_total:
                    print(f"[MONTO] ✅ Monto por palabra clave: {monto_total:.2f}")
                    return monto_total

    # Criterio 2: Línea con símbolo de moneda al final
    print(f"[MONTO] Criterio 2: Líneas con símbolo de moneda")
    for linea in lineas:
        if re.search(r'(S/\.|€|\$)\s*\d+[.,]\d{2}\s*$', linea):
            monto = _extraer_numero(linea)
            if monto:
                print(f"[MONTO] ✅ Monto por símbolo de moneda: {monto:.2f}")
                return monto

    # Criterio 3: Línea con 2 decimales (número más grande)
    print(f"[MONTO] Criterio 3: Número más grande con decimales")
    numeros = re.findall(r'(\d+[.,]\d{2})', texto_completo)
    if numeros:
        try:
            monto_str = numeros[-1].replace(',', '.')
            monto_total = float(monto_str)
            if monto_total > 0:
                print(f"[MONTO] ✅ Monto por número más grande: {monto_total:.2f}")
                return monto_total
        except ValueError:
            pass

    # Criterio 4: Línea que contiene muchos números (suma total)
    print(f"[MONTO] Criterio 4: Línea con múltiples números")
    for linea in reversed(lineas):
        numeros_en_linea = re.findall(r'\d+[.,]\d{2}', linea)
        if len(numeros_en_linea) >= 2:
            monto = _extraer_numero(linea)
            if monto:
                print(f"[MONTO] ✅ Monto por línea con múltiples números: {monto:.2f}")
                return monto

    print(f"[MONTO] ⚠️ No se encontró monto")
    return None


def _extraer_numero(linea):
    """Extrae el primer número decimal encontrado en una línea"""
    numeros = re.findall(r'(\d+[.,]\d{2}|\d+)', linea)
    if numeros:
        try:
            monto_str = numeros[-1].replace(',', '.')
            return float(monto_str)
        except ValueError:
            pass
    return None


def _detectar_moneda(texto):
    """Detecta la moneda del texto"""
    if 'S/.' in texto or 's/.' in texto:
        return 'S/.'
    elif '$' in texto:
        return '$'
    elif '€' in texto:
        return '€'
    elif '£' in texto:
        return '£'
    return SIMBOLO_MONEDA


def _extraer_vendedor(lineas, texto_completo):
    """Extrae el vendedor usando múltiples criterios"""
    print(f"[VENDEDOR] Buscando vendedor...")

    vendedor = 'Comercio'

    # Criterio 1: Primeras líneas no vacías que no sean números
    print(f"[VENDEDOR] Criterio 1: Primeras líneas no numéricas")
    for linea in lineas[:10]:
        if (linea and len(linea) > 3 and
            not re.search(r'^[\d\s\-\/]+$', linea) and
            not re.search(r'^[A-Z\s]+$', linea)):
            vendedor = linea
            print(f"[VENDEDOR] ✅ Vendedor: {vendedor}")
            return vendedor

    # Criterio 2: Línea que contiene palabras clave de negocio
    print(f"[VENDEDOR] Criterio 2: Palabras clave de negocio")
    palabras_negocio = ['tienda', 'comercio', 'empresa', 'establecimiento', 'negocio', 'supermercado', 'mercado']
    for linea in lineas:
        linea_lower = linea.lower()
        for palabra in palabras_negocio:
            if palabra in linea_lower:
                vendedor = linea
                print(f"[VENDEDOR] ✅ Vendedor: {vendedor}")
                return vendedor

    # Criterio 3: Línea con mayúsculas (frecuentemente es el nombre de la tienda)
    print(f"[VENDEDOR] Criterio 3: Línea con mayúsculas")
    for linea in lineas[:15]:
        if linea and re.search(r'[A-Z]{3,}', linea) and len(linea) > 5:
            vendedor = linea
            print(f"[VENDEDOR] ✅ Vendedor: {vendedor}")
            return vendedor

    print(f"[VENDEDOR] Vendedor por defecto: {vendedor}")
    return vendedor


def _extraer_fecha(lineas, texto_completo):
    """Extrae la fecha usando múltiples criterios"""
    print(f"[FECHA] Buscando fecha...")

    # Criterio 1: Formato dd/mm/yyyy o dd-mm-yyyy
    print(f"[FECHA] Criterio 1: Formato dd/mm/yyyy o dd-mm-yyyy")
    patron_fecha1 = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
    match = re.search(patron_fecha1, texto_completo)
    if match:
        fecha = match.group(1)
        print(f"[FECHA] ✅ Fecha encontrada: {fecha}")
        return fecha

    # Criterio 2: Formato completo con mes en texto
    print(f"[FECHA] Criterio 2: Formato con mes en texto")
    meses = r'(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|january|february|march|april|may|june|july|august|september|october|november|december)'
    patron_fecha2 = rf'(\d{{1,2}}\s+de?\s+{meses}\s+de\s+\d{{2,4}}|\d{{1,2}}\s+{meses}\s+\d{{2,4}})'
    match = re.search(patron_fecha2, texto_completo, re.IGNORECASE)
    if match:
        fecha = match.group(0)
        print(f"[FECHA] ✅ Fecha encontrada: {fecha}")
        return fecha

    # Criterio 3: Línea que contiene palabras clave de fecha
    print(f"[FECHA] Criterio 3: Palabras clave de fecha")
    palabras_fecha = ['fecha', 'fecha de emisión', 'expedición', 'día']
    for idx, linea in enumerate(lineas):
        linea_lower = linea.lower()
        for palabra in palabras_fecha:
            if palabra in linea_lower:
                # Buscar número en la misma línea o siguiente
                numero = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', linea)
                if numero:
                    fecha = numero.group(1)
                    print(f"[FECHA] ✅ Fecha por palabra clave: {fecha}")
                    return fecha
                # Buscar en siguiente línea
                if idx + 1 < len(lineas):
                    numero = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', lineas[idx + 1])
                    if numero:
                        fecha = numero.group(1)
                        print(f"[FECHA] ✅ Fecha en línea siguiente: {fecha}")
                        return fecha

    print(f"[FECHA] ⚠️ Fecha no encontrada")
    return None


def _extraer_descripcion(lineas, vendedor, texto_completo):
    """Extrae la descripción usando múltiples criterios"""
    print(f"[DESCRIPCION] Extrayendo descripción...")

    # Criterio 1: Usar el vendedor
    descripcion = f'Compra en {vendedor}'

    # Criterio 2: Buscar línea con productos/artículos
    print(f"[DESCRIPCION] Criterio 2: Línea con productos")
    for linea in lineas:
        if (re.search(r'\b(producto|artículo|item|referencia)\b', linea, re.IGNORECASE) and
            len(linea) > 10):
            descripcion = linea
            print(f"[DESCRIPCION] ✅ Descripción por producto: {descripcion}")
            return descripcion

    # Criterio 3: Línea más larga entre líneas de descripción (frecuentemente la descripción)
    print(f"[DESCRIPCION] Criterio 3: Línea más larga")
    lineas_largas = [l for l in lineas if 15 < len(l) < 80 and not re.search(r'^\d+[\.,\s\d]+$', l)]
    if lineas_largas:
        descripcion = max(lineas_largas, key=len)
        print(f"[DESCRIPCION] ✅ Descripción por línea larga: {descripcion}")
        return descripcion

    print(f"[DESCRIPCION] Descripción por defecto: {descripcion}")
    return descripcion


def _detectar_categoria(descripcion, texto_completo):
    """Detecta la categoría automáticamente"""
    print(f"[CATEGORIA] Detectando categoría...")

    categorias_map = {
        'Alimentación': ['supermercado', 'mercado', 'panadería', 'carnicería', 'verdulería', 'tienda de alimentos', 'restaurante', 'comida'],
        'Transporte': ['gasolina', 'uber', 'taxi', 'bus', 'pasaje', 'tren', 'auto', 'combustible'],
        'Salud': ['farmacia', 'medicina', 'doctor', 'hospital', 'médico', 'salud'],
        'Electrónica': ['electrónica', 'tienda tech', 'computadora', 'teléfono', 'laptop'],
        'Entretenimiento': ['cine', 'teatro', 'juegos', 'música', 'entretenimiento'],
        'Servicios': ['servicio', 'reparación', 'plomería', 'electricidad', 'mantenimiento'],
        'Compras': ['compras', 'tienda', 'ropa', 'calzado', 'boutique']
    }

    texto_busqueda = (descripcion + ' ' + texto_completo).lower()

    for categoria, palabras_clave in categorias_map.items():
        for palabra in palabras_clave:
            if palabra in texto_busqueda:
                print(f"[CATEGORIA] ✅ Categoría detectada: {categoria}")
                return categoria

    print(f"[CATEGORIA] Categoría por defecto: Otros")
    return 'Otros'

