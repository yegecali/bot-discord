"""
Controlador de Eventos
Manejadores de eventos del bot
"""
import discord
from src.repository import GastoRepository
from src.factura_processor import procesar_factura
from src.services import GastoService, DiscordService


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
        print(f"[EVENTO] Bot conectado como {self.bot.user}")
        print(f"[EVENTO] Latencia: {round(self.bot.latency * 1000)}ms")

    async def on_message(self, message):
        """Procesar mensajes"""
        print(f"[EVENTO] Mensaje de {message.author}: {message.content}")

        # Ignorar mensajes del bot
        if message.author == self.bot.user:
            await self.bot.process_commands(message)
            return

        # Procesar imágenes (facturas)
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image/'):
                    print(f"[EVENTO] 📸 Imagen detectada: {attachment.filename}")
                    await self._procesar_factura(message, attachment)

        # Procesar comandos normales
        await self.bot.process_commands(message)

    async def _procesar_factura(self, message, attachment):
        """Procesa una factura"""
        print(f"[EVENTO] Procesando factura...")

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
                title="[WAIT] Procesando factura...",
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
                    title=f"[OK] Gasto registrado (ID: {gasto.id})",
                    description=f"**S/. {gasto.monto:.2f}**\n{gasto.descripcion}",
                    color=discord.Color.green()
                )

                embed_exito.add_field(
                    name="[CATEGORIA]",
                    value=gasto.categoria,
                    inline=True
                )

                embed_exito.add_field(
                    name="[FECHA]",
                    value=gasto.fecha,
                    inline=True
                )

                await msg.edit(embed=embed_exito)

            else:
                # Error en OCR
                embed_error = DiscordService.crear_embed_error(
                    "Error procesando factura",
                    datos['error']
                )
                await msg.edit(embed=embed_error)

        except Exception as e:
            print(f"[EVENTO] [ERROR] Error: {e}")
            embed_error = DiscordService.crear_embed_error(
                "Error",
                str(e)
            )
            await message.reply(embed=embed_error, mention_author=False)

