import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Base de datos
DB_PATH = Path('gastos.db')

def init_database():
    """Inicializa la base de datos de gastos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL,
            categoria TEXT,
            fecha TEXT NOT NULL,
            imagen_url TEXT,
            datos_ocr TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def registrar_gasto(usuario_id, descripcion, monto, categoria='Otros', imagen_url=None, datos_ocr=None):
    """Registra un nuevo gasto"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    fecha = datetime.now().strftime('%Y-%m-%d')
    datos_ocr_json = json.dumps(datos_ocr) if datos_ocr else None

    cursor.execute('''
        INSERT INTO gastos (usuario_id, descripcion, monto, categoria, fecha, imagen_url, datos_ocr)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (usuario_id, descripcion, monto, categoria, fecha, imagen_url, datos_ocr_json))

    conn.commit()
    gasto_id = cursor.lastrowid
    conn.close()

    return gasto_id

def obtener_gastos_usuario(usuario_id, dias=30):
    """Obtiene los gastos del usuario de los últimos días"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, descripcion, monto, categoria, fecha, timestamp
        FROM gastos
        WHERE usuario_id = ?
        ORDER BY fecha DESC
        LIMIT ?
    ''', (usuario_id, dias))

    gastos = cursor.fetchall()
    conn.close()

    return gastos

def obtener_total_gastos(usuario_id, dias=30):
    """Obtiene el total de gastos del usuario"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT SUM(monto) as total
        FROM gastos
        WHERE usuario_id = ? AND datetime(timestamp) >= datetime('now', '-' || ? || ' days')
    ''', (usuario_id, dias))

    result = cursor.fetchone()
    conn.close()

    return result[0] or 0.0

def obtener_gastos_por_categoria(usuario_id, dias=30):
    """Obtiene gastos agrupados por categoría"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT categoria, SUM(monto) as total, COUNT(*) as cantidad
        FROM gastos
        WHERE usuario_id = ? AND datetime(timestamp) >= datetime('now', '-' || ? || ' days')
        GROUP BY categoria
        ORDER BY total DESC
    ''', (usuario_id, dias))

    resultados = cursor.fetchall()
    conn.close()

    return resultados

def eliminar_gasto(gasto_id, usuario_id):
    """Elimina un gasto del usuario"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM gastos
        WHERE id = ? AND usuario_id = ?
    ''', (gasto_id, usuario_id))

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    return affected > 0

# Inicializar base de datos
init_database()

