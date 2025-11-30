"""
Utilidades Comunes
Funciones reutilizables en toda la aplicación
"""
import os
import re
import tempfile
import logging
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import discord

# ================================================================
# CONFIGURACIÓN DE LOGGING
# ================================================================

def get_logger(module_name: str):
    """
    Obtiene un logger configurado para un módulo

    Args:
        module_name (str): Nombre del módulo

    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(module_name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(f'[{module_name}] %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


# ================================================================
# MANEJO DE ARCHIVOS TEMPORALES
# ================================================================

def crear_archivo_temporal(contenido: bytes, sufijo: str = '.tmp') -> str:
    """
    Crea un archivo temporal con contenido

    Args:
        contenido (bytes): Contenido del archivo
        sufijo (str): Sufijo del archivo temporal

    Returns:
        str: Ruta del archivo temporal
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=sufijo) as tmp:
        tmp.write(contenido)
        return tmp.name


def limpiar_archivo_temporal(ruta: str) -> bool:
    """
    Elimina un archivo temporal si existe

    Args:
        ruta (str): Ruta del archivo

    Returns:
        bool: True si se eliminó, False si no existe o hay error
    """
    try:
        if os.path.exists(ruta):
            os.remove(ruta)
            return True
        return False
    except Exception as e:
        logging.error(f"Error limpiando archivo temporal {ruta}: {e}")
        return False


# ================================================================
# EXTRACCIÓN DE NÚMEROS Y PATRONES
# ================================================================

def extraer_numero(texto: str) -> Optional[float]:
    """
    Extrae el primer número decimal de un texto

    Args:
        texto (str): Texto a procesar

    Returns:
        Optional[float]: Número encontrado o None
    """
    numeros = re.findall(r'(\d+[.,]\d{2}|\d+)', texto)
    if numeros:
        try:
            numero_str = numeros[-1].replace(',', '.')
            return float(numero_str)
        except ValueError:
            pass
    return None


def extraer_numeros_multiples(texto: str) -> List[float]:
    """
    Extrae múltiples números decimales de un texto

    Args:
        texto (str): Texto a procesar

    Returns:
        List[float]: Lista de números encontrados
    """
    numeros = re.findall(r'(\d+[.,]\d{2})', texto)
    resultado = []
    for num_str in numeros:
        try:
            resultado.append(float(num_str.replace(',', '.')))
        except ValueError:
            pass
    return resultado


def buscar_palabra_clave(lineas: List[str], palabras_clave: List[str],
                         retornar_indice: bool = False) -> Tuple[Optional[str], Optional[int]]:
    """
    Busca una palabra clave en una lista de líneas

    Args:
        lineas (List[str]): Lista de líneas
        palabras_clave (List[str]): Palabras a buscar
        retornar_indice (bool): Si True, retorna también el índice

    Returns:
        Tuple[Optional[str], Optional[int]]: (línea encontrada, índice) o (None, None)
    """
    for idx, linea in enumerate(lineas):
        linea_lower = linea.lower()
        for palabra in palabras_clave:
            if palabra in linea_lower:
                if retornar_indice:
                    return linea, idx
                return linea, None
    return None, None


def buscar_patron_linea(lineas: List[str], patron: str,
                       retornar_indice: bool = False) -> Tuple[Optional[str], Optional[int]]:
    """
    Busca un patrón regex en líneas

    Args:
        lineas (List[str]): Lista de líneas
        patron (str): Patrón regex
        retornar_indice (bool): Si True, retorna también el índice

    Returns:
        Tuple[Optional[str], Optional[int]]: (línea encontrada, índice) o (None, None)
    """
    for idx, linea in enumerate(lineas):
        if re.search(patron, linea):
            if retornar_indice:
                return linea, idx
            return linea, None
    return None, None


# ================================================================
# MANEJO DE BASE DE DATOS
# ================================================================

def ejecutar_con_sesion_db(operacion, *args, **kwargs):
    """
    Ejecuta una operación con una sesión de DB automáticamente gestionada

    Args:
        operacion: Función que recibe (db, *args, **kwargs)
        *args: Argumentos posicionales
        **kwargs: Argumentos nombrados

    Returns:
        Resultado de la operación
    """
    from src.models import SessionLocal

    db = SessionLocal()
    try:
        return operacion(db, *args, **kwargs)
    finally:
        db.close()


# ================================================================
# EMBEDS DE DISCORD
# ================================================================

def crear_embed_error(titulo: str, descripcion: str, detalles: str = None) -> discord.Embed:
    """
    Crea un embed de error para Discord

    Args:
        titulo (str): Título del error
        descripcion (str): Descripción del error
        detalles (str): Detalles adicionales (opcional)

    Returns:
        discord.Embed: Embed configurado
    """
    embed = discord.Embed(
        title=f"❌ {titulo}",
        description=descripcion,
        color=discord.Color.red()
    )
    if detalles:
        embed.add_field(name="Detalles", value=detalles, inline=False)
    return embed


def crear_embed_exito(titulo: str, descripcion: str, detalles: str = None) -> discord.Embed:
    """
    Crea un embed de éxito para Discord

    Args:
        titulo (str): Título del éxito
        descripcion (str): Descripción del éxito
        detalles (str): Detalles adicionales (opcional)

    Returns:
        discord.Embed: Embed configurado
    """
    embed = discord.Embed(
        title=f"✅ {titulo}",
        description=descripcion,
        color=discord.Color.green()
    )
    if detalles:
        embed.add_field(name="Detalles", value=detalles, inline=False)
    return embed


def crear_embed_info(titulo: str, descripcion: str, color: discord.Color = None) -> discord.Embed:
    """
    Crea un embed de información para Discord

    Args:
        titulo (str): Título
        descripcion (str): Descripción
        color (discord.Color): Color del embed

    Returns:
        discord.Embed: Embed configurado
    """
    embed = discord.Embed(
        title=f"ℹ️ {titulo}",
        description=descripcion,
        color=color or discord.Color.blue()
    )
    return embed


def crear_embed_cargando(titulo: str, descripcion: str = "Procesando...") -> discord.Embed:
    """
    Crea un embed de estado "cargando"

    Args:
        titulo (str): Título
        descripcion (str): Descripción

    Returns:
        discord.Embed: Embed configurado
    """
    embed = discord.Embed(
        title=f"⏳ {titulo}",
        description=descripcion,
        color=discord.Color.blue()
    )
    return embed


# ================================================================
# VALIDACIÓN Y LIMPIEZA
# ================================================================

def limpiar_texto(texto: str) -> str:
    """
    Limpia un texto: elimina espacios extra y caracteres inválidos

    Args:
        texto (str): Texto a limpiar

    Returns:
        str: Texto limpio
    """
    # Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    # Eliminar saltos de línea múltiples
    texto = re.sub(r'\n\n+', '\n', texto)
    return texto.strip()


def normalizar_lineas(texto: str) -> List[str]:
    """
    Normaliza un texto en líneas limpias

    Args:
        texto (str): Texto a normalizar

    Returns:
        List[str]: Lista de líneas normalizadas
    """
    lineas = texto.split('\n')
    return [l.strip() for l in lineas if l.strip()]


def validar_ruta_archivo(ruta: str) -> bool:
    """
    Valida si una ruta de archivo existe y es accesible

    Args:
        ruta (str): Ruta del archivo

    Returns:
        bool: True si existe y es accesible
    """
    try:
        return os.path.exists(ruta) and os.path.isfile(ruta)
    except Exception:
        return False


# ================================================================
# MANEJO DE CONFIGURACIÓN
# ================================================================

def obtener_valor_config(diccionario: dict, clave: str,
                        valor_defecto=None, tipo=None):
    """
    Obtiene un valor de configuración con conversión de tipo

    Args:
        diccionario (dict): Diccionario de configuración
        clave (str): Clave a buscar
        valor_defecto: Valor por defecto
        tipo: Tipo a convertir (str, int, float, bool)

    Returns:
        Valor encontrado o valor por defecto
    """
    valor = diccionario.get(clave, valor_defecto)

    if valor is None:
        return valor_defecto

    if tipo:
        try:
            if tipo == bool:
                if isinstance(valor, str):
                    return valor.lower() in ('true', '1', 'yes', 'si', 'verdadero')
                return bool(valor)
            return tipo(valor)
        except (ValueError, TypeError):
            return valor_defecto

    return valor

