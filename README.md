# Bot Personal de Discord 🤖

Gestor de gastos con procesamiento automático de facturas usando OCR (Tesseract).

## 📋 Características

✅ **Procesamiento de Facturas**
- Extrae automáticamente montos, fechas y vendedor
- Utiliza OCR (Tesseract) para escanear imágenes
- Soporta múltiples formatos: PNG, JPG, JPEG, GIF, BMP

✅ **Gestión de Gastos**
- Registra gastos automáticamente en Soles (S/.)
- Base de datos SQLite para persistencia
- Organización por categorías

✅ **Reportes y Análisis**
- Ver gastos por rango de fechas
- Agrupación por categoría
- Cálculo de promedios
- Totales y subtotales

✅ **OAuth2 Integration**
- Servidor web Flask para autorización
- Callback automático de Discord
- Página de estado

## 📁 Estructura del Proyecto

```
BotPersonal/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuración centralizada
│   ├── bot.py                 # Bot principal de Discord
│   ├── database.py            # Gestión de base de datos
│   ├── factura_processor.py   # Procesamiento de facturas con OCR
│   ├── oauth_handler.py       # Manejo de OAuth2
│   └── web_server.py          # Servidor Flask
│
├── tests/
│   ├── __init__.py
│   ├── test_factura_processor.py
│   ├── test_database.py
│   └── test_tesseract.py
│
├── main.py                    # Punto de entrada
├── run_tests.py               # Ejecutor de tests
├── requirements.txt           # Dependencias
├── .env.example               # Ejemplo de variables de entorno
└── README.md                  # Este archivo
```

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd C:\Proyectos\BotPersonal
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar Tesseract OCR

**Windows:**
1. Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Ejecutar el instalador
3. Instalar en: `C:\Program Files\Tesseract-OCR`

**Verificar instalación:**
```bash
tesseract --version
```

### 5. Configurar variables de entorno

Copiar `.env.example` a `.env` y completar:

```env
# Discord Bot Token
DISCORD_TOKEN=tu_token_aqui

# OAuth2
CLIENT_ID=tu_client_id
CLIENT_SECRET=tu_client_secret
REDIRECT_URI=http://localhost:8080/callback
```

## 📝 Configuración

### Discord Bot Setup

1. Ir a [Discord Developer Portal](https://discord.com/developers/applications)
2. Crear nueva aplicación
3. En "Bot" → Add Bot
4. Copiar el token a `.env` como `DISCORD_TOKEN`
5. Habilitar intents:
   - Message Content Intent
   - Server Members Intent

### Permisos Necesarios

El bot necesita estos permisos (código 8 = Admin):
- Enviar mensajes
- Leer historial de mensajes
- Ver canales
- Procesar archivos adjuntos

## 🎮 Uso

### Iniciar el Bot

```bash
python main.py
```

El bot iniciará:
- ✅ Servidor web en `http://localhost:8080`
- ✅ Bot de Discord escuchando comandos

### Comandos Disponibles

| Comando | Descripción | Ejemplo |
|---------|------------|---------|
| `!gastos [días]` | Ver gastos recientes | `!gastos 30` |
| `!total [días]` | Total de gastos | `!total` |
| `!categorias [días]` | Gastos por categoría | `!categorias 7` |
| `!canales` | Listar canales | `!canales` |
| `!ping` | Latencia del bot | `!ping` |
| `!ayuda` | Ver ayuda completa | `!ayuda` |

### Procesar Facturas

1. Enviar imagen de factura en Discord
2. El bot automáticamente:
   - Descarga la imagen
   - Escanea con Tesseract OCR
   - Extrae información
   - Registra el gasto
   - Muestra resumen

## 🧪 Tests

### Ejecutar todos los tests

```bash
python run_tests.py
```

### Tests disponibles

- `test_factura_processor.py` - Tests de extracción de información
- `test_database.py` - Tests de base de datos
- `test_tesseract.py` - Verificación de Tesseract

## 📊 Base de Datos

SQLite con tabla de gastos:

```sql
CREATE TABLE gastos (
    id INTEGER PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    descripcion TEXT,
    monto REAL,
    categoria TEXT,
    fecha TEXT,
    imagen_url TEXT,
    datos_ocr TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## 🛠️ Solución de Problemas

### Error: "No module named 'audioop'"

```bash
pip install audioop-lts
```

### Error: "Tesseract is not installed"

1. Verificar instalación: `tesseract --version`
2. Verificar ruta en `src/config.py`
3. Agregar a PATH si es necesario

### Bot no responde

1. Verificar `DISCORD_TOKEN` en `.env`
2. Verificar permisos del bot en Discord
3. Revisar logs en consola

### OCR no extrae información

1. Verificar que la imagen sea legible
2. Revisar logs detallados en consola
3. Probar con `!ayuda` para ver estado

## 📝 Logs

El bot genera logs detallados con prefijos:

- `[CONFIG]` - Configuración del sistema
- `[BOT]` - Eventos del bot
- `[FACTURA]` - Procesamiento de facturas
- `[EXTRACCION]` - Extracción de información
- `[DATABASE]` - Operaciones de BD
- `[WEB]` - Servidor web

## 🔐 Seguridad

⚠️ **Importante:**
- Nunca compartir `DISCORD_TOKEN`
- Mantener `.env` fuera del control de versiones
- Usar permisos mínimos necesarios
- Validar entrada de usuarios

## 📦 Dependencias

```
discord.py==2.6.4
python-dotenv==1.0.0
pynacl==1.6.1
audioop-lts==0.2.2
aiohttp==3.13.2
flask==3.0.0
requests==2.31.0
pytesseract==0.3.10
pillow==10.1.0
```

## 📄 Licencia

Proyecto personal de código abierto.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios grandes, abre un issue primero.

## 📞 Soporte

Para reportar bugs o solicitar features, abre un issue en el repositorio.

---

**Última actualización:** Noviembre 2024
**Versión:** 1.0.0

