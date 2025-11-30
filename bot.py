import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pytesseract
from database import registrar_gasto, obtener_gastos_usuario, obtener_total_gastos, obtener_gastos_por_categoria, eliminar_gasto
from factura_processor import procesar_factura, descargar_imagen

# IMPORTANTE: La configuración de pytesseract se hace en factura_processor.py
# No configurar aquí para evitar conflictos

# Cargar variables de entorno
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Crear instancia del bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento: Bot listo
@bot.event
async def on_ready():
    print(f'{bot.user} ha iniciado sesión')
    print(f'Bot conectado a Discord')
    print('------')

# Evento: Mensaje nuevo
@bot.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == bot.user:
        return

    # Procesar imágenes de facturas
    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                await procesar_imagen_factura(message, attachment)

    # Responder a menciones
    if bot.user.mentioned_in(message):
        await message.channel.send(f'¡Hola {message.author}! Soy un bot de Discord 🤖')

    # Procesar comandos
    await bot.process_commands(message)

async def procesar_imagen_factura(message, attachment):
    """Procesa una imagen de factura enviada por el usuario"""
    print(f"\n[BOT DEBUG] ===== INICIO PROCESAMIENTO DE FACTURA =====")
    print(f"[BOT DEBUG] Usuario: {message.author}")
    print(f"[BOT DEBUG] Archivo: {attachment.filename}")
    print(f"[BOT DEBUG] URL: {attachment.url}")
    try:
        # Indicador de procesamiento
        async with message.channel.typing():
            print(f"[BOT DEBUG] Enviando indicador de escritura...")

            # Descargar imagen
            print(f"[BOT DEBUG] Iniciando descarga de imagen...")
            imagen_path = await descargar_imagen(attachment.url)
            if not imagen_path:
                print(f"[BOT DEBUG] ❌ Falló descarga de imagen")
                await message.reply('❌ No pude descargar la imagen. Intenta de nuevo.')
                return

            print(f"[BOT DEBUG] ✅ Imagen descargada: {imagen_path}")

            # Procesar factura
            print(f"[BOT DEBUG] Iniciando procesamiento de factura...")
            datos = await procesar_factura(imagen_path)
            print(f"[BOT DEBUG] Resultado del procesamiento: {datos}")

            if 'error' in datos:
                print(f"[BOT DEBUG] ❌ Error en procesamiento: {datos.get('error')}")
                embed = discord.Embed(
                    title='❌ Error procesando factura',
                    description=datos.get('error'),
                    color=discord.Color.red()
                )
                await message.reply(embed=embed)
                return

            # Validar datos
            monto = datos.get('monto_total')
            if not monto:
                print(f"[BOT DEBUG] ⚠️ No se encontró monto total")
                await message.reply('❌ No pude extraer el monto total de la factura.')
                return

            print(f"[BOT DEBUG] ✅ Monto validado: {monto}")

            # Registrar en base de datos
            descripcion = datos.get('descripción', f'Factura de {datos.get("vendedor", "comercio")}')
            categoria = datos.get('categoría', 'Otros')

            print(f"[BOT DEBUG] Registrando gasto en base de datos...")
            print(f"[BOT DEBUG] - Usuario ID: {message.author.id}")
            print(f"[BOT DEBUG] - Monto: {monto}")
            print(f"[BOT DEBUG] - Descripción: {descripcion}")
            print(f"[BOT DEBUG] - Categoría: {categoria}")

            gasto_id = registrar_gasto(
                usuario_id=message.author.id,
                descripcion=descripcion,
                monto=monto,
                categoria=categoria,
                imagen_url=attachment.url,
                datos_ocr=datos
            )

            print(f"[BOT DEBUG] ✅ Gasto registrado con ID: {gasto_id}")

            # Crear respuesta
            embed = discord.Embed(
                title='✅ Gasto registrado correctamente',
                description=f'Factura #{gasto_id}',
                color=discord.Color.green()
            )
            moneda = datos.get('moneda', 'S/.')
            embed.add_field(name='💰 Monto', value=f'{moneda} {monto:.2f}', inline=False)
            embed.add_field(name='📝 Descripción', value=descripcion, inline=False)
            embed.add_field(name='🏷️ Categoría', value=categoria, inline=False)
            embed.add_field(name='🏪 Vendedor', value=datos.get('vendedor', 'N/A'), inline=False)

            if datos.get('items'):
                items_text = '\n'.join([f'• {item}' for item in datos['items'][:5]])
                if len(datos['items']) > 5:
                    items_text += f'\n• ... y {len(datos["items"]) - 5} más'
                embed.add_field(name='🛒 Artículos', value=items_text, inline=False)

            print(f"[BOT DEBUG] Enviando respuesta al usuario...")
            await message.reply(embed=embed)
            print(f"[BOT DEBUG] ✅ ===== PROCESAMIENTO COMPLETADO =====\n")

    except Exception as e:
        print(f'[BOT DEBUG] ❌ Error procesando factura: {e}')
        print(f"[BOT DEBUG] Tipo de error: {type(e).__name__}")
        import traceback
        print(f"[BOT DEBUG] Traceback:")
        print(traceback.format_exc())
        await message.reply(f'❌ Error: {str(e)}')


# Comando: ping
@bot.command(name='ping')
async def ping(ctx):
    """Comando que responde con pong"""
    latencia = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latencia: {latencia}ms')

# Comando: hola
@bot.command(name='hola')
async def hola(ctx):
    """Comando que saluda al usuario"""
    await ctx.send(f'¡Hola {ctx.author}! 👋')

# Comando: info
@bot.command(name='info')
async def info(ctx):
    """Comando que muestra información del usuario"""
    embed = discord.Embed(
        title='Información del usuario',
        description=f'Información de {ctx.author}',
        color=discord.Color.blue()
    )
    embed.add_field(name='Nombre', value=ctx.author.mention, inline=False)
    embed.add_field(name='ID', value=ctx.author.id, inline=False)
    embed.add_field(name='Cuenta creada', value=ctx.author.created_at.strftime('%d/%m/%Y'), inline=False)
    embed.set_thumbnail(url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

# Comando: canales disponibles
@bot.command(name='canales')
async def canales(ctx):
    """Comando que muestra los canales disponibles del servidor"""
    guild = ctx.guild

    # Separar canales por tipo
    text_channels = [ch for ch in guild.channels if isinstance(ch, discord.TextChannel)]
    voice_channels = [ch for ch in guild.channels if isinstance(ch, discord.VoiceChannel)]

    # Crear embed para canales de texto
    embed = discord.Embed(
        title=f'Canales de {guild.name}',
        description='Lista de canales disponibles:',
        color=discord.Color.purple()
    )

    # Agregar canales de texto
    if text_channels:
        canal_list = '\n'.join([f'💬 {ch.mention}' for ch in text_channels])
        embed.add_field(name='Canales de Texto', value=canal_list, inline=False)

    # Agregar canales de voz
    if voice_channels:
        canal_list = '\n'.join([f'🎤 {ch.name}' for ch in voice_channels])
        embed.add_field(name='Canales de Voz', value=canal_list, inline=False)

    # Información del servidor
    embed.add_field(name='Total de Canales', value=f'{len(guild.channels)}', inline=True)
    embed.add_field(name='Miembros', value=f'{guild.member_count}', inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

    await ctx.send(embed=embed)

# Comando: Ver gastos
@bot.command(name='gastos')
async def ver_gastos(ctx, dias: int = 30):
    """Ver tus gastos de los últimos días"""
    gastos = obtener_gastos_usuario(ctx.author.id, dias)

    if not gastos:
        await ctx.send(f'📊 No tienes gastos registrados en los últimos {dias} días.')
        return

    embed = discord.Embed(
        title=f'📊 Tus gastos (últimos {dias} días)',
        description=f'Total de registros: {len(gastos)}',
        color=discord.Color.blue()
    )

    for gasto in gastos[:10]:  # Mostrar últimos 10
        gasto_id, descripcion, monto, categoria, fecha, timestamp = gasto
        embed.add_field(
            name=f'{categoria} - {fecha}',
            value=f'**S/. {monto:.2f}** - {descripcion}',
            inline=False
        )

    if len(gastos) > 10:
        embed.set_footer(text=f'... y {len(gastos) - 10} más')

    await ctx.send(embed=embed)

# Comando: Total de gastos
@bot.command(name='total')
async def total_gastos(ctx, dias: int = 30):
    """Ver el total de tus gastos"""
    total = obtener_total_gastos(ctx.author.id, dias)
    gastos = obtener_gastos_usuario(ctx.author.id, dias)

    embed = discord.Embed(
        title='💰 Resumen de Gastos',
        color=discord.Color.gold()
    )
    embed.add_field(name=f'Total (últimos {dias} días)', value=f'**S/. {total:.2f}**', inline=False)
    embed.add_field(name='Número de transacciones', value=f'{len(gastos)}', inline=False)

    if len(gastos) > 0:
        promedio = total / len(gastos)
        embed.add_field(name='Promedio por transacción', value=f'${promedio:.2f}', inline=False)

    await ctx.send(embed=embed)

# Comando: Gastos por categoría
@bot.command(name='categorias')
async def gastos_por_categoria(ctx, dias: int = 30):
    """Ver gastos agrupados por categoría"""
    categorias = obtener_gastos_por_categoria(ctx.author.id, dias)

    if not categorias:
        await ctx.send('📊 No tienes gastos registrados.')
        return

    embed = discord.Embed(
        title=f'📊 Gastos por Categoría (últimos {dias} días)',
        color=discord.Color.purple()
    )

    total_general = 0
    for categoria, total, cantidad in categorias:
        emoji = {
            'alimentación': '🍔',
            'transporte': '🚗',
            'servicios': '🔧',
            'electrónica': '💻',
            'entretenimiento': '🎮',
            'salud': '🏥',
            'otros': '📦'
        }.get(categoria.lower(), '📦')

        embed.add_field(
            name=f'{emoji} {categoria}',
            value=f'S/. {total:.2f} ({cantidad} compras)',
            inline=False
        )
        total_general += total

    embed.set_footer(text=f'Total: S/. {total_general:.2f}')
    await ctx.send(embed=embed)

# Comando: ayuda personalizada
@bot.command(name='ayuda')
async def ayuda(ctx):
    """Comando que muestra la ayuda del bot"""
    embed = discord.Embed(
        title='Comandos disponibles',
        description='Lista de comandos que puedes usar:',
        color=discord.Color.green()
    )
    embed.add_field(name='📋 Generales', value='!ping | !hola | !info | !canales', inline=False)
    embed.add_field(name='💰 Gastos', value='!gastos | !total | !categorias', inline=False)
    embed.add_field(name='📸 Facturas', value='Envía una imagen de factura para registrar gasto automáticamente', inline=False)
    embed.add_field(name='ℹ️ Ayuda', value='!ayuda', inline=False)

    await ctx.send(embed=embed)

# Ejecutar el bot
if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)

