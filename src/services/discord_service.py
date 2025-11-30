"""
Servicio de Discord
Lógica de aplicación relacionada con Discord
"""
import discord
from src.config import COMMAND_PREFIX


class DiscordService:
    """Servicio con lógica de Discord"""

    @staticmethod
    def crear_embed_info_bot():
        """Crea embed de información del bot"""
        embed = discord.Embed(
            title="🤖 Ayuda del Bot",
            description="Gestor de gastos y procesador de facturas",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📸 Procesar Facturas",
            value="Envía una imagen de factura en el chat y el bot la procesará automáticamente",
            inline=False
        )

        embed.add_field(
            name="💰 Comandos de Gastos",
            value=f"`{COMMAND_PREFIX}gastos` - Ver gastos recientes\n"
                  f"`{COMMAND_PREFIX}total` - Total de gastos\n"
                  f"`{COMMAND_PREFIX}categorias` - Gastos por categoría",
            inline=False
        )

        embed.add_field(
            name="📋 Otros Comandos",
            value=f"`{COMMAND_PREFIX}canales` - Listar canales\n"
                  f"`{COMMAND_PREFIX}ping` - Ver latencia\n"
                  f"`{COMMAND_PREFIX}hola` - Saludar",
            inline=False
        )

        embed.add_field(
            name="💡 Consejos",
            value="• Asegúrate que las facturas sean legibles\n"
                  "• El bot extrae montos en S/. (Soles)\n"
                  "• Los datos se guardan en la base de datos",
            inline=False
        )

        embed.set_footer(text=f"Usa {COMMAND_PREFIX}ayuda <comando> para más información")
        return embed

    @staticmethod
    def listar_canales_guild(guild: discord.Guild):
        """Crea embed con lista de canales"""
        text_channels = [ch for ch in guild.channels if isinstance(ch, discord.TextChannel)]
        voice_channels = [ch for ch in guild.channels if isinstance(ch, discord.VoiceChannel)]

        embed = discord.Embed(
            title=f"📋 Canales de {guild.name}",
            description=f"Total: {len(guild.channels)} canales",
            color=discord.Color.purple()
        )

        if text_channels:
            canal_list = '\n'.join([f'💬 {ch.mention}' for ch in text_channels[:15]])
            if len(text_channels) > 15:
                canal_list += f'\n... y {len(text_channels) - 15} más'
            embed.add_field(
                name=f"Canales de Texto ({len(text_channels)})",
                value=canal_list,
                inline=False
            )

        if voice_channels:
            canal_list = '\n'.join([f'🎤 {ch.name}' for ch in voice_channels[:10]])
            if len(voice_channels) > 10:
                canal_list += f'\n... y {len(voice_channels) - 10} más'
            embed.add_field(
                name=f"Canales de Voz ({len(voice_channels)})",
                value=canal_list,
                inline=False
            )

        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        return embed

    @staticmethod
    def crear_embed_bienvenida(usuario):
        """Crea embed de bienvenida"""
        embed = discord.Embed(
            title="👋 ¡Hola!",
            description=f"¿Qué tal, {usuario.mention}?",
            color=discord.Color.purple()
        )
        return embed

    @staticmethod
    def crear_embed_pong(latencia_ms):
        """Crea embed de pong"""
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latencia: **{latencia_ms}ms**",
            color=discord.Color.blue()
        )
        return embed

    @staticmethod
    def crear_embed_error(titulo, mensaje):
        """Crea embed de error"""
        embed = discord.Embed(
            title=f"❌ {titulo}",
            description=mensaje,
            color=discord.Color.red()
        )
        return embed

    @staticmethod
    def crear_embed_exito(titulo, mensaje):
        """Crea embed de éxito"""
        embed = discord.Embed(
            title=f"✅ {titulo}",
            description=mensaje,
            color=discord.Color.green()
        )
        return embed

