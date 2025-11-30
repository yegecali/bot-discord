"""
Modelo de Gasto
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Index
from datetime import datetime
from .base import Base


class Gasto(Base):
    """Modelo de tabla gastos"""
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False, index=True)
    descripcion = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    categoria = Column(String, default='Otros')
    fecha = Column(String, nullable=False)
    imagen_url = Column(String, nullable=True)
    datos_ocr = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Índices
    __table_args__ = (
        Index('idx_usuario_id', 'usuario_id'),
        Index('idx_fecha', 'fecha'),
        Index('idx_categoria', 'categoria'),
    )

    def __repr__(self):
        return f"<Gasto(id={self.id}, usuario_id={self.usuario_id}, monto={self.monto}, fecha={self.fecha})>"

    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'descripcion': self.descripcion,
            'monto': self.monto,
            'categoria': self.categoria,
            'fecha': self.fecha,
            'imagen_url': self.imagen_url,
            'datos_ocr': self.datos_ocr,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

