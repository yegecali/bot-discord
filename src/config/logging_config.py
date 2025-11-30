"""
Configuración centralizada de logging
Sistema profesional de logs con archivos rotatorios y niveles configurables
"""
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

# Directorio de logs
LOGS_DIR = Path(__file__).parent.parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Configuración de formatos
LOG_FORMATS = {
    'console': '[%(name)s] %(levelname)s: %(message)s',
    'file': '%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
    'detailed': '%(asctime)s - [%(name)s] - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
}

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Niveles de log
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


class LoggerConfig:
    """Configuración centralizada de logging"""

    _initialized = False
    _root_logger = None

    @classmethod
    def initialize(cls, level='INFO', enable_file=True, enable_console=True):
        """
        Inicializa el sistema de logging centralizado

        Args:
            level (str): Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            enable_file (bool): Habilitar logs a archivo
            enable_console (bool): Habilitar logs a consola
        """
        if cls._initialized:
            return

        cls._root_logger = logging.getLogger()
        cls._root_logger.setLevel(LOG_LEVELS.get(level, logging.INFO))

        # Limpiar handlers existentes
        for handler in cls._root_logger.handlers[:]:
            cls._root_logger.removeHandler(handler)

        # Handler para consola
        if enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(LOG_LEVELS.get(level, logging.INFO))
            console_formatter = logging.Formatter(
                LOG_FORMATS['console']
            )
            console_handler.setFormatter(console_formatter)
            cls._root_logger.addHandler(console_handler)

        # Handler para archivo con rotación
        if enable_file:
            log_file = LOGS_DIR / f'bot_{datetime.now().strftime("%Y%m%d")}.log'
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10 MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(LOG_LEVELS.get(level, logging.INFO))
            file_formatter = logging.Formatter(
                LOG_FORMATS['file'],
                datefmt=LOG_DATE_FORMAT
            )
            file_handler.setFormatter(file_formatter)
            cls._root_logger.addHandler(file_handler)

        cls._initialized = True

    @classmethod
    def get_logger(cls, module_name: str) -> logging.Logger:
        """
        Obtiene un logger para un módulo

        Args:
            module_name (str): Nombre del módulo (__name__)

        Returns:
            logging.Logger: Logger configurado
        """
        if not cls._initialized:
            cls.initialize()

        return logging.getLogger(module_name)

    @classmethod
    def set_level(cls, level: str):
        """Cambia el nivel de logging global"""
        log_level = LOG_LEVELS.get(level, logging.INFO)
        if cls._root_logger:
            cls._root_logger.setLevel(log_level)
            for handler in cls._root_logger.handlers:
                handler.setLevel(log_level)

    @classmethod
    def get_log_file(cls) -> Path:
        """Obtiene la ruta del archivo de log actual"""
        return LOGS_DIR / f'bot_{datetime.now().strftime("%Y%m%d")}.log'


# Inicializar logging al importar este módulo
LoggerConfig.initialize()

