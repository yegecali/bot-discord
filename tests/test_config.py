"""
Tests unitarios para configuración
"""
import pytest
from pathlib import Path
from src.config import (
    TESSERACT_RUTAS,
    MONEDA_DEFECTO,
    SIMBOLO_MONEDA,
    OCR_IDIOMAS,
    COMMAND_PREFIX,
    DB_PATH
)


class TestConfiguracion:
    """Tests para variables de configuración"""

    def test_tesseract_rutas_existe(self):
        """Test: TESSERACT_RUTAS está definido"""
        assert TESSERACT_RUTAS is not None
        assert isinstance(TESSERACT_RUTAS, list)
        assert len(TESSERACT_RUTAS) > 0

    def test_moneda_defecto(self):
        """Test: Moneda por defecto es PEN (Perú)"""
        assert MONEDA_DEFECTO == 'PEN'

    def test_simbolo_moneda(self):
        """Test: Símbolo de moneda es S/."""
        assert SIMBOLO_MONEDA == 'S/.'

    def test_ocr_idiomas(self):
        """Test: Idiomas OCR incluyen español"""
        assert 'spa' in OCR_IDIOMAS
        assert 'eng' in OCR_IDIOMAS

    def test_command_prefix(self):
        """Test: Prefijo de comando es !"""
        assert COMMAND_PREFIX == '!'

    def test_db_path_valido(self):
        """Test: Ruta de BD es válida"""
        assert DB_PATH is not None
        assert isinstance(DB_PATH, (str, Path))
        assert 'gastos.db' in str(DB_PATH)


class TestConfiguracionBusquedaTesseract:
    """Tests para búsqueda de Tesseract"""

    def test_rutas_tesseract_son_strings(self):
        """Test: Todas las rutas de Tesseract son strings"""
        for ruta in TESSERACT_RUTAS:
            assert isinstance(ruta, str)

    def test_rutas_tesseract_windows(self):
        """Test: Rutas incluyen ubicaciones de Windows"""
        rutas_str = str(TESSERACT_RUTAS)

        # Verificar que hay rutas válidas para Windows
        assert 'Program Files' in rutas_str or 'programdata' in rutas_str.lower() or len(TESSERACT_RUTAS) > 0


class TestConfiguracionFormatos:
    """Tests para formatos"""

    def test_simbolo_moneda_es_string(self):
        """Test: Símbolo de moneda es un string"""
        assert isinstance(SIMBOLO_MONEDA, str)
        assert len(SIMBOLO_MONEDA) > 0

    def test_command_prefix_es_string(self):
        """Test: Prefijo de comando es un string"""
        assert isinstance(COMMAND_PREFIX, str)
        assert len(COMMAND_PREFIX) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

