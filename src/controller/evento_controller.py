"""
Controlador de Eventos
Manejadores de eventos del bot
"""
import discord
from src.repository import GastoRepository
from src.factura_processor import procesar_factura
from src.services import GastoService, DiscordService
from src.config import ExceptionHandler
from src.utils import get_logger

logger = get_logger(__name__)


def registrar_eventos_en_controller(bot):
    """
    Registra todos los eventos del bot

    Args:
        bot: Instancia del bot
    """
    controller = EventoController(bot)

    @bot.event
    async def on_ready():
        """Evento cuando el bot se conecta"""
        await controller.on_ready()

    @bot.event
    async def on_message(message):
        """Evento para procesar mensajes"""
        await controller.on_message(message)


class EventoController:
    """Controlador de eventos"""

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        """Bot conectado"""
        logger.info(f"🤖 Bot conectado como {self.bot.user}")
        logger.info(f"⏱️ Latencia: {round(self.bot.latency * 1000)}ms")

    async def on_message(self, message):
        """Procesar mensajes"""
        logger.debug(f"📬 Mensaje de {message.author}: {message.content}")

        # Ignorar mensajes del bot
        if message.author == self.bot.user:
            await self.bot.process_commands(message)
            return

        # Procesar imágenes (facturas)
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image/'):
                    logger.info(f"📸 Imagen detectada: {attachment.filename}")
                    await self._procesar_factura(message, attachment)

        # Procesar comandos normales
        await self.bot.process_commands(message)

    async def _procesar_factura(self, message, attachment):
        """Procesa una factura"""
        logger.info(f"⏳ Procesando factura...")

        try:
            # Descargar imagen
            import io
            import tempfile
            from PIL import Image

            imagen_data = await attachment.read()

            # Guardar en archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                tmp.write(imagen_data)
                ruta_temporal = tmp.name

            # Procesar OCR
            embed = discord.Embed(
                title="⏳ Procesando factura...",
                color=discord.Color.blue()
            )
            msg = await message.reply(embed=embed, mention_author=False)

            # Llamar a procesar_factura con await
            datos = await procesar_factura(ruta_temporal)

            if 'error' not in datos:
                # Crear gasto
                gasto = GastoRepository.crear_gasto(
                    usuario_id=message.author.id,
                    descripcion=datos.get('descripcion', 'Factura'),
                    monto=datos.get('monto_total', 0),
                    categoria=datos.get('categoria', 'Otros'),
                    imagen_url=attachment.url,
                    datos_ocr=datos
                )

                # Mostrar éxito
                embed_exito = discord.Embed(
                    title=f"✅ Gasto registrado (ID: {gasto.id})",
                    description=f"**S/. {gasto.monto:.2f}**\n{gasto.descripcion}",
                    color=discord.Color.green()
                )

                embed_exito.add_field(
                    name="📁 CATEGORIA",
                    value=gasto.categoria,
                    inline=True
                )

                embed_exito.add_field(
                    name="📅 FECHA",
                    value=gasto.fecha,
                    inline=True
                )

                await msg.edit(embed=embed_exito)
                logger.info(f"✅ Factura procesada exitosamente - ID: {gasto.id}")

            else:
                # Error en OCR
                embed_error = DiscordService.crear_embed_error(
                    "Error procesando factura",
                    datos['error']
                )
                await msg.edit(embed=embed_error)
                logger.error(f"❌ Error en OCR: {datos['error']}")

        except Exception as e:
            # Usar manejador centralizado de excepciones
            resultado = ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Procesamiento de factura",
                datos_adicionales={
                    'Usuario': str(message.author),
                    'Archivo': attachment.filename,
                    'Tamaño': f"{len(imagen_data)} bytes" if 'imagen_data' in locals() else 'N/A'
                }
            )

            # Enviar embed de error a Discord
            embed_error = resultado['embed']
            await message.reply(embed=embed_error, mention_author=False)

