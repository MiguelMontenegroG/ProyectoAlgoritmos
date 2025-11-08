# Script para ejecutar el Requerimiento 2 en PowerShell
Write-Host "🚀 Ejecutando Requerimiento 2 - Análisis de Similitud Textual" -ForegroundColor Green
Write-Host ""

# Cambiar al directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Verificar si Python está disponible
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python encontrado" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python no encontrado en PATH" -ForegroundColor Red
    Write-Host "💡 Intente ejecutar directamente con la ruta completa de Python" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Ejemplo: & 'C:\Users\ANGEL\AppData\Local\Programs\Python\Python313\python.exe' procesamiento/Requerimiento2/requerimiento2Ejecutable.py" -ForegroundColor Cyan
    Read-Host "Presione Enter para continuar"
    exit 1
}

# Ejecutar el script
Write-Host "⏳ Ejecutando análisis de similitud textual..." -ForegroundColor Yellow
python procesamiento/Requerimiento2/requerimiento2Ejecutable.py

Write-Host ""
Read-Host "Presione Enter para salir"