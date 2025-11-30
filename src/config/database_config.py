"""
Configuración de base de datos
"""
from pathlib import Path

# ============================================================
# BASE DE DATOS
# ============================================================
BASE_DIR = Path(__file__).parent.parent.parent
DB_PATH = BASE_DIR / 'gastos.db'

