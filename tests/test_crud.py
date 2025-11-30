"""
Tests unitarios para operaciones CRUD
"""
import pytest
from datetime import datetime, timedelta
from src.models import Base, engine, SessionLocal, Gasto
from src.crud import (
    crear_gasto,
    obtener_gasto,
    obtener_gastos_usuario,
    obtener_total_gastos,
    obtener_gastos_por_categoria,
    obtener_gastos_por_fecha,
    actualizar_gasto,
    eliminar_gasto,
    obtener_estadisticas
)


@pytest.fixture(scope="function")
def setup_db():
    """Setup y teardown de base de datos"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestCRUDCreate:
    """Tests para CREATE"""

    def test_crear_gasto_basico(self, setup_db):
        """Test: Crear un gasto básico"""
        gasto = crear_gasto(
            usuario_id=123456789,
            descripcion="Compra en Supermercado",
            monto=150.50,
            categoria="Compras"
        )

        assert gasto.id is not None
        assert gasto.usuario_id == 123456789
        assert gasto.monto == 150.50

    def test_crear_gasto_con_ocr(self, setup_db):
        """Test: Crear gasto con datos OCR"""
        datos_ocr = {"vendedor": "Tienda XYZ", "items": ["Arroz"]}

        gasto = crear_gasto(
            usuario_id=123,
            descripcion="Compra",
            monto=100.0,
            categoria="Compras",
            datos_ocr=datos_ocr
        )

        assert gasto.datos_ocr == datos_ocr

    def test_crear_gasto_categoria_por_defecto(self, setup_db):
        """Test: Categoría por defecto"""
        gasto = crear_gasto(
            usuario_id=123,
            descripcion="Compra",
            monto=100.0
        )

        assert gasto.categoria == "Otros"


class TestCRUDRead:
    """Tests para READ"""

    def test_obtener_gasto_por_id(self, setup_db):
        """Test: Obtener gasto por ID"""
        gasto_creado = crear_gasto(
            usuario_id=123,
            descripcion="Compra",
            monto=100.0
        )

        gasto = obtener_gasto(gasto_creado.id)

        assert gasto is not None
        assert gasto.id == gasto_creado.id
        assert gasto.monto == 100.0

    def test_obtener_gasto_no_existe(self, setup_db):
        """Test: Obtener gasto que no existe"""
        gasto = obtener_gasto(99999)
        assert gasto is None

    def test_obtener_gastos_usuario(self, setup_db):
        """Test: Obtener todos los gastos de un usuario"""
        usuario_id = 123

        # Crear 5 gastos
        for i in range(5):
            crear_gasto(
                usuario_id=usuario_id,
                descripcion=f"Gasto {i}",
                monto=100.0 + i
            )

        gastos = obtener_gastos_usuario(usuario_id)

        assert len(gastos) == 5

    def test_obtener_gastos_usuario_vacio(self, setup_db):
        """Test: Usuario sin gastos"""
        gastos = obtener_gastos_usuario(999)
        assert len(gastos) == 0

    def test_obtener_gastos_por_dias(self, setup_db):
        """Test: Filtrar por rango de días"""
        usuario_id = 123

        # Crear gastos
        for i in range(3):
            crear_gasto(
                usuario_id=usuario_id,
                descripcion=f"Gasto {i}",
                monto=100.0
            )

        gastos = obtener_gastos_usuario(usuario_id, dias=30)
        assert len(gastos) == 3

    def test_obtener_total_gastos(self, setup_db):
        """Test: Obtener total de gastos"""
        usuario_id = 123

        crear_gasto(usuario_id=usuario_id, descripcion="G1", monto=100.0)
        crear_gasto(usuario_id=usuario_id, descripcion="G2", monto=50.0)
        crear_gasto(usuario_id=usuario_id, descripcion="G3", monto=75.0)

        total = obtener_total_gastos(usuario_id)

        assert total == 225.0

    def test_obtener_gastos_por_categoria(self, setup_db):
        """Test: Agrupar gastos por categoría"""
        usuario_id = 123

        crear_gasto(usuario_id=usuario_id, descripcion="G1", monto=100.0, categoria="Compras")
        crear_gasto(usuario_id=usuario_id, descripcion="G2", monto=50.0, categoria="Compras")
        crear_gasto(usuario_id=usuario_id, descripcion="G3", monto=75.0, categoria="Alimentación")

        categorias = obtener_gastos_por_categoria(usuario_id)

        assert len(categorias) == 2

        # Verificar que el total está correcto
        compras = [c for c in categorias if c[0] == "Compras"][0]
        assert compras[1] == 150.0  # Total
        assert compras[2] == 2      # Cantidad

    def test_obtener_gastos_por_fecha(self, setup_db):
        """Test: Obtener gastos de una fecha específica"""
        usuario_id = 123
        fecha = "2024-11-30"

        crear_gasto(usuario_id=usuario_id, descripcion="G1", monto=100.0, fecha=fecha)
        crear_gasto(usuario_id=usuario_id, descripcion="G2", monto=50.0, fecha="2024-11-29")

        gastos = obtener_gastos_por_fecha(usuario_id, fecha)

        assert len(gastos) == 1
        assert gastos[0].monto == 100.0


class TestCRUDUpdate:
    """Tests para UPDATE"""

    def test_actualizar_gasto(self, setup_db):
        """Test: Actualizar un gasto"""
        gasto_creado = crear_gasto(
            usuario_id=123,
            descripcion="Original",
            monto=100.0,
            categoria="Compras"
        )

        gasto_actualizado = actualizar_gasto(
            gasto_id=gasto_creado.id,
            usuario_id=123,
            descripcion="Actualizado",
            categoria="Alimentación"
        )

        assert gasto_actualizado.descripcion == "Actualizado"
        assert gasto_actualizado.categoria == "Alimentación"
        assert gasto_actualizado.monto == 100.0  # Sin cambios

    def test_actualizar_gasto_usuario_incorrecto(self, setup_db):
        """Test: Actualizar gasto de otro usuario"""
        gasto = crear_gasto(usuario_id=123, descripcion="G", monto=100.0)

        gasto_actualizado = actualizar_gasto(
            gasto_id=gasto.id,
            usuario_id=999,  # Otro usuario
            descripcion="Nueva"
        )

        assert gasto_actualizado is None


class TestCRUDDelete:
    """Tests para DELETE"""

    def test_eliminar_gasto(self, setup_db):
        """Test: Eliminar un gasto"""
        gasto = crear_gasto(usuario_id=123, descripcion="G", monto=100.0)

        resultado = eliminar_gasto(gasto_id=gasto.id, usuario_id=123)

        assert resultado is True

        # Verificar que fue eliminado
        gasto_eliminado = obtener_gasto(gasto.id)
        assert gasto_eliminado is None

    def test_eliminar_gasto_no_existe(self, setup_db):
        """Test: Eliminar gasto que no existe"""
        resultado = eliminar_gasto(gasto_id=99999, usuario_id=123)
        assert resultado is False

    def test_eliminar_gasto_usuario_incorrecto(self, setup_db):
        """Test: Eliminar gasto de otro usuario"""
        gasto = crear_gasto(usuario_id=123, descripcion="G", monto=100.0)

        resultado = eliminar_gasto(gasto_id=gasto.id, usuario_id=999)

        assert resultado is False


class TestEstadisticas:
    """Tests para estadísticas"""

    def test_obtener_estadisticas_basicas(self, setup_db):
        """Test: Obtener estadísticas básicas"""
        usuario_id = 123

        crear_gasto(usuario_id=usuario_id, descripcion="G1", monto=100.0, categoria="Compras")
        crear_gasto(usuario_id=usuario_id, descripcion="G2", monto=50.0, categoria="Compras")
        crear_gasto(usuario_id=usuario_id, descripcion="G3", monto=75.0, categoria="Alimentación")

        stats = obtener_estadisticas(usuario_id)

        assert stats['total'] == 225.0
        assert stats['cantidad'] == 3
        assert stats['promedio'] == 75.0

    def test_obtener_estadisticas_por_categoria(self, setup_db):
        """Test: Estadísticas por categoría"""
        usuario_id = 123

        crear_gasto(usuario_id=usuario_id, descripcion="G1", monto=100.0, categoria="Compras")
        crear_gasto(usuario_id=usuario_id, descripcion="G2", monto=75.0, categoria="Alimentación")

        stats = obtener_estadisticas(usuario_id)

        assert len(stats['categorias']) == 2

        compras = [c for c in stats['categorias'] if c['nombre'] == 'Compras'][0]
        assert compras['total'] == 100.0
        assert compras['cantidad'] == 1


class TestIntegracion:
    """Tests de integración"""

    def test_flujo_completo(self, setup_db):
        """Test: Flujo completo CRUD"""
        usuario_id = 123

        # CREATE
        gasto1 = crear_gasto(
            usuario_id=usuario_id,
            descripcion="Compra 1",
            monto=100.0,
            categoria="Compras"
        )

        gasto2 = crear_gasto(
            usuario_id=usuario_id,
            descripcion="Compra 2",
            monto=50.0,
            categoria="Compras"
        )

        # READ
        gastos = obtener_gastos_usuario(usuario_id)
        assert len(gastos) == 2

        total = obtener_total_gastos(usuario_id)
        assert total == 150.0

        # UPDATE
        gasto1_actualizado = actualizar_gasto(
            gasto_id=gasto1.id,
            usuario_id=usuario_id,
            descripcion="Compra 1 actualizada"
        )
        assert gasto1_actualizado.descripcion == "Compra 1 actualizada"

        # DELETE
        resultado = eliminar_gasto(gasto_id=gasto2.id, usuario_id=usuario_id)
        assert resultado is True

        # Verificar final
        gastos_finales = obtener_gastos_usuario(usuario_id)
        assert len(gastos_finales) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

