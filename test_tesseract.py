#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de verificación de Tesseract OCR
Ejecuta este script para diagnosticar problemas con Tesseract
"""

import os
import sys
import subprocess
import pytesseract

# IMPORTANTE: Importar factura_processor ANTES de verificar, para que configure pytesseract
print("Importando factura_processor (esto configurará pytesseract)...\n")
from factura_processor import procesar_factura
from pathlib import Path
from PIL import Image

print("="*70)
print("🔍 VERIFICADOR DE TESSERACT OCR")
print("="*70)

# Paso 1: Verificar PATH
print("\n[1/5] Verificando si Tesseract está en PATH...")
try:
    resultado = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
    if resultado.returncode == 0:
        print(f"✅ Tesseract encontrado en PATH")
        print(f"    Versión: {resultado.stdout.split(chr(10))[0]}")
        en_path = True
    else:
        print(f"❌ Error ejecutando tesseract")
        print(f"    Stderr: {resultado.stderr}")
        en_path = False
except Exception as e:
    print(f"❌ Tesseract NO está en PATH: {e}")
    en_path = False

# Paso 2: Verificar rutas locales
print("\n[2/5] Verificando rutas locales de Tesseract...")
rutas_posibles = [
    r'C:\Users\Yemi Genderson\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
]

encontrada = False
for ruta in rutas_posibles:
    if os.path.exists(ruta):
        print(f"✅ Encontrado: {ruta}")
        # Intentar ejecutar
        try:
            resultado = subprocess.run([ruta, '--version'], capture_output=True, text=True)
            if resultado.returncode == 0:
                print(f"    ✅ Verificación: OK")
                print(f"    Versión: {resultado.stdout.split(chr(10))[0]}")
                encontrada = True
        except Exception as e:
            print(f"    ❌ Error: {e}")
    else:
        print(f"❌ No existe: {ruta}")

# Paso 3: Verificar pytesseract
print("\n[3/5] Verificando configuración de pytesseract...")
print(f"tesseract_cmd = {pytesseract.pytesseract.tesseract_cmd}")

# Paso 4: Intentar OCR con imagen de prueba
print("\n[4/5] Intentando OCR con imagen de prueba...")
try:
    # Crear imagen de prueba simple
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)

    # Escribir texto simple
    texto = "TOTAL: $100.50"
    draw.text((50, 50), texto, fill='black')

    # Guardar imagen temporal
    test_image_path = 'test_factura.png'
    img.save(test_image_path)
    print(f"✅ Imagen de prueba creada: {test_image_path}")

    # Intentar OCR
    print("Ejecutando OCR en imagen de prueba...")
    texto_ocr = pytesseract.image_to_string(img, lang='spa+eng')
    print(f"✅ OCR completado exitosamente")
    print(f"Texto extraído: {repr(texto_ocr)}")

    # Limpiar
    os.remove(test_image_path)

except Exception as e:
    print(f"❌ Error en OCR: {e}")
    import traceback
    traceback.print_exc()

# Paso 5: Resumen
print("\n[5/5] RESUMEN")
print("-"*70)

if en_path or encontrada:
    print("✅ Tesseract está correctamente instalado")
    print("\n   El bot debería funcionar sin problemas.")
    print("   Si aún tiene errores, intenta:")
    print("   1. Reiniciar Python/Terminal")
    print("   2. Reiniciar el bot con: python main.py")
else:
    print("❌ Tesseract NO está instalado o no se encuentra")
    print("\n   Solución:")
    print("   1. Descarga desde: https://github.com/UB-Mannheim/tesseract/wiki")
    print("   2. Ejecuta: tesseract-ocr-w64-setup-v5.x.x.exe")
    print("   3. Reinicia tu terminal")

print("\n" + "="*70)
print("FIN DE LA VERIFICACIÓN")
print("="*70 + "\n")

