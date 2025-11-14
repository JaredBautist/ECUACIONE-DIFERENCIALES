@echo off
REM Script para iniciar el servidor backend de Python en Windows
REM Uso: start-backend.bat

echo.
echo 🚀 Iniciando DiffEQ Solver Backend...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install -r requirements.txt --quiet

echo.
echo ✅ Dependencias instaladas
echo.
echo 🌐 Iniciando servidor en http://localhost:8000
echo 📚 Documentación disponible en http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Iniciar el servidor
python python_backend_server.py
