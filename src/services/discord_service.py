"""
Servicio de Discord
Lógica de aplicación relacionada con Discord
"""
import discord


class DiscordService:
    """Servicio con lógica de Discord"""

    @staticmethod
    def crear_embed_error(titulo, mensaje):
        """Crea embed de error"""
        embed = discord.Embed(
            title=f"[ERROR] {titulo}",
            description=mensaje,
            color=discord.Color.red()
        )
        return embed

    @staticmethod
    def crear_embed_exito(titulo, mensaje):
        """Crea embed de éxito"""
        embed = discord.Embed(
            title=f"[OK] {titulo}",
            description=mensaje,
            color=discord.Color.green()
        )
        return embed

