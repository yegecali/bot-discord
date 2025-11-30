-- Script SQL para crear tablas de la base de datos de gastos
-- ============================================================

-- Tabla de gastos
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
);

-- Índices para optimizar búsquedas
CREATE INDEX IF NOT EXISTS idx_usuario_id ON gastos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_fecha ON gastos(fecha);
CREATE INDEX IF NOT EXISTS idx_categoria ON gastos(categoria);

