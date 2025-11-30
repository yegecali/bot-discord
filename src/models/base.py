"""
Configuración base de SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import DB_PATH
from src.utils import get_logger

logger = get_logger(__name__)

# Configurar la conexión a la base de datos
DATABASE_URL = f"sqlite:///{DB_PATH}"
logger.info(f"🗄️ Conectando a: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def init_db():
    """Inicializa la base de datos creando todas las tablas"""
    logger.info("📋 Inicializando tablas...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas creadas correctamente")


def get_db():
    """Obtiene una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

