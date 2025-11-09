# Dockerfile para el proyecto de análisis bibliométrico
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (mínimas para versión web)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# NOTA: Chrome y ChromeDriver NO se instalan en la versión web para reducir el tamaño
# Estas dependencias solo están disponibles en modo consola con requirements-full.txt
# Si necesita descargar documentos, use el modo consola local:
#   pip install -r requirements-full.txt
#   python main.py

# Copiar los archivos principales
COPY requirements.txt . 

# Crear la carpeta antes de copiar el script
RUN mkdir -p procesamiento

# Copiar el script de instalación de dependencias
COPY procesamiento/install_dependencies.py procesamiento/install_dependencies.py

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el instalador de dependencias adicionales
RUN python procesamiento/install_dependencies.py

# Finalmente copiar todo el código del proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p output logs

# Crear script de inicio que verifica e instala dependencias si es necesario
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'set -e' >> /entrypoint.sh && \
    echo 'echo "🔍 Verificando dependencias..."' >> /entrypoint.sh && \
    echo 'if [ -f "procesamiento/install_dependencies.py" ]; then' >> /entrypoint.sh && \
    echo '    python procesamiento/install_dependencies.py || echo "⚠️ Algunas dependencias opcionales pueden no estar disponibles"' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    echo 'echo "🚀 Iniciando aplicación..."' >> /entrypoint.sh && \
    echo 'exec "$@"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Establecer variables de entorno
ENV PYTHONPATH=/app:/app/src
# DISPLAY no es necesario sin Chrome
# ENV DISPLAY=:99

# Exponer puerto (para interfaz web o API)
EXPOSE 8000

# Usar el script de entrada
ENTRYPOINT ["/entrypoint.sh"]

# Comando por defecto
CMD ["python", "web_app.py"]
