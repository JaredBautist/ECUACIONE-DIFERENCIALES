#!/bin/bash

# Script para iniciar el servidor backend de Python
# Uso: ./start-backend.sh

echo "🚀 Iniciando DiffEQ Solver Backend..."
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip no está instalado"
    echo "Por favor instala pip"
    exit 1
fi

# Instalar dependencias si no están instaladas
echo "📦 Verificando dependencias..."
pip3 install -r requirements.txt --quiet

echo ""
echo "✅ Dependencias instaladas"
echo ""
echo "🌐 Iniciando servidor en http://localhost:8000"
echo "📚 Documentación disponible en http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar el servidor
python3 python_backend_server.py
