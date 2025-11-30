"""
Servicio de Gastos
Lógica de aplicación para operaciones de gastos
"""
from src.repository import GastoRepository
from src.config import SIMBOLO_MONEDA, ExceptionHandler
from src.services.template_service import template_service
from src.utils import get_logger
import discord

logger = get_logger(__name__)


class GastoService:
    """Servicio con lógica de aplicación para gastos"""

    @staticmethod
    def crear_gasto_desde_factura(usuario_id, descripcion, monto, categoria, imagen_url=None, datos_ocr=None):
        """Crea un gasto desde una factura procesada"""
        try:
            gasto = GastoRepository.crear_gasto(
                usuario_id=usuario_id,
                descripcion=descripcion,
                monto=monto,
                categoria=categoria,
                imagen_url=imagen_url,
                datos_ocr=datos_ocr
            )
            logger.info(f"📸 Gasto registrado desde factura: {descripcion}")
            return gasto
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Creando gasto desde factura",
                datos_adicionales={
                    'Usuario ID': usuario_id,
                    'Descripción': descripcion,
                    'Monto': f"{SIMBOLO_MONEDA} {monto:.2f}",
                    'Categoría': categoria,
                    'Archivo': imagen_url or 'N/A'
                }
            )
            raise

    @staticmethod
    def obtener_resumen_gastos(usuario_id, dias=30):
        """Obtiene resumen de gastos para mostrar"""
        try:
            gastos = GastoRepository.obtener_gastos_usuario(usuario_id, dias)
            total = GastoRepository.obtener_total_gastos(usuario_id, dias)

            return {
                'gastos': gastos,
                'total': total,
                'cantidad': len(gastos),
                'promedio': total / len(gastos) if gastos else 0
            }
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Obteniendo resumen de gastos",
                datos_adicionales={
                    'Usuario ID': usuario_id,
                    'Rango días': dias
                }
            )
            raise

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
        """Crea un embed de Discord con los gastos usando plantilla"""
        resumen = GastoService.obtener_resumen_gastos(usuario_id, dias)
        contenido = template_service.render_gastos_recientes(resumen['gastos'], dias)

        embed = discord.Embed(
            title=f"📊 Tus Gastos (últimos {dias} días)",
            description=contenido,
            color=discord.Color.blue()
        )
        return embed

    @staticmethod
    def crear_embed_total(usuario_id, dias=30):
        """Crea un embed con total de gastos usando plantilla"""
        resumen = GastoService.obtener_resumen_gastos(usuario_id, dias)
        contenido = template_service.render_resumen_total(
            resumen['total'],
            resumen['cantidad'],
            resumen['promedio'],
            dias
        )

        embed = discord.Embed(
            title="💰 Resumen de Gastos",
            description=contenido,
            color=discord.Color.gold()
        )
        return embed

    @staticmethod
    def crear_embed_categorias(usuario_id, dias=30):
        """Crea un embed con gastos por categoría usando plantilla"""
        categorias = GastoService.obtener_resumen_por_categoria(usuario_id, dias)
        contenido = template_service.render_gastos_categorias(categorias, dias)

        embed = discord.Embed(
            title=f"📊 Gastos por Categoría (últimos {dias} días)",
            description=contenido,
            color=discord.Color.purple()
        )
        return embed

