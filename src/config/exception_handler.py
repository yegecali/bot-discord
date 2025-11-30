"""
Manejador centralizado de excepciones
Gestiona errores con logging, embeds Discord y plantillas Markdown
"""
import traceback
import discord
from datetime import datetime
from typing import Optional, Dict, Any
from src.logger import get_logger

logger = get_logger(__name__)


class ExceptionHandler:
    """Manejador centralizado de excepciones con Discord y logging"""

    # Mapeo de tipos de error a emojis
    ERROR_EMOJIS = {
        'ValueError': '⚠️',
        'TypeError': '🔴',
        'KeyError': '🔑',
        'FileNotFoundError': '📁',
        'PermissionError': '🔒',
        'ConnectionError': '🌐',
        'TimeoutError': '⏱️',
        'Exception': '❌',
    }

    # Mapeo de tipos de error a colores Discord
    ERROR_COLORS = {
        'ValueError': discord.Color.orange(),
        'TypeError': discord.Color.red(),
        'KeyError': discord.Color.dark_orange(),
        'FileNotFoundError': discord.Color.dark_red(),
        'PermissionError': discord.Color.dark_red(),
        'ConnectionError': discord.Color.red(),
        'TimeoutError': discord.Color.orange(),
        'Exception': discord.Color.red(),
    }

    @classmethod
    def _obtener_emoji(cls, tipo_error: str) -> str:
        """Obtiene emoji para un tipo de error"""
        return cls.ERROR_EMOJIS.get(tipo_error, '❌')

    @classmethod
    def _obtener_color(cls, tipo_error: str) -> discord.Color:
        """Obtiene color para un tipo de error"""
        return cls.ERROR_COLORS.get(tipo_error, discord.Color.red())

    @classmethod
    def _extraer_info_error(cls, excepcion: Exception) -> Dict[str, Any]:
        """Extrae información detallada del error"""
        tipo_error = type(excepcion).__name__
        mensaje_error = str(excepcion)
        traceback_str = traceback.format_exc()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return {
            'tipo': tipo_error,
            'mensaje': mensaje_error,
            'traceback': traceback_str,
            'timestamp': timestamp,
            'emoji': cls._obtener_emoji(tipo_error),
            'color': cls._obtener_color(tipo_error),
        }

    @classmethod
    def log_error(cls, excepcion: Exception, contexto: str = "Error") -> Dict[str, Any]:
        """
        Registra un error en logs con información detallada

        Args:
            excepcion: Excepción capturada
            contexto: Contexto del error (ej: "Procesando factura")

        Returns:
            dict: Información del error extraída
        """
        info_error = cls._extraer_info_error(excepcion)

        logger.error(
            f"\n{'='*60}\n"
            f"🚨 ERROR: {contexto}\n"
            f"{'='*60}\n"
            f"Tipo: {info_error['tipo']}\n"
            f"Mensaje: {info_error['mensaje']}\n"
            f"Timestamp: {info_error['timestamp']}\n"
            f"{'='*60}\n"
            f"Traceback:\n{info_error['traceback']}\n"
            f"{'='*60}\n"
        )

        return info_error

    @classmethod
    def crear_embed_error(cls, excepcion: Exception, contexto: str = "Error",
                         datos_adicionales: Optional[Dict] = None) -> discord.Embed:
        """
        Crea un embed de Discord con información del error

        Args:
            excepcion: Excepción capturada
            contexto: Contexto del error
            datos_adicionales: Datos extra para mostrar

        Returns:
            discord.Embed: Embed configurado
        """
        info_error = cls._extraer_info_error(excepcion)

        embed = discord.Embed(
            title=f"{info_error['emoji']} ERROR - {contexto}",
            description=info_error['mensaje'],
            color=info_error['color'],
            timestamp=datetime.now()
        )

        # Información del error
        embed.add_field(
            name="🔴 Tipo de Error",
            value=f"`{info_error['tipo']}`",
            inline=True
        )

        embed.add_field(
            name="⏰ Hora",
            value=info_error['timestamp'],
            inline=True
        )

        # Datos adicionales si existen
        if datos_adicionales:
            for clave, valor in datos_adicionales.items():
                embed.add_field(
                    name=f"📌 {clave}",
                    value=f"`{str(valor)[:256]}`",
                    inline=False
                )

        # Traceback (primeras líneas)
        lineas_traceback = info_error['traceback'].split('\n')[-3:]
        traceback_resumido = '\n'.join(lineas_traceback).strip()
        if traceback_resumido:
            embed.add_field(
                name="📋 Últimas líneas del error",
                value=f"```\n{traceback_resumido[:1024]}\n```",
                inline=False
            )

        embed.set_footer(text="Sistema de manejo de errores centralizado")

        return embed

    @classmethod
    def manejar_error(cls, excepcion: Exception, contexto: str = "Error",
                     datos_adicionales: Optional[Dict] = None,
                     callback_discord=None) -> Dict[str, Any]:
        """
        Maneja un error de forma centralizada: logging + Discord

        Args:
            excepcion: Excepción capturada
            contexto: Contexto del error
            datos_adicionales: Datos extra para mostrar
            callback_discord: Función async para enviar embed a Discord

        Returns:
            dict: Información del error y embed
        """
        # Log en consola
        info_error = cls.log_error(excepcion, contexto)

        # Crear embed
        embed = cls.crear_embed_error(excepcion, contexto, datos_adicionales)

        # Retornar información
        return {
            'info_error': info_error,
            'embed': embed,
            'callback_discord': callback_discord
        }

    @classmethod
    def crear_plantilla_error_markdown(cls, excepcion: Exception, contexto: str = "Error",
                                       datos_adicionales: Optional[Dict] = None) -> str:
        """
        Crea una plantilla Markdown con información del error

        Args:
            excepcion: Excepción capturada
            contexto: Contexto del error
            datos_adicionales: Datos extra

        Returns:
            str: Markdown con información del error
        """
        from pathlib import Path
        from jinja2 import Template

        info_error = cls._extraer_info_error(excepcion)

        # Cargar plantilla Markdown
        template_path = Path(__file__).parent.parent / 'templates' / 'error.md'

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except FileNotFoundError:
            # Plantilla por defecto si no existe
            template_content = """# ❌ ERROR - {{ contexto }}

## 🔴 Tipo de Error
```
{{ tipo_error }}
```

## 💬 Mensaje
{{ mensaje }}

## ⏰ Información de Tiempo
**{{ timestamp }}**

{% if datos_adicionales %}
## 📊 Datos Adicionales
{% for clave, valor in datos_adicionales.items() %}
- **{{ clave }}:** `{{ valor }}`
{% endfor %}
{% endif %}

## 📋 Traceback Completo
```
{{ traceback }}
```

---
*Sistema de manejo de errores centralizado - BotPersonal*
"""

        # Compilar plantilla
        template = Template(template_content)

        # Renderizar con datos
        markdown_content = template.render(
            contexto=contexto,
            tipo_error=info_error['tipo'],
            mensaje=info_error['mensaje'],
            timestamp=info_error['timestamp'],
            traceback=info_error['traceback'],
            datos_adicionales=datos_adicionales or {}
        )

        return markdown_content


# Instancia global para usar en toda la app
exception_handler = ExceptionHandler()

