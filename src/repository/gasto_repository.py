"""
Repository para Gasto
Lógica de negocio reutilizable
"""
from src.models import SessionLocal
from src.dao import GastoDAO


class GastoRepository:
    """Repository con lógica de negocio para gastos"""

    @staticmethod
    def crear_gasto(usuario_id: int, descripcion: str, monto: float,
                    categoria: str = 'Otros', imagen_url: str = None,
                    datos_ocr: dict = None):
        """Crea un nuevo gasto"""
        db = SessionLocal()
        try:
            print(f"[REPOSITORY] 📝 Creando gasto: {descripcion} - S/. {monto:.2f}")
            gasto = GastoDAO.crear(
                db, usuario_id, descripcion, monto, categoria, imagen_url, datos_ocr
            )
            print(f"[REPOSITORY] ✅ Gasto creado con ID: {gasto.id}")
            return gasto
        except Exception as e:
            print(f"[REPOSITORY] ❌ Error creando gasto: {e}")
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
                print(f"[REPOSITORY] ⚠️ Gasto {gasto_id} no encontrado")
            return gasto
        finally:
            db.close()

    @staticmethod
    def obtener_gastos_usuario(usuario_id: int, dias: int = 30) -> list:
        """Obtiene gastos de un usuario"""
        db = SessionLocal()
        try:
            gastos = GastoDAO.obtener_por_rango_fechas(db, usuario_id, dias)
            print(f"[REPOSITORY] 📊 Se encontraron {len(gastos)} gastos")
            return gastos
        finally:
            db.close()

    @staticmethod
    def obtener_total_gastos(usuario_id: int, dias: int = 30) -> float:
        """Obtiene el total de gastos"""
        db = SessionLocal()
        try:
            total = GastoDAO.suma_total(db, usuario_id, dias)
            print(f"[REPOSITORY] 💰 Total: S/. {total:.2f}")
            return total
        finally:
            db.close()

    @staticmethod
    def obtener_gastos_por_categoria(usuario_id: int, dias: int = 30) -> list:
        """Obtiene gastos agrupados por categoría"""
        db = SessionLocal()
        try:
            categorias = GastoDAO.agrupar_por_categoria(db, usuario_id, dias)
            print(f"[REPOSITORY] 📈 Se encontraron {len(categorias)} categorías")
            return categorias
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
                print(f"[REPOSITORY] ✅ Gasto {gasto_id} actualizado")
                return gasto
            return None
        except Exception as e:
            print(f"[REPOSITORY] ❌ Error actualizando: {e}")
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
                print(f"[REPOSITORY] ✅ Gasto eliminado")
                return resultado
            return False
        except Exception as e:
            print(f"[REPOSITORY] ❌ Error eliminando: {e}")
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

            print(f"[REPOSITORY] 📊 Estadísticas generadas")

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
        finally:
            db.close()

