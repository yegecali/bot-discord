#!/bin/bash
# Script de inicio del bot para Linux/MacOS

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║       🤖 BOT PERSONAL DE DISCORD - INICIO RÁPIDO          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar si el entorno virtual existe
if [ ! -d ".venv" ]; then
    echo "❌ Entorno virtual no encontrado"
    echo ""
    echo "Crear con:"
    echo "  python3 -m venv .venv"
    echo ""
    exit 1
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error al activar entorno virtual"
    exit 1
fi

echo "✅ Entorno virtual activado"
echo ""

# Verificar .env
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado"
    echo ""
    echo "Crear .env con:"
    echo "  DISCORD_TOKEN=tu_token"
    echo "  CLIENT_ID=tu_id"
    echo "  CLIENT_SECRET=tu_secret"
    echo ""
    exit 1
fi

echo "✅ Archivo .env encontrado"
echo ""

# Instalar dependencias si es necesario
echo "📦 Verificando dependencias..."
pip show discord.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️ Instalando dependencias..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias"
        exit 1
    fi
fi

echo "✅ Dependencias OK"
echo ""

# Iniciar bot
echo "🚀 Iniciando bot..."
echo ""
python3 iniciar_bot.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error al iniciar bot"
    exit 1
fi

