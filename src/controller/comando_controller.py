"""
Controlador de Comandos
Manejadores de comandos del bot
"""
import discord
from discord.ext import commands
from src.services import GastoService, DiscordService
from src.config import COMMAND_PREFIX
from src.utils import get_logger

logger = get_logger(__name__)


def registrar_comandos_en_controller(bot):
    """
    Registra todos los comandos del bot usando el controller

    Args:
        bot: Instancia del bot
    """
    controller = ComandoController(bot)

    @bot.command(name='gastos')
    async def gastos(ctx, dias: int = 30):
        """Ver gastos"""
        await controller.ver_gastos(ctx, dias)

    @bot.command(name='total')
    async def total(ctx, dias: int = 30):
        """Ver total"""
        await controller.ver_total(ctx, dias)

    @bot.command(name='categorias')
    async def categorias(ctx, dias: int = 30):
        """Ver por categoría"""
        await controller.ver_categorias(ctx, dias)



class ComandoController:
    """Controlador de comandos"""

    def __init__(self, bot):
        self.bot = bot

    async def ver_gastos(self, ctx, dias: int = 30):
        """Comando gastos"""
        logger.info(f"💰 Comando !gastos ejecutado por {ctx.author}")
        embed = GastoService.crear_embed_gastos(ctx.author.id, dias)
        await ctx.send(embed=embed)

    async def ver_total(self, ctx, dias: int = 30):
        """Comando total"""
        logger.info(f"📊 Comando !total ejecutado por {ctx.author}")
        embed = GastoService.crear_embed_total(ctx.author.id, dias)
        await ctx.send(embed=embed)

    async def ver_categorias(self, ctx, dias: int = 30):
        """Comando categorias"""
        logger.info(f"📈 Comando !categorias ejecutado por {ctx.author}")
        embed = GastoService.crear_embed_categorias(ctx.author.id, dias)
        await ctx.send(embed=embed)

