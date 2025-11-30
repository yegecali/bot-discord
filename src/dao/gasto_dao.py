"""
DAO (Data Access Object) para Gasto
Operaciones CRUD básicas sin lógica de negocio
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from src.models import Gasto, SessionLocal


class GastoDAO:
    """Data Access Object para operaciones CRUD de Gasto"""

    @staticmethod
    def crear(db: Session, usuario_id: int, descripcion: str, monto: float,
              categoria: str = 'Otros', imagen_url: str = None, datos_ocr: dict = None) -> Gasto:
        """Inserta un nuevo gasto"""
        fecha = datetime.now().strftime('%Y-%m-%d')
        gasto = Gasto(
            usuario_id=usuario_id,
            descripcion=descripcion,
            monto=monto,
            categoria=categoria,
            fecha=fecha,
            imagen_url=imagen_url,
            datos_ocr=datos_ocr
        )
        db.add(gasto)
        db.commit()
        db.refresh(gasto)
        return gasto

    @staticmethod
    def obtener_por_id(db: Session, gasto_id: int) -> Gasto:
        """Obtiene un gasto por ID"""
        return db.query(Gasto).filter(Gasto.id == gasto_id).first()

    @staticmethod
    def obtener_todos(db: Session, usuario_id: int = None) -> list:
        """Obtiene todos los gastos, opcionalmente filtrados por usuario"""
        query = db.query(Gasto)
        if usuario_id:
            query = query.filter(Gasto.usuario_id == usuario_id)
        return query.order_by(desc(Gasto.fecha)).all()

    @staticmethod
    def obtener_por_rango_fechas(db: Session, usuario_id: int, dias: int = 30) -> list:
        """Obtiene gastos de los últimos N días"""
        fecha_limite = datetime.now() - timedelta(days=dias)
        return db.query(Gasto).filter(
            Gasto.usuario_id == usuario_id,
            Gasto.timestamp >= fecha_limite
        ).order_by(desc(Gasto.fecha)).all()

    @staticmethod
    def actualizar(db: Session, gasto_id: int, **kwargs) -> Gasto:
        """Actualiza un gasto existente"""
        gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
        if gasto:
            for key, value in kwargs.items():
                if hasattr(gasto, key):
                    setattr(gasto, key, value)
            db.commit()
            db.refresh(gasto)
        return gasto

    @staticmethod
    def eliminar(db: Session, gasto_id: int) -> bool:
        """Elimina un gasto"""
        gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
        if gasto:
            db.delete(gasto)
            db.commit()
            return True
        return False

    @staticmethod
    def contar_por_usuario(db: Session, usuario_id: int, dias: int = 30) -> int:
        """Cuenta gastos de un usuario"""
        fecha_limite = datetime.now() - timedelta(days=dias)
        return db.query(Gasto).filter(
            Gasto.usuario_id == usuario_id,
            Gasto.timestamp >= fecha_limite
        ).count()

    @staticmethod
    def suma_total(db: Session, usuario_id: int, dias: int = 30) -> float:
        """Suma total de gastos de un usuario"""
        fecha_limite = datetime.now() - timedelta(days=dias)
        resultado = db.query(func.sum(Gasto.monto)).filter(
            Gasto.usuario_id == usuario_id,
            Gasto.timestamp >= fecha_limite
        ).scalar()
        return float(resultado or 0.0)

    @staticmethod
    def agrupar_por_categoria(db: Session, usuario_id: int, dias: int = 30) -> list:
        """Agrupa gastos por categoría"""
        fecha_limite = datetime.now() - timedelta(days=dias)
        return db.query(
            Gasto.categoria,
            func.sum(Gasto.monto).label('total'),
            func.count(Gasto.id).label('cantidad')
        ).filter(
            Gasto.usuario_id == usuario_id,
            Gasto.timestamp >= fecha_limite
        ).group_by(Gasto.categoria).order_by(desc('total')).all()

