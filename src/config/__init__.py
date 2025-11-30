"""
Módulo de configuración
"""
from .app_config import *
from .database_config import *
from .tesseract_config import *
from .ocr_config import ocr_config
from .db_persistence import (
    ensure_db_persistence,
    verify_db_exists,
    check_db_permissions
)


