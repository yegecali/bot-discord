"""
Servicio de Discord
Lógica de aplicación relacionada con Discord
"""
from src.utils import crear_embed_error, crear_embed_exito, crear_embed_info


class DiscordService:
    """Servicio con lógica de Discord"""

    @staticmethod
    def crear_embed_error(titulo, mensaje):
        """Crea embed de error - DEPRECATED: usar utils.crear_embed_error"""
        return crear_embed_error(titulo, mensaje)

    @staticmethod
    def crear_embed_exito(titulo, mensaje):
        """Crea embed de éxito - DEPRECATED: usar utils.crear_embed_exito"""
        return crear_embed_exito(titulo, mensaje)

