# 📊 Proyecto Análisis Bibliométrico - IA Generativa en Educación

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![Render](https://img.shields.io/badge/Render-Deployed-green)](https://render.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Análisis bibliométrico completo de la Inteligencia Artificial Generativa en Educación, desarrollado para la Universidad del Quindío. Implementa 5 requerimientos funcionales con múltiples algoritmos de análisis de datos científicos.

## 🎯 Características Principales

### ✅ Requerimientos Implementados

1. **📥 Automatización de Descarga de Datos**
   - Web scraping de IEEE Xplore y ScienceDirect
   - Unificación automática de archivos BibTeX
   - Eliminación de duplicados inteligente

2. **🎯 Análisis de Similitud Textual (6 Algoritmos)**
   - **Clásicos**: Levenshtein, Jaccard, Jaro-Winkler, TF-IDF + Coseno
   - **IA**: BERT, Sentence-BERT
   - Análisis paso a paso con explicaciones matemáticas

3. **📈 Análisis de Frecuencia por Categoría**
   - "Concepts of Generative AI in Education"
   - 15 palabras asociadas predefinidas
   - Algoritmo de expansión automática

4. **🌳 Clustering Jerárquico**
   - Tres algoritmos: Ward, Complete, Average
   - Dendrogramas interactivos
   - Determinación de coherencia

5. **📊 Visualizaciones Avanzadas**
   - Mapas de calor geográficos
   - Nubes de palabras dinámicas
   - Líneas temporales de publicaciones
   - Exportación automática a PDF

### 🚀 Múltiples Interfaces

- **🌐 Web App**: Interfaz gráfica completa (Flask)
- **💻 Consola**: Menú interactivo completo
- **📓 Jupyter**: Notebooks con explicaciones detalladas
- **🐳 Docker**: Contenedorización completa
- **☁️ Render**: Despliegue en la nube

## 🛠️ Tecnologías Utilizadas

### Lenguaje y Frameworks
- **Python 3.11+**
- **Flask** (interfaz web)
- **Jupyter Notebook** (análisis interactivo)

### Bibliotecas de IA y ML
- **Transformers** (modelos BERT)
- **Sentence-Transformers** (similitud semántica)
- **Scikit-learn** (algoritmos de ML)
- **PyTorch** (framework de deep learning)

### Análisis de Datos
- **Pandas & NumPy** (manipulación de datos)
- **SciPy** (cálculos científicos)
- **NLTK** (procesamiento de lenguaje)

### Visualización
- **Matplotlib & Seaborn** (gráficos)
- **Plotly** (visualizaciones interactivas)
- **WordCloud** (nubes de palabras)

### Web Scraping
- **Selenium** (automatización de navegadores)
- **ChromeDriver** (control de Chrome)
- **Requests** (solicitudes HTTP)

### Infraestructura
- **Docker & Docker Compose**
- **Render** (despliegue en la nube)
- **Git** (control de versiones)

## 🚀 Inicio Rápido

### Opción 1: Docker (Recomendado)
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/ProyectoAlgoritmos.git
cd ProyectoAlgoritmos

# Ejecutar con Docker
docker-compose up --build

# Acceder: http://localhost:8000
```

### Opción 2: Local
```bash
# Instalar dependencias
pip install -r requirements.txt
python procesamiento/install_dependencies.py

# Ejecutar aplicación web
python web_app.py

# O ejecutar menú de consola
python main.py
```

### Opción 3: Render (Nube)
1. Conecta tu repositorio a [Render.com](https://render.com)
2. Render detectará automáticamente la configuración
3. Despliegue automático en minutos

## 📁 Estructura del Proyecto

```
ProyectoAlgoritmos/
├── src/                          # Módulos principales
│   ├── similarity/              # Algoritmos de similitud textual
│   └── frequency/               # Análisis de frecuencia
├── procesamiento/               # Scripts de procesamiento
│   ├── Requerimiento1/          # Descarga y unificación
│   ├── Requerimiento2/          # Similitud textual
│   ├── Requerimiento3/          # Análisis de categoría
│   ├── Requerimiento4/          # Clustering
│   └── Requerimiento5/          # Visualizaciones
├── extractores/                 # Web scrapers
├── output/                      # Resultados generados
├── logs/                        # Logs de aplicación
├── web_app.py                   # Interfaz web Flask
├── main.py                      # Menú de consola
├── requirements.txt             # Dependencias Python
├── Dockerfile                   # Configuración Docker
├── docker-compose.yml           # Orquestación Docker
├── render.yaml                  # Configuración Render
└── DEPLOYMENT.md               # Guía de despliegue completa
```

## 🎮 Uso de la Aplicación

### Interfaz Web
1. Accede a la URL proporcionada
2. Selecciona el análisis deseado del menú principal
3. Sigue las instrucciones en pantalla

### Menú de Consola
```bash
python main.py
# Selecciona opciones del 1 al 10
```

### Requerimiento 2 Específico
```bash
# Windows
.\ejecutar_requerimiento2.bat

# O directamente
python procesamiento/Requerimiento2/requerimiento2Ejecutable.py
```

## 📊 Algoritmos Implementados

### Similitud Textual (Requerimiento 2)
| Algoritmo | Tipo | Descripción |
|-----------|------|-------------|
| Levenshtein | Clásico | Distancia de edición de caracteres |
| Jaccard | Clásico | Similitud de conjuntos de palabras |
| Jaro-Winkler | Clásico | Optimizado para nombres y strings cortos |
| TF-IDF + Coseno | Estadístico | Vectorización con similitud coseno |
| BERT | IA | Contexto bidireccional transformer |
| Sentence-BERT | IA | Similitud semántica optimizada |

### Clustering (Requerimiento 4)
- **Ward**: Minimiza varianza intra-cluster
- **Complete**: Distancia máxima entre clusters
- **Average**: Distancia promedio entre clusters

## 🔧 Configuración

### Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Variables importantes
PYTHONPATH=/app/src          # Ruta de módulos
PORT=8000                    # Puerto del servidor
LOG_LEVEL=INFO              # Nivel de logging
```

### Dependencias del Sistema
- **Chrome/Chromium** (para web scraping)
- **Python 3.11+**
- **4GB RAM mínimo**
- **10GB espacio en disco**

## 📈 Resultados y Salidas

### Archivos Generados
- `output/unified_cleaned.bib` - Base de datos unificada
- `output/duplicates.bib` - Registros duplicados eliminados
- `output/*.pdf` - Visualizaciones exportadas
- `output/*.png` - Gráficos generados
- `logs/app.log` - Logs de aplicación

### Métricas de Rendimiento
- ✅ Procesamiento de +5000 artículos científicos
- ✅ 6 algoritmos de similitud implementados
- ✅ Análisis en tiempo real
- ✅ Exportación automática de resultados

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **Universidad del Quindío** - Institución patrocinadora
- **IEEE Xplore** y **ScienceDirect** - Fuentes de datos
- **Comunidad de Python** - Bibliotecas y frameworks utilizados

## 📞 Contacto

- **Institución**: Universidad del Quindío
- **Proyecto**: Análisis de Algoritmos
- **Tema**: Inteligencia Artificial Generativa en Educación

---

**🚀 ¡Listo para revolucionar el análisis bibliométrico!**

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en GitHub.