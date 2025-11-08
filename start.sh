#!/bin/bash

# Script de inicio para Render
echo "🚀 Iniciando aplicación de análisis bibliométrico..."

# Crear directorios necesarios
mkdir -p output logs

# Establecer PYTHONPATH
export PYTHONPATH=/opt/render/project/src:$PYTHONPATH

# Verificar si es un entorno Render
if [ -n "$RENDER" ]; then
    echo "📦 Ejecutando en entorno Render"
    echo "🌐 Puerto: $PORT"

    # Para Render web service, ejecutar la aplicación web
    python web_app.py
else
    echo "💻 Ejecutando en entorno local"
    python main.py
fi