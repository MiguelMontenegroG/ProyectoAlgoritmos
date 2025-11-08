# Dockerfile para el proyecto de análisis bibliométrico
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome (última versión estable disponible)
RUN mkdir -p /etc/apt/keyrings \
    && wget -q -O /etc/apt/keyrings/google-linux-signing-key.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalar ChromeDriver compatible automáticamente
RUN CHROME_VERSION=$(google-chrome --version | grep -oE '[0-9]+(\.[0-9]+)+') \
    && CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_VERSION%%.*}") \
    && wget -q -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /usr/local/bin/chromedriver-linux64

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

# Establecer variables de entorno
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# Exponer puerto (para interfaz web o API)
EXPOSE 8000

# Comando por defecto
CMD ["python", "web_app.py"]
