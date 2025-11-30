#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script rápido para verificar que Tesseract está configurado correctamente
Ejecuta esto ANTES de python main.py
"""

print("\n" + "="*70)
print("🔍 VERIFICACIÓN RÁPIDA DE TESSERACT")
print("="*70 + "\n")

# Importar factura_processor para que configure pytesseract
print("[1/3] Importando módulos...")
try:
    from factura_processor import pytesseract
    print("✅ Módulos importados\n")
except Exception as e:
    print(f"❌ Error importando: {e}\n")
    exit(1)

# Verificar configuración
print("[2/3] Verificando configuración de pytesseract...")
tesseract_cmd = pytesseract.pytesseract.tesseract_cmd
print(f"tesseract_cmd = {tesseract_cmd}")

import os
if tesseract_cmd and os.path.exists(str(tesseract_cmd)):
    print(f"✅ Ruta existe: {tesseract_cmd}\n")
else:
    print(f"⚠️ Ruta podría no existir o no ser accesible\n")

# Intentar ejecutar un OCR simple
print("[3/3] Probando OCR...")
try:
    from PIL import Image, ImageDraw

    # Crear imagen de prueba
    img = Image.new('RGB', (300, 100), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((50, 40), "TOTAL: S/. 99.99", fill='black')

    # Ejecutar OCR
    texto = pytesseract.image_to_string(img, lang='spa+eng')
    print(f"Texto extraído: {repr(texto)}")

    if "99" in texto or "TOTAL" in texto:
        print("✅ OCR funciona correctamente!\n")
    else:
        print("⚠️ OCR ejecutado pero resultado extraño\n")

except Exception as e:
    print(f"❌ Error en OCR: {e}\n")
    exit(1)

print("="*70)
print("✅ TODO ESTÁ LISTO - Ejecuta: python main.py")
print("="*70 + "\n")

