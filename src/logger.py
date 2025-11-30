"""
Módulo de logging centralizado
Proporciona la función get_logger sin dependencias circulares
"""
from src.config.logging_config import LoggerConfig

# Exportar directamente desde LoggerConfig
get_logger = LoggerConfig.get_logger
setup_logging = LoggerConfig.initialize

