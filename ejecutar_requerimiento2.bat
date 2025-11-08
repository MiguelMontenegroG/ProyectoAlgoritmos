@echo off
REM Script para ejecutar el Requerimiento 2 en Windows
echo 🚀 Ejecutando Requerimiento 2 - Análisis de Similitud Textual
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Verificar si Python está disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado en PATH
    echo 💡 Intente ejecutar directamente con la ruta completa de Python
    echo.
    echo Ejemplo: "C:\Users\ANGEL\AppData\Local\Programs\Python\Python313\python.exe" procesamiento/Requerimiento2/requerimiento2Ejecutable.py
    pause
    exit /b 1
)

REM Ejecutar el script
python procesamiento/Requerimiento2/requerimiento2Ejecutable.py

REM Pausar para ver resultados
echo.
echo Presione cualquier tecla para continuar...
pause >nul