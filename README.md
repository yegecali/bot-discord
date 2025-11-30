# Bot Personal de Discord - Gestor de Gastos

Un bot de Discord que escanea facturas y registra tus gastos automáticamente usando OCR.

## 🎯 Características

- ✅ **Escaneo de Facturas** - Envía una imagen y el bot extrae el monto
- ✅ **Registro Automático de Gastos** - Se guardan en base de datos SQLite
- ✅ **Comandos de Consulta** - Ver tus gastos totales y por categoría
- ✅ **Sistema de Categorización** - Organiza gastos por tipo
- ✅ **Interfaz Web OAuth2** - Autoriza el bot fácilmente
- ✅ **Comandos Generales** - Ping, info de usuario, lista de canales

## 📋 Requisitos Previos

### Necesario
- Python 3.8 o superior
- pip (gestor de paquetes)
- **Tesseract OCR** instalado (ver [TESSERACT_INSTALL.md](TESSERACT_INSTALL.md))

### Discord
- Token del bot
- Client ID y Client Secret
- Permisos para leer mensajes y adjuntos

## 🚀 Instalación

### 1. Clonar/Descargar el proyecto

```bash
cd C:\Proyectos\BotPersonal
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar Tesseract OCR

⚠️ **IMPORTANTE:** Lee [TESSERACT_INSTALL.md](TESSERACT_INSTALL.md) para instalar Tesseract en tu sistema

### 5. Configurar credenciales

Copia `.env.example` a `.env`:
```bash
copy .env.example .env
```

Edita `.env` y agrega:
```
DISCORD_TOKEN=tu_token_del_bot
CLIENT_ID=tu_client_id
CLIENT_SECRET=tu_client_secret
REDIRECT_URI=http://localhost:8080/callback
```

## 🏃 Ejecutar el Bot

### Opción 1: Bot + Servidor Web (RECOMENDADO)

```bash
python main.py
```

Accede a: `http://localhost:8080`

### Opción 2: Solo el Bot

```bash
python bot.py
```

## 💰 Cómo Usar - Gestor de Gastos

### 1️⃣ Enviar una Factura

Simplemente **envía una foto de la factura** en Discord. El bot:
- 📸 Descarga la imagen
- 🔍 Escanea el texto con OCR
- 💰 Extrae el monto total
- 💾 Registra en la base de datos
- ✅ Te muestra un resumen

**Ejemplo:**
```
Tu: [Envías una foto de factura]
Bot: ✅ Gasto registrado correctamente
     💰 Monto: $45.99
     📝 Vendedor: Supermercado XYZ
     🏷️ Categoría: Alimentación
```

### 2️⃣ Ver Tus Gastos

```
!gastos          → Muestra últimos gastos (últimos 30 días)
!gastos 7        → Últimos 7 días
!total           → Total gastado
!total 7         → Total de la última semana
!categorias      → Gastos por categoría
```

### 3️⃣ Otros Comandos

```
!ping            → Latencia del bot
!hola            → Te saluda
!info            → Tu información
!canales         → Canales del servidor
!ayuda           → Lista de comandos
```

## 📊 Ejemplos de Uso

### Enviar factura de supermercado
```
[Imagen de factura]
↓
Bot: ✅ Gasto registrado
    💰 $125.50 USD
    📝 Carrefour
    🛒 Alimentación
```

### Ver total de gastos
```
Tu: !total
Bot: 💰 Total (últimos 30 días): $892.35
    📊 Número de transacciones: 12
    📈 Promedio: $74.36
```

### Ver por categoría
```
Tu: !categorias
Bot: 📊 Gastos por Categoría
    🍔 Alimentación: $450.00 (6 compras)
    🚗 Transporte: $200.00 (3 compras)
    📦 Otros: $242.35 (3 compras)
    Total: $892.35
```

## 📁 Estructura del Proyecto

```
BotPersonal/
├── main.py                  # Punto de entrada (bot + servidor)
├── bot.py                   # Lógica principal del bot
├── web_server.py            # Servidor Flask (OAuth2)
├── oauth_handler.py         # Manejo de OAuth2
├── database.py              # Gestión de base de datos SQLite
├── factura_processor.py     # Procesamiento de OCR
├── requirements.txt         # Dependencias
├── gastos.db                # Base de datos (se crea automáticamente)
├── .env.example             # Plantilla de variables
├── .env                     # Variables de entorno (no subir a git)
├── README.md                # Este archivo
├── QUICK_START.md           # Guía rápida
└── TESSERACT_INSTALL.md     # Instalación de Tesseract
```

## 🔐 Seguridad

⚠️ **IMPORTANTE:**
- **Nunca** compartas tu `DISCORD_TOKEN` o `CLIENT_SECRET`
- **No** subas el archivo `.env` a repositorios públicos
- `gastos.db` contiene datos personales - guárdalo bien
- El `.gitignore` ya excluye archivos sensibles

## 🐛 Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'tesseract'"
```bash
pip install pytesseract
```

### ❌ "TesseractNotFoundError"
→ Lee [TESSERACT_INSTALL.md](TESSERACT_INSTALL.md) para instalar Tesseract

### ❌ "No se encontró el monto total"
- La imagen debe ser legible (buena resolución)
- El texto debe estar en español o inglés
- Prueba con otra factura

### ❌ El bot no responde a imágenes
- Verifica que el bot tenga permisos de "Leer mensajes"
- Comprueba que el token sea válido
- Revisa la consola para ver los errores

### ❌ "Port 8080 already in use"
Edita `main.py` para cambiar el puerto:
```python
run_server(port=8081)
```

## 📚 Extensiones Posibles

- 📈 Gráficos de gastos
- 📧 Reportes mensuales por email
- 🏦 Integración con APIs bancarias
- 🎯 Metas de presupuesto
- 📱 Aplicación móvil

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:
- Reportar bugs
- Sugerir nuevas características
- Mejorar la documentación

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente.

## ❓ Preguntas

¿Problemas o dudas? Revisa:
1. [TESSERACT_INSTALL.md](TESSERACT_INSTALL.md) - Problemas con OCR
2. [QUICK_START.md](QUICK_START.md) - Guía rápida
3. Consola de errores del bot

---

**¡Listo para gestionar tus gastos! 💰**

