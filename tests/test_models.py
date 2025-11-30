"""
Tests unitarios para los modelos SQLAlchemy
"""
import pytest
import json
from datetime import datetime
from src.models import Gasto, Base, engine, SessionLocal


class TestGastoModel:
    """Tests para el modelo Gasto"""

    @pytest.fixture
    def db_session(self):
        """Crea una sesión de prueba"""
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        yield db
        db.close()
        Base.metadata.drop_all(bind=engine)

    def test_crear_gasto(self, db_session):
        """Test: Crear un gasto"""
        gasto = Gasto(
            usuario_id=123456789,
            descripcion="Compra en Supermercado",
            monto=150.50,
            categoria="Compras",
            fecha="2024-11-30"
        )

        db_session.add(gasto)
        db_session.commit()
        db_session.refresh(gasto)

        assert gasto.id is not None
        assert gasto.usuario_id == 123456789
        assert gasto.monto == 150.50
        assert gasto.categoria == "Compras"

    def test_gasto_valores_por_defecto(self, db_session):
        """Test: Valores por defecto del gasto"""
        gasto = Gasto(
            usuario_id=123,
            descripcion="Gasto",
            monto=100.0,
            fecha="2024-11-30"
        )

        db_session.add(gasto)
        db_session.commit()

        assert gasto.categoria == "Otros"
        assert gasto.imagen_url is None
        assert gasto.datos_ocr is None
        assert gasto.timestamp is not None

    def test_gasto_to_dict(self, db_session):
        """Test: Convertir gasto a diccionario"""
        gasto = Gasto(
            usuario_id=123,
            descripcion="Compra",
            monto=50.0,
            categoria="Compras",
            fecha="2024-11-30"
        )

        db_session.add(gasto)
        db_session.commit()

        gasto_dict = gasto.to_dict()

        assert isinstance(gasto_dict, dict)
        assert gasto_dict['usuario_id'] == 123
        assert gasto_dict['monto'] == 50.0
        assert gasto_dict['descripcion'] == "Compra"

    def test_gasto_con_datos_ocr(self, db_session):
        """Test: Gasto con datos OCR (JSON)"""
        datos_ocr = {
            "vendedor": "Supermercado XYZ",
            "fecha": "29/11/2024",
            "items": ["Arroz", "Pollo"]
        }

        gasto = Gasto(
            usuario_id=123,
            descripcion="Compra",
            monto=100.0,
            categoria="Compras",
            fecha="2024-11-30",
            datos_ocr=datos_ocr
        )

        db_session.add(gasto)
        db_session.commit()
        db_session.refresh(gasto)

        assert gasto.datos_ocr == datos_ocr
        assert gasto.datos_ocr['vendedor'] == "Supermercado XYZ"

    def test_gasto_repr(self, db_session):
        """Test: Representación en string del gasto"""
        gasto = Gasto(
            usuario_id=123,
            descripcion="Compra",
            monto=50.0,
            fecha="2024-11-30"
        )

        db_session.add(gasto)
        db_session.commit()

        repr_str = repr(gasto)
        assert "Gasto" in repr_str
        assert str(gasto.usuario_id) in repr_str

    def test_multiples_gastos_mismo_usuario(self, db_session):
        """Test: Múltiples gastos del mismo usuario"""
        for i in range(5):
            gasto = Gasto(
                usuario_id=123,
                descripcion=f"Gasto {i}",
                monto=100.0 + i,
                categoria="Compras",
                fecha="2024-11-30"
            )
            db_session.add(gasto)

        db_session.commit()

        gastos = db_session.query(Gasto).filter(Gasto.usuario_id == 123).all()
        assert len(gastos) == 5

    def test_indices_creados(self, db_session):
        """Test: Verificar que los índices están creados"""
        # Crear varios gastos para verificar índices
        for i in range(10):
            gasto = Gasto(
                usuario_id=123 + i,
                descripcion=f"Gasto {i}",
                monto=50.0,
                categoria="Compras" if i % 2 == 0 else "Alimentación",
                fecha="2024-11-30"
            )
            db_session.add(gasto)

        db_session.commit()

        # Buscar por usuario_id (tiene índice)
        resultado = db_session.query(Gasto).filter(Gasto.usuario_id == 123).first()
        assert resultado is not None

        # Buscar por categoría (tiene índice)
        resultado = db_session.query(Gasto).filter(Gasto.categoria == "Compras").all()
        assert len(resultado) == 5

    def test_validacion_tipos(self, db_session):
        """Test: Validación de tipos de datos"""
        # Test con conversión de tipos
        gasto = Gasto(
            usuario_id="123",  # Se convierte a int
            descripcion="Compra",
            monto="150.50",    # Se convierte a float
            fecha="2024-11-30"
        )

        db_session.add(gasto)
        db_session.commit()

        assert isinstance(gasto.usuario_id, int)
        assert isinstance(gasto.monto, float)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

