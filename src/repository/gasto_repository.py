"""
Repository para Gasto
Lógica de negocio reutilizable
"""
from src.models import SessionLocal
from src.dao import GastoDAO
from src.utils import get_logger
from src.config import ExceptionHandler

logger = get_logger(__name__)


class GastoRepository:
    """Repository con lógica de negocio para gastos"""

    @staticmethod
    def crear_gasto(usuario_id: int, descripcion: str, monto: float,
                    categoria: str = 'Otros', imagen_url: str = None,
                    datos_ocr: dict = None):
        """Crea un nuevo gasto"""
        db = SessionLocal()
        try:
            logger.info(f"📝 Creando gasto: {descripcion} - S/. {monto:.2f}")
            gasto = GastoDAO.crear(
                db, usuario_id, descripcion, monto, categoria, imagen_url, datos_ocr
            )
            logger.info(f"✅ Gasto creado con ID: {gasto.id}")
            return gasto
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Creando gasto",
                datos_adicionales={
                    'Usuario ID': usuario_id,
                    'Descripción': descripcion,
                    'Monto': f"S/. {monto:.2f}",
                    'Categoría': categoria
                }
            )
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def obtener_gasto(gasto_id: int):
        """Obtiene un gasto por ID"""
        db = SessionLocal()
        try:
            gasto = GastoDAO.obtener_por_id(db, gasto_id)
            if not gasto:
                logger.warning(f"⚠️ Gasto {gasto_id} no encontrado")
            return gasto
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Obteniendo gasto",
                datos_adicionales={'Gasto ID': gasto_id}
            )
            raise
        finally:
            db.close()

    @staticmethod
    def obtener_gastos_usuario(usuario_id: int, dias: int = 30) -> list:
        """Obtiene gastos de un usuario"""
        db = SessionLocal()
        try:
            gastos = GastoDAO.obtener_por_rango_fechas(db, usuario_id, dias)
            logger.info(f"📊 Se encontraron {len(gastos)} gastos")
            return gastos
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Obteniendo gastos del usuario",
                datos_adicionales={
                    'Usuario ID': usuario_id,
                    'Rango días': dias
                }
            )
            raise
        finally:
            db.close()

    @staticmethod
    def obtener_total_gastos(usuario_id: int, dias: int = 30) -> float:
        """Obtiene el total de gastos"""
        db = SessionLocal()
        try:
            total = GastoDAO.suma_total(db, usuario_id, dias)
            logger.info(f"💰 Total: S/. {total:.2f}")
            return total
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Calculando total de gastos",
                datos_adicionales={
                    'Usuario ID': usuario_id,
                    'Rango días': dias
                }
            )
            raise
        finally:
            db.close()

    @staticmethod
    def obtener_gastos_por_categoria(usuario_id: int, dias: int = 30) -> list:
        """Obtiene gastos agrupados por categoría"""
        db = SessionLocal()
        try:
            categorias = GastoDAO.agrupar_por_categoria(db, usuario_id, dias)
            logger.info(f"📈 Se encontraron {len(categorias)} categorías")
            return categorias
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Obteniendo gastos por categoría",
                datos_adicionales={
                    'Usuario ID': usuario_id,
                    'Rango días': dias
                }
            )
            raise
        finally:
            db.close()

    @staticmethod
    def actualizar_gasto(gasto_id: int, usuario_id: int, **kwargs):
        """Actualiza un gasto"""
        db = SessionLocal()
        try:
            gasto = GastoDAO.obtener_por_id(db, gasto_id)
            if gasto and gasto.usuario_id == usuario_id:
                gasto = GastoDAO.actualizar(db, gasto_id, **kwargs)
                logger.info(f"✅ Gasto {gasto_id} actualizado")
                return gasto
            return None
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Actualizando gasto",
                datos_adicionales={
                    'Gasto ID': gasto_id,
                    'Usuario ID': usuario_id,
                    'Campos': str(list(kwargs.keys()))
                }
            )
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def eliminar_gasto(gasto_id: int, usuario_id: int) -> bool:
        """Elimina un gasto"""
        db = SessionLocal()
        try:
            gasto = GastoDAO.obtener_por_id(db, gasto_id)
            if gasto and gasto.usuario_id == usuario_id:
                resultado = GastoDAO.eliminar(db, gasto_id)
                logger.info(f"✅ Gasto eliminado")
                return resultado
            return False
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Eliminando gasto",
                datos_adicionales={
                    'Gasto ID': gasto_id,
                    'Usuario ID': usuario_id
                }
            )
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def obtener_estadisticas(usuario_id: int, dias: int = 30) -> dict:
        """Obtiene estadísticas completas"""
        db = SessionLocal()
        try:
            gastos = GastoDAO.obtener_por_rango_fechas(db, usuario_id, dias)
            total = sum(g.monto for g in gastos)
            cantidad = len(gastos)
            promedio = total / cantidad if cantidad > 0 else 0
            categorias = GastoDAO.agrupar_por_categoria(db, usuario_id, dias)

            logger.info(f"📊 Estadísticas generadas")

            return {
                'total': total,
                'cantidad': cantidad,
                'promedio': promedio,
                'categorias': [
                    {
                        'nombre': cat[0],
                        'total': cat[1],
                        'cantidad': cat[2]
                    }
                    for cat in categorias
                ]
            }
        except Exception as e:
            ExceptionHandler.manejar_error(
                excepcion=e,
                contexto="Obteniendo estadísticas",
                datos_adicionales={
                    'Usuario ID': usuario_id,
                    'Rango días': dias
                }
            )
            raise
        finally:
            db.close()

