# 🚀 Guía de Despliegue - Proyecto Análisis Bibliométrico

Este documento explica cómo desplegar la aplicación de análisis bibliométrico usando Docker y Render.

## 📋 Requisitos Previos

- Docker y Docker Compose instalados (para despliegue local)
- Cuenta en Render.com (para despliegue en la nube)
- Git configurado

## 🐳 Despliegue con Docker

### Opción 1: Despliegue Simple

```bash
# Construir y ejecutar la aplicación
docker-compose up --build
```

### Opción 2: Solo Aplicación Principal

```bash
# Construir imagen
docker build -t bibliometric-analysis .

# Ejecutar contenedor
docker run -v $(pwd):/app -v $(pwd)/output:/app/output bibliometric-analysis
```

### Opción 3: Con Jupyter Notebook

```bash
# Ejecutar con Jupyter habilitado
docker-compose --profile jupyter up --build

# Acceder a Jupyter en http://localhost:8888
```

## ☁️ Despliegue en Render

### Paso 1: Preparar el Repositorio

1. Asegúrate de que todos los archivos estén en el repositorio:
   - `render.yaml`
   - `requirements.txt`
   - `start.sh`
   - Todo el código fuente

2. Confirma que `start.sh` tenga permisos de ejecución:
   ```bash
   chmod +x start.sh
   ```

### Paso 2: Desplegar en Render

1. Ve a [Render.com](https://render.com) y crea una cuenta
2. Conecta tu repositorio de GitHub
3. Render detectará automáticamente el archivo `render.yaml`
4. Configura los servicios:
   - **bibliometric-analysis**: Servicio web principal
   - **bibliometric-jupyter**: Servicio Jupyter (opcional)

### Paso 3: Configuración

Para el servicio principal:
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt && python procesamiento/install_dependencies.py`
- **Start Command**: `./start.sh`

Para Jupyter (opcional):
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt && python procesamiento/install_dependencies.py`
- **Start Command**: `jupyter notebook --ip=0.0.0.0 --port=$PORT --no-browser --allow-root`

## 🔧 Configuración del Entorno

### Variables de Entorno

```bash
# Para Render
PYTHONPATH=/opt/render/project/src
RENDER=true
PORT=10000  # Asignado automáticamente por Render

# Para Docker local
PYTHONPATH=/app
DISPLAY=:99
```

### Almacenamiento Persistente

- **Docker**: Los volúmenes están configurados para persistir datos en `output/` y `logs/`
- **Render**: Disco persistente configurado para `/opt/render/project/output`

## 📁 Estructura de Archivos

```
ProyectoAlgoritmos/
├── Dockerfile                 # Configuración Docker
├── docker-compose.yml         # Orquestación de contenedores
├── render.yaml               # Configuración Render
├── start.sh                  # Script de inicio
├── requirements.txt          # Dependencias Python
├── DEPLOYMENT.md            # Esta documentación
└── procesamiento/
    └── install_dependencies.py  # Instalador de dependencias
```

## 🚨 Solución de Problemas

### Problemas Comunes en Docker

1. **ChromeDriver no encontrado**:
   ```bash
   docker-compose down
   docker-compose up --build --force-recreate
   ```

2. **Permisos en archivos**:
   ```bash
   sudo chown -R $USER:$USER .
   ```

### Problemas Comunes en Render

1. **Instalación de dependencias falla**:
   - Verifica que `requirements.txt` esté actualizado
   - Revisa los logs de construcción en Render

2. **Aplicación no inicia**:
   - Verifica que `start.sh` tenga permisos de ejecución
   - Revisa las variables de entorno

3. **Almacenamiento insuficiente**:
   - Los archivos BibTeX pueden ser grandes
   - Considera aumentar el tamaño del disco en Render

## 📊 Monitoreo y Logs

### Docker
```bash
# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f bibliometric-analysis
```

### Render
- Los logs están disponibles en el dashboard de Render
- Revisa la pestaña "Logs" de cada servicio

## 🔄 Actualizaciones

### Docker
```bash
# Detener servicios
docker-compose down

# Obtener cambios
git pull

# Reconstruir e iniciar
docker-compose up --build
```

### Render
- Las actualizaciones se despliegan automáticamente al hacer push a la rama principal
- O puedes activar el despliegue manual desde el dashboard

## 🎯 Recomendaciones de Producción

1. **Monitoreo**: Configura alertas en Render para errores
2. **Backups**: Los datos en `output/` deberían ser respaldados regularmente
3. **Escalabilidad**: Considera múltiples instancias para alto tráfico
4. **Seguridad**: No almacenes credenciales en el código

## 🔍 Ejecutar Requerimiento 2

### Desde el Menú Principal
```bash
python main.py
# Seleccionar opción 2: "Herramientas de análisis"
# Luego elegir opción 2: "Análisis de Similitud Textual (Script)"
```

### Directamente (Windows)
```batch
# Usando el script batch
ejecutar_requerimiento2.bat

# O usando PowerShell
.\ejecutar_requerimiento2.ps1

# O directamente con Python
python procesamiento/Requerimiento2/requerimiento2Ejecutable.py
```

### Instalación Automática
Si faltan dependencias, el script las instala automáticamente:
```bash
python procesamiento/Requerimiento2/install_requerimiento2.py
```

### Características del Requerimiento 2
- ✅ **6 algoritmos**: Levenshtein, Jaccard, Jaro-Winkler, TF-IDF+Coseno, BERT, Sentence-BERT
- ✅ **Análisis detallado**: Explicaciones matemáticas paso a paso
- ✅ **Interfaz interactiva**: Selección de artículos desde BibTeX
- ✅ **Visualizaciones**: Gráficos comparativos y rankings
- ✅ **Instalación automática**: Verifica e instala dependencias faltantes
- ✅ **Acceso fácil**: Disponible desde el menú principal (opción 2 → submenú)

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs de la aplicación
2. Verifica la configuración del entorno
3. Consulta la documentación de Docker/Render
4. Revisa issues similares en el repositorio