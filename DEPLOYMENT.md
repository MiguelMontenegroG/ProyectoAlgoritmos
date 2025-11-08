# 🚀 Guía de Despliegue - Proyecto Análisis Bibliométrico

Esta guía proporciona instrucciones **detalladas y paso a paso** para desplegar la aplicación de análisis bibliométrico en diferentes entornos.

## 📋 Requisitos Previos

### Para Todos los Entornos
- **Python 3.11+** instalado
- **Git** configurado
- **Cuenta GitHub** (para despliegue en la nube)

### Para Docker Local
- **Docker Desktop** o Docker Engine
- **Docker Compose** v2.0+
- Mínimo 4GB RAM disponible

### Para Render (Nube)
- **Cuenta en Render.com** (gratuita disponible)
- **Repositorio GitHub** público o privado

## 🏠 Instalación Local (Recomendado para Desarrollo)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/ProyectoAlgoritmos.git
cd ProyectoAlgoritmos
```

### Paso 2: Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar según sea necesario (opcional)
# nano .env
```

### Paso 3: Instalar Dependencias
```bash
# Instalar dependencias principales
pip install -r requirements.txt

# Instalar dependencias específicas del proyecto
python procesamiento/install_dependencies.py
```

### Paso 4: Ejecutar la Aplicación

#### Opción A: Interfaz Web (Recomendado)
```bash
python web_app.py
```
- Abre http://localhost:8000 en tu navegador
- Interfaz gráfica completa con todas las funcionalidades

#### Opción B: Menú de Consola
```bash
python main.py
```
- Menú interactivo en terminal
- Requiere interacción manual

#### Opción C: Requerimiento 2 Específico (Windows)
```batch
# Usando batch
ejecutar_requerimiento2.bat

# O usando PowerShell
.\ejecutar_requerimiento2.ps1

# O directamente
python procesamiento/Requerimiento2/requerimiento2Ejecutable.py
```

## 🐳 Despliegue con Docker

### Método 1: Docker Compose (Recomendado)
```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build

# Ver logs
docker-compose logs -f
```

**Acceder:**
- Aplicación principal: http://localhost:8000
- Jupyter (opcional): http://localhost:8888

### Método 2: Docker Solo
```bash
# Construir imagen
docker build -t bibliometric-analysis .

# Ejecutar contenedor
docker run -p 8000:8000 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  bibliometric-analysis
```

### Método 3: Con Jupyter Notebook
```bash
# Ejecutar servicios específicos
docker-compose --profile jupyter up --build
```

## ☁️ Despliegue en Render (Nube)

### Paso 1: Preparar Repositorio
```bash
# Asegurar que todos los archivos necesarios estén en Git
git add .
git commit -m "Preparar para despliegue en Render"
git push origin main
```

**Archivos críticos que deben estar en el repositorio:**
- ✅ `render.yaml`
- ✅ `requirements.txt`
- ✅ `web_app.py`
- ✅ `start.sh`
- ✅ `procesamiento/install_dependencies.py`
- ✅ Todo el código fuente en `src/`, `procesamiento/`, etc.

### Paso 2: Crear Cuenta en Render
1. Ve a [https://render.com](https://render.com)
2. Regístrate con GitHub (recomendado)
3. Verifica tu correo electrónico

### Paso 3: Conectar Repositorio
1. En el dashboard de Render, haz clic en "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente `render.yaml`

### Paso 4: Configurar Servicio
**Para el servicio principal (`bibliometric-analysis`):**
- **Name**: `bibliometric-analysis` (o tu preferencia)
- **Runtime**: `Python 3`
- **Build Command**:
  ```bash
  pip install -r requirements.txt && python procesamiento/install_dependencies.py
  ```
- **Start Command**:
  ```bash
  python web_app.py
  ```

### Paso 5: Configuración Avanzada
- **Environment**: `Production`
- **Instance Type**: `Free` (para empezar)
- **Disk**: 10GB (para almacenar datos BibTeX)

### Paso 6: Desplegar
1. Haz clic en "Create Web Service"
2. Espera a que se complete el build (5-15 minutos)
3. Una vez desplegado, obtendrás una URL como: `https://tu-app.onrender.com`

## 🔧 Configuración del Entorno

### Variables de Entorno (.env)
```bash
# Copiar y configurar
cp .env.example .env

# Variables importantes
PYTHONPATH=/app/src          # Para Docker
PYTHONPATH=/opt/render/project/src  # Para Render
RENDER=true                  # Indica entorno Render
PORT=8000                    # Puerto (asignado automáticamente en Render)
LOG_LEVEL=INFO              # Nivel de logging
```

### Estructura de Directorios
```
ProyectoAlgoritmos/
├── src/                     # Módulos principales
├── procesamiento/           # Scripts de procesamiento
├── output/                  # Resultados (creado automáticamente)
├── logs/                    # Logs de aplicación
├── web_app.py              # Interfaz web Flask
├── main.py                 # Menú de consola
├── requirements.txt        # Dependencias Python
├── Dockerfile              # Configuración Docker
├── docker-compose.yml      # Orquestación Docker
├── render.yaml            # Configuración Render
├── start.sh               # Script de inicio
├── .env.example           # Variables de entorno
└── .dockerignore          # Exclusiones Docker
```

## 🚨 Solución de Problemas

### Problemas Comunes

#### 1. Error: "No module named 'src'"
```bash
# Verificar PYTHONPATH
python -c "import sys; print(sys.path)"

# Solución: Ejecutar desde el directorio raíz
cd /ruta/al/proyecto
python web_app.py
```

#### 2. Error de Dependencias en Render
```bash
# Verificar requirements.txt
pip install -r requirements.txt

# Si falla, verificar versiones
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

#### 3. ChromeDriver no Funciona
```bash
# Para Docker local
docker-compose down
docker-compose up --build --force-recreate

# Para Render: Ya está configurado automáticamente
```

#### 4. Memoria Insuficiente
- **Docker**: Aumenta la memoria asignada en Docker Desktop
- **Render**: Actualiza a un plan pago o reduce el tamaño de los datos

#### 5. Puerto ya en Uso
```bash
# Cambiar puerto en .env
PORT=8001

# O matar proceso usando el puerto
lsof -ti:8000 | xargs kill -9
```

### Logs y Debugging

#### Docker
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de contenedor específico
docker logs bibliometric-analysis

# Acceder al contenedor
docker exec -it bibliometric-analysis bash
```

#### Render
1. Ve al dashboard de tu servicio
2. Haz clic en "Logs" en la barra lateral
3. Selecciona "Build" o "Runtime" logs

#### Local
```bash
# Ver logs de aplicación
tail -f logs/app.log

# Ejecutar con debug
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
python web_app.py
```

## 📊 Monitoreo y Mantenimiento

### Métricas a Monitorear
- **Uptime**: Disponibilidad del servicio
- **Response Time**: Tiempo de respuesta
- **Error Rate**: Tasa de errores
- **Storage Usage**: Uso de disco
- **Memory Usage**: Uso de memoria

### Tareas de Mantenimiento
```bash
# Limpiar contenedores Docker no utilizados
docker system prune -a

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Backup de datos
cp -r output output_backup_$(date +%Y%m%d)
```

## 🔄 Actualizaciones y Despliegue Continuo

### Docker Local
```bash
# Detener servicios
docker-compose down

# Obtener cambios
git pull

# Reconstruir e iniciar
docker-compose up --build
```

### Render (Automático)
1. Los cambios se despliegan automáticamente al hacer push a `main`
2. O activa despliegue manual desde el dashboard
3. Monitorea el proceso en la pestaña "Events"

### Versionado
```bash
# Crear tag para versión
git tag v1.0.0
git push origin v1.0.0

# En Render, especificar branch/tag en configuración
```

## 🎯 Recomendaciones de Producción

### Seguridad
- ✅ No almacenar credenciales en código
- ✅ Usar HTTPS (Render lo proporciona automáticamente)
- ✅ Mantener dependencias actualizadas
- ✅ Configurar CORS si es necesario

### Rendimiento
- ✅ Usar instancias apropiadas según la carga
- ✅ Configurar caché para datos estáticos
- ✅ Optimizar imágenes y PDFs generados
- ✅ Monitorear uso de memoria

### Backup y Recuperación
- ✅ Backup regular de datos en `output/`
- ✅ Configurar monitoreo de uptime
- ✅ Documentar procedimientos de recuperación

## 📞 Soporte y Contacto

### Recursos de Ayuda
- 📖 **Documentación**: Este archivo `DEPLOYMENT.md`
- 🐛 **Issues**: Reportar problemas en GitHub
- 💬 **Comunidad**: Foros de Docker/Render

### Checklist Pre-Despliegue
- [ ] Repositorio actualizado en GitHub
- [ ] Variables de entorno configuradas
- [ ] Dependencias probadas localmente
- [ ] Archivos estáticos optimizados
- [ ] Configuración de backup preparada
- [ ] Monitoreo configurado

---

**¡Tu aplicación está lista para producción!** 🚀

Si sigues esta guía paso a paso, tendrás una aplicación completamente funcional desplegada en la nube o ejecutándose localmente.