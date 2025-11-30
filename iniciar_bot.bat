@echo off
REM Script de inicio del bot para Windows
REM Ejecutar desde la línea de comandos: iniciar_bot.bat

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║       🤖 BOT PERSONAL DE DISCORD - INICIO RÁPIDO          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar si el entorno virtual existe
if not exist ".venv" (
    echo ❌ Entorno virtual no encontrado
    echo.
    echo Crear con:
    echo   python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call .venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo ❌ Error al activar entorno virtual
    pause
    exit /b 1
)

echo ✅ Entorno virtual activado
echo.

REM Verificar .env
if not exist ".env" (
    echo ❌ Archivo .env no encontrado
    echo.
    echo Crear .env con:
    echo   DISCORD_TOKEN=tu_token
    echo   CLIENT_ID=tu_id
    echo   CLIENT_SECRET=tu_secret
    echo.
    pause
    exit /b 1
)

echo ✅ Archivo .env encontrado
echo.

REM Instalar dependencias si es necesario
echo 📦 Verificando dependencias...
pip show discord.py >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Instalando dependencias...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
)

echo ✅ Dependencias OK
echo.

REM Iniciar bot
echo 🚀 Iniciando bot...
echo.
python iniciar_bot.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error al iniciar bot
    pause
    exit /b 1
)

pause

