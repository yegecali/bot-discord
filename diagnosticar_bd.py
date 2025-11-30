"""
Script de diagnóstico para la base de datos
Verifica si la BD se está borrando y por qué
"""
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from src.config import DB_PATH
from src.models import SessionLocal, Gasto

def diagnosticar_bd():
    """Diagnóstico completo de la BD"""
    print("\n" + "="*60)
    print("DIAGNÓSTICO DE BASE DE DATOS")
    print("="*60)

    # 1. Verificar si archivo existe
    print(f"\n[1] Verificando archivo: {DB_PATH}")
    if Path(DB_PATH).exists():
        size = Path(DB_PATH).stat().st_size
        mtime = datetime.fromtimestamp(Path(DB_PATH).stat().st_mtime)
        print(f"    ✅ EXISTE")
        print(f"    📊 Tamaño: {size} bytes")
        print(f"    📅 Última modificación: {mtime}")
    else:
        print(f"    ❌ NO EXISTE")
        return

    # 2. Verificar conexión SQLite
    print(f"\n[2] Verificando conexión SQLite")
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Listar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"    ✅ Conexión OK")
        print(f"    📋 Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"       - {table[0]}")

        # Contar registros en gastos
        cursor.execute("SELECT COUNT(*) FROM gastos")
        count = cursor.fetchone()[0]
        print(f"    📊 Registros en 'gastos': {count}")

        conn.close()
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return

    # 3. Verificar con SQLAlchemy
    print(f"\n[3] Verificando con SQLAlchemy")
    try:
        db = SessionLocal()
        count = db.query(Gasto).count()
        print(f"    ✅ Conexión OK")
        print(f"    📊 Gastos registrados: {count}")

        if count > 0:
            ultimos = db.query(Gasto).order_by(Gasto.id.desc()).limit(3).all()
            print(f"    📝 Últimos 3 gastos:")
            for g in ultimos:
                print(f"       ID: {g.id}, Monto: S/. {g.monto}, Fecha: {g.fecha}")

        db.close()
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return

    # 4. Verificar permisos
    print(f"\n[4] Verificando permisos")
    try:
        if os.access(DB_PATH, os.R_OK):
            print(f"    ✅ Lectura: OK")
        else:
            print(f"    ❌ Lectura: DENEGADA")

        if os.access(DB_PATH, os.W_OK):
            print(f"    ✅ Escritura: OK")
        else:
            print(f"    ❌ Escritura: DENEGADA")
    except Exception as e:
        print(f"    ❌ Error: {e}")

    print("\n" + "="*60)


if __name__ == '__main__':
    diagnosticar_bd()

