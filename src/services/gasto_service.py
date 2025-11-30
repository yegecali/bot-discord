"""
Servicio de Gastos
Lógica de aplicación para operaciones de gastos
"""
from src.repository import GastoRepository
from src.config import SIMBOLO_MONEDA
import discord


class GastoService:
    """Servicio con lógica de aplicación para gastos"""

    @staticmethod
    def crear_gasto_desde_factura(usuario_id, descripcion, monto, categoria, imagen_url=None, datos_ocr=None):
        """Crea un gasto desde una factura procesada"""
        gasto = GastoRepository.crear_gasto(
            usuario_id=usuario_id,
            descripcion=descripcion,
            monto=monto,
            categoria=categoria,
            imagen_url=imagen_url,
            datos_ocr=datos_ocr
        )
        print(f"[SERVICE] 📸 Gasto registrado desde factura: {descripcion}")
        return gasto

    @staticmethod
    def obtener_resumen_gastos(usuario_id, dias=30):
        """Obtiene resumen de gastos para mostrar"""
        gastos = GastoRepository.obtener_gastos_usuario(usuario_id, dias)
        total = GastoRepository.obtener_total_gastos(usuario_id, dias)

        return {
            'gastos': gastos,
            'total': total,
            'cantidad': len(gastos),
            'promedio': total / len(gastos) if gastos else 0
        }

    @staticmethod
    def obtener_resumen_por_categoria(usuario_id, dias=30):
        """Obtiene resumen agrupado por categoría"""
        return GastoRepository.obtener_gastos_por_categoria(usuario_id, dias)

    @staticmethod
    def obtener_estadisticas_completas(usuario_id, dias=30):
        """Obtiene estadísticas completas"""
        return GastoRepository.obtener_estadisticas(usuario_id, dias)

    @staticmethod
    def crear_embed_gastos(usuario_id, dias=30):
        """Crea un embed de Discord con los gastos"""
        resumen = GastoService.obtener_resumen_gastos(usuario_id, dias)

        embed = discord.Embed(
            title=f"📊 Tus Gastos (últimos {dias} días)",
            description=f"Total de registros: {resumen['cantidad']}",
            color=discord.Color.blue()
        )

        for gasto in resumen['gastos'][:10]:
            embed.add_field(
                name=f"{gasto.categoria} - {gasto.fecha}",
                value=f"**{SIMBOLO_MONEDA} {gasto.monto:.2f}** - {gasto.descripcion}",
                inline=False
            )

        if len(resumen['gastos']) > 10:
            embed.set_footer(text=f"... y {len(resumen['gastos']) - 10} más gastos")

        return embed

    @staticmethod
    def crear_embed_total(usuario_id, dias=30):
        """Crea un embed con total de gastos"""
        resumen = GastoService.obtener_resumen_gastos(usuario_id, dias)

        embed = discord.Embed(
            title="💰 Resumen de Gastos",
            color=discord.Color.gold()
        )

        embed.add_field(
            name=f"Total (últimos {dias} días)",
            value=f"**{SIMBOLO_MONEDA} {resumen['total']:.2f}**",
            inline=False
        )

        embed.add_field(
            name="📈 Número de transacciones",
            value=f"{resumen['cantidad']}",
            inline=True
        )

        if resumen['cantidad'] > 0:
            embed.add_field(
                name="📊 Promedio por transacción",
                value=f"{SIMBOLO_MONEDA} {resumen['promedio']:.2f}",
                inline=True
            )

        return embed

    @staticmethod
    def crear_embed_categorias(usuario_id, dias=30):
        """Crea un embed con gastos por categoría"""
        categorias = GastoService.obtener_resumen_por_categoria(usuario_id, dias)

        embed = discord.Embed(
            title=f"📊 Gastos por Categoría (últimos {dias} días)",
            color=discord.Color.purple()
        )

        emojis = {
            'alimentación': '🍔',
            'transporte': '🚗',
            'servicios': '🔧',
            'electrónica': '💻',
            'entretenimiento': '🎮',
            'salud': '🏥',
            'compras': '🛍️',
            'otros': '📦'
        }

        total_general = 0
        for categoria, total, cantidad in categorias:
            emoji = emojis.get(categoria.lower(), '📦')
            embed.add_field(
                name=f"{emoji} {categoria}",
                value=f"{SIMBOLO_MONEDA} {total:.2f} ({cantidad} compras)",
                inline=False
            )
            total_general += total

        embed.set_footer(text=f"Total: {SIMBOLO_MONEDA} {total_general:.2f}")
        return embed

