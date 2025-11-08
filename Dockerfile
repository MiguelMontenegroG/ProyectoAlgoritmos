# Dockerfile para el proyecto de análisis bibliométrico
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome para web scraping
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalar ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Copiar archivos de requerimientos
COPY requirements.txt .
COPY procesamiento/install_dependencies.py .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias adicionales del proyecto
RUN python procesamiento/install_dependencies.py

# Copiar el código del proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p output logs

# Establecer variables de entorno
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# Exponer puerto (si es necesario para web interface)
EXPOSE 8000

# Comando por defecto
CMD ["python", "main.py"]