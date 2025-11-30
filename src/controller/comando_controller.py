"""
Controlador de Comandos
Manejadores de comandos del bot
"""
import discord
from discord.ext import commands
from src.services import GastoService, DiscordService
from src.config import COMMAND_PREFIX


def registrar_comandos_en_controller(bot):
    """
    Registra todos los comandos del bot usando el controller

    Args:
        bot: Instancia del bot
    """
    controller = ComandoController(bot)

    @bot.command(name='ping')
    async def ping(ctx):
        """Verifica latencia"""
        await controller.ping(ctx)

    @bot.command(name='hola')
    async def hola(ctx):
        """Saluda"""
        await controller.hola(ctx)

    @bot.command(name='canales')
    async def canales(ctx):
        """Lista canales"""
        await controller.canales(ctx)

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

    @bot.command(name='ayuda')
    async def ayuda(ctx):
        """Ver ayuda"""
        await controller.ver_ayuda(ctx)


class ComandoController:
    """Controlador de comandos"""

    def __init__(self, bot):
        self.bot = bot

    async def ping(self, ctx):
        """Comando ping"""
        latencia = round(self.bot.latency * 1000)
        embed = DiscordService.crear_embed_pong(latencia)
        await ctx.send(embed=embed)

    async def hola(self, ctx):
        """Comando hola"""
        embed = DiscordService.crear_embed_bienvenida(ctx.author)
        await ctx.send(embed=embed)

    async def canales(self, ctx):
        """Comando canales"""
        embed = DiscordService.listar_canales_guild(ctx.guild)
        await ctx.send(embed=embed)

    async def ver_gastos(self, ctx, dias: int = 30):
        """Comando gastos"""
        print(f"[CONTROLLER] !gastos ejecutado por {ctx.author}")
        embed = GastoService.crear_embed_gastos(ctx.author.id, dias)
        await ctx.send(embed=embed)

    async def ver_total(self, ctx, dias: int = 30):
        """Comando total"""
        print(f"[CONTROLLER] !total ejecutado por {ctx.author}")
        embed = GastoService.crear_embed_total(ctx.author.id, dias)
        await ctx.send(embed=embed)

    async def ver_categorias(self, ctx, dias: int = 30):
        """Comando categorias"""
        print(f"[CONTROLLER] !categorias ejecutado por {ctx.author}")
        embed = GastoService.crear_embed_categorias(ctx.author.id, dias)
        await ctx.send(embed=embed)

    async def ver_ayuda(self, ctx):
        """Comando ayuda"""
        print(f"[CONTROLLER] !ayuda ejecutado por {ctx.author}")
        embed = DiscordService.crear_embed_info_bot()
        await ctx.send(embed=embed)

