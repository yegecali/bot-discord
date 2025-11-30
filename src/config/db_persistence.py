"""
Solución para persistencia de BD en SQLite
Este módulo asegura que los datos persistan correctamente
"""
import os
from pathlib import Path
from sqlalchemy import event, text
from sqlalchemy.engine import Engine
from src.config import DB_PATH
from src.utils import get_logger
from src.config.exception_handler import ExceptionHandler

logger = get_logger(__name__)


def ensure_db_persistence():
    """
    Asegura que la BD persista correctamente

    Soluciona:
    - WAL mode para mejor concurrencia
    - Sincronización correcta
    - Integridad referencial
    - Timeout para locks
    """
    try:
        from src.models.base import engine

        # Habilitar WAL mode (Write-Ahead Logging)
        # Mejor para concurrencia y evita locks
        with engine.connect() as conn:
            conn.execute(text("PRAGMA journal_mode=WAL"))
            conn.execute(text("PRAGMA synchronous=NORMAL"))  # FULL para máxima seguridad
            conn.execute(text("PRAGMA foreign_keys=ON"))
            conn.execute(text("PRAGMA cache_size=10000"))
            conn.execute(text("PRAGMA busy_timeout=5000"))  # 5 segundos timeout
            conn.commit()

        logger.info("✅ Modo WAL habilitado")
        logger.info("✅ Sincronización configurada")
        logger.info("✅ Foreign keys habilitadas")
    except Exception as e:
        ExceptionHandler.manejar_error(
            excepcion=e,
            contexto="Configurando persistencia de BD",
            datos_adicionales={'BD': DB_PATH}
        )
        raise


def verify_db_exists():
    """Verifica que la BD existe y tiene tablas"""
    try:
        from src.models import init_db

        db_path = Path(DB_PATH)

        # Si BD no existe o está vacía, crearla
        if not db_path.exists() or db_path.stat().st_size == 0:
            logger.info(f"📝 Creando BD en: {DB_PATH}")
            init_db()
            logger.info(f"✅ BD creada correctamente")
        else:
            logger.info(f"✅ BD existe: {db_path.stat().st_size} bytes")

            # Verificar que tiene tablas
            import sqlite3
            try:
                conn = sqlite3.connect(str(DB_PATH))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                conn.close()

                if not tables:
                    logger.warning(f"⚠️ BD vacía, recreando tablas...")
                    init_db()
                    logger.info(f"✅ Tablas recreadas")
                else:
                    logger.info(f"✅ Tablas encontradas: {len(tables)}")
            except Exception as e:
                ExceptionHandler.manejar_error(
                    excepcion=e,
                    contexto="Verificando tablas de BD",
                    datos_adicionales={'BD': DB_PATH}
                )
                raise
    except Exception as e:
        ExceptionHandler.manejar_error(
            excepcion=e,
            contexto="Verificando existencia de BD",
            datos_adicionales={'Ruta': DB_PATH}
        )
        raise


def check_db_permissions():
    """Verifica permisos de lectura/escritura"""
    try:
        if not os.access(DB_PATH, os.R_OK):
            logger.error(f"❌ Sin permisos de lectura")
            return False

        if not os.access(DB_PATH, os.W_OK):
            logger.error(f"❌ Sin permisos de escritura")
            return False

        logger.info(f"✅ Permisos OK (lectura/escritura)")
        return True
    except Exception as e:
        ExceptionHandler.manejar_error(
            excepcion=e,
            contexto="Verificando permisos de BD",
            datos_adicionales={'BD': DB_PATH}
        )
        raise


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Event listener para configurar SQLite en cada conexión"""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA temp_store=MEMORY")
    cursor.close()

