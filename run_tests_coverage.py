#!/usr/bin/env python
"""
Script para ejecutar tests con cobertura
Uso: python run_tests_coverage.py
"""
import subprocess
import sys
from pathlib import Path

def ejecutar_tests_con_cobertura():
    """Ejecuta los tests con reporte de cobertura"""

    print("\n" + "="*60)
    print("🧪 EJECUTANDO TESTS CON COBERTURA")
    print("="*60 + "\n")

    # Comando pytest con cobertura
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=src",
        "--cov-report=html",
        "--cov-report=term",
        "--tb=short"
    ]

    resultado = subprocess.run(cmd, cwd=Path(__file__).parent)

    if resultado.returncode == 0:
        print("\n" + "="*60)
        print("✅ TODOS LOS TESTS PASARON")
        print("📊 Reporte HTML en: htmlcov/index.html")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("❌ ALGUNOS TESTS FALLARON")
        print("="*60 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    ejecutar_tests_con_cobertura()

