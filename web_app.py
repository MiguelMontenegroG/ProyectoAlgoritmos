"""
Aplicación web Flask para el proyecto de análisis bibliométrico
Permite acceso web a todas las funcionalidades del proyecto con interfaz completa
"""

import os
import sys
import subprocess
import io
import contextlib
import json
import tempfile
from flask import Flask, render_template_string, request, redirect, url_for, flash, session, jsonify
import threading
import time
import base64

# Configurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Funciones web-friendly (sin input interactivo)
def mainRequerimiento2_web():
    """Versión web del Requerimiento 2 con valores por defecto - completamente automática"""
    import os
    import sys
    import pandas as pd
    import warnings
    warnings.filterwarnings('ignore')

    # Configurar rutas
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = current_dir
    src_path = os.path.join(project_root, 'src')

    possible_src_paths = [
        src_path,
        os.path.join(current_dir, '..', '..', '..', 'src'),
        os.path.join(current_dir, '..', '..', 'src'),
        os.path.join(os.getcwd(), 'src'),
        os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'src'))
    ]

    src_path_found = None
    for path in possible_src_paths:
        if os.path.exists(path):
            src_path_found = os.path.abspath(path)
            break

    if src_path_found:
        if src_path_found not in sys.path:
            sys.path.insert(0, src_path_found)
        project_root = os.path.dirname(src_path_found)
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    print("=" * 80)
    print("                🎯 REQUERIMIENTO 2: ANÁLISIS DE SIMILITUD TEXTUAL (WEB)")
    print("=" * 80)
    print("Versión completamente automática - sin interacción del usuario")
    print("=" * 80)

    try:
        # Importar funciones necesarias
        from procesamiento.Requerimiento2.requerimiento2Ejecutable import (
            load_bibtex_abstracts, run_similarity_analysis, display_article_info,
            show_detailed_analysis, create_visualization, find_bibtex_file
        )

        # Buscar archivo BibTeX
        bibtex_path = find_bibtex_file()
        if not bibtex_path:
            print("\n❌ No se encontró archivo BibTeX unificado")
            print("💡 Para generar archivos BibTeX:")
            print("   1. Descargue archivos .bib en modo consola local")
            print("   2. O suba archivos .bib al directorio 'output/'")
            print("   3. Luego ejecute 'Unificar y Filtrar Datos' desde el menú principal")
            print("\n📁 Archivos .bib buscados en:")
            output_dir = os.path.join(project_root, 'output')
            if os.path.exists(output_dir):
                bib_files = [f for f in os.listdir(output_dir) if f.endswith('.bib')]
                if bib_files:
                    print(f"   Encontrados {len(bib_files)} archivos .bib:")
                    for f in bib_files:
                        print(f"   - {f}")
                else:
                    print("   No se encontraron archivos .bib en output/")
            return

        print(f"\n📁 Archivo BibTeX encontrado: {os.path.basename(bibtex_path)}")

        # Cargar abstracts
        abstracts = load_bibtex_abstracts(bibtex_path)
        if abstracts.empty:
            print("❌ No se pudieron cargar los abstracts")
            print("💡 El archivo BibTeX puede estar vacío o no tener el formato correcto")
            return

        print(f"✅ Se cargaron {len(abstracts)} abstracts exitosamente")

        # Seleccionar automáticamente los primeros 2 artículos
        if len(abstracts) < 2:
            print("❌ Se necesitan al menos 2 artículos para el análisis")
            print(f"💡 El archivo solo contiene {len(abstracts)} artículo(s)")
            return

        abstract1_data = {
            'title': str(abstracts.iloc[0]['title']),
            'abstract': str(abstracts.iloc[0]['abstract']),
            'year': str(abstracts.iloc[0]['year'])
        }
        abstract2_data = {
            'title': str(abstracts.iloc[1]['title']),
            'abstract': str(abstracts.iloc[1]['abstract']),
            'year': str(abstracts.iloc[1]['year'])
        }

        print(f"📄 Artículo 1: {abstract1_data['title'][:60]}...")
        print(f"📄 Artículo 2: {abstract2_data['title'][:60]}...")

        # Mostrar información básica
        print(f"\n📊 Información del Artículo 1:")
        print(f"   Título: {abstract1_data['title'][:50]}...")
        print(f"   Año: {abstract1_data['year']}")
        print(f"   Longitud abstract: {len(abstract1_data['abstract'])} caracteres")

        print(f"\n📊 Información del Artículo 2:")
        print(f"   Título: {abstract2_data['title'][:50]}...")
        print(f"   Año: {abstract2_data['year']}")
        print(f"   Longitud abstract: {len(abstract2_data['abstract'])} caracteres")

        # Ejecutar análisis de similitud
        print("\n🔍 Ejecutando análisis de similitud de 6 algoritmos...")
        analyzer = run_similarity_analysis(abstract1_data, abstract2_data)
        print("✅ Análisis de similitud completado")

        # Mostrar resultados detallados
        print("\n📈 RESULTADOS DETALLADOS:")
        show_detailed_analysis(analyzer)

        # Generar visualización
        print("\n🎨 Generando gráfico de comparación...")
        create_visualization(analyzer.compare_all())
        print("✅ Gráfico generado exitosamente")

        print("\n🎯 Análisis de similitud textual completado exitosamente")
        print("   Los resultados y gráficos están disponibles en la interfaz web")

    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("💡 Verifique que todas las dependencias estén instaladas")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Error en el análisis: {e}")
        import traceback
        traceback.print_exc()

def mainRequerimiento2_first_last_web():
    """Versión web del Requerimiento 2 - compara primer y último documento automáticamente"""
    import os
    import sys
    import pandas as pd
    import warnings
    warnings.filterwarnings('ignore')

    # Configurar rutas
    current_dir = os.path.dirname(os.path.abspath(__file__))
    possible_src_paths = [
        os.path.join(current_dir, '..', '..', '..', 'src'),
        os.path.join(current_dir, '..', '..', 'src'),
        os.path.join(os.getcwd(), 'src'),
        os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'src'))
    ]

    src_path = None
    for path in possible_src_paths:
        if os.path.exists(path):
            src_path = os.path.abspath(path)
            break

    if src_path is None:
        print("❌ ERROR: No se pudo encontrar el directorio 'src'")
        return

    project_root = os.path.dirname(src_path)

    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    print("=" * 80)
    print("                🎯 REQUERIMIENTO 2: ANÁLISIS DE SIMILITUD (WEB)")
    print("                Comparación: Primer vs Último Documento")
    print("=" * 80)
    print("Versión completamente automática - sin interacción del usuario")
    print("=" * 80)

    try:
        # Importar funciones necesarias
        from procesamiento.Requerimiento2.requerimiento2Ejecutable import (
            load_bibtex_abstracts, run_similarity_analysis, display_article_info,
            show_detailed_analysis, create_visualization, find_bibtex_file
        )

        # Buscar archivo BibTeX
        bibtex_path = find_bibtex_file()
        if not bibtex_path:
            print("\n❌ No se encontró archivo BibTeX unificado")
            print("Ejecute primero el Requerimiento 1 para generar el archivo unificado")
            return

        print(f"\n📁 Archivo BibTeX encontrado: {os.path.basename(bibtex_path)}")

        # Cargar abstracts
        abstracts = load_bibtex_abstracts(bibtex_path)
        if abstracts.empty:
            print("❌ No se pudieron cargar los abstracts")
            return

        print(f"✅ Se cargaron {len(abstracts)} abstracts exitosamente")

        # Seleccionar automáticamente el primer y último artículo
        if len(abstracts) < 2:
            print("❌ Se necesitan al menos 2 artículos para el análisis")
            return

        abstract1_data = {
            'title': str(abstracts.iloc[0]['title']),
            'abstract': str(abstracts.iloc[0]['abstract']),
            'year': str(abstracts.iloc[0]['year'])
        }
        abstract2_data = {
            'title': str(abstracts.iloc[-1]['title']),
            'abstract': str(abstracts.iloc[-1]['abstract']),
            'year': str(abstracts.iloc[-1]['year'])
        }

        print(f"📄 Artículo 1 (PRIMER): {abstract1_data['title'][:60]}...")
        print(f"📄 Artículo 2 (ÚLTIMO): {abstract2_data['title'][:60]}...")

        # Mostrar información básica
        print(f"\n📊 Información del Primer Artículo:")
        print(f"   Título: {abstract1_data['title'][:50]}...")
        print(f"   Año: {abstract1_data['year']}")
        print(f"   Longitud abstract: {len(abstract1_data['abstract'])} caracteres")

        print(f"\n📊 Información del Último Artículo:")
        print(f"   Título: {abstract2_data['title'][:50]}...")
        print(f"   Año: {abstract2_data['year']}")
        print(f"   Longitud abstract: {len(abstract2_data['abstract'])} caracteres")

        # Ejecutar análisis de similitud
        print("\n🔍 Ejecutando análisis de similitud de 6 algoritmos...")
        analyzer = run_similarity_analysis(abstract1_data, abstract2_data)
        print("✅ Análisis de similitud completado")

        # Mostrar resultados detallados automáticamente
        print("\n📈 RESULTADOS DETALLADOS:")
        show_detailed_analysis(analyzer)

        # Generar visualización automáticamente
        print("\n🎨 Generando gráfico comparativo interactivo...")
        create_visualization(analyzer.compare_all())
        print("✅ Gráfico interactivo generado exitosamente")

        print("\n🎯 Análisis de similitud completado exitosamente")
        print("   Comparación: Primer documento vs Último documento")
        print("   Los resultados y gráficos están disponibles en la interfaz web")

    except Exception as e:
        print(f"❌ Error en el análisis: {e}")
        import traceback
        traceback.print_exc()

def ejecutarEjecutar_web():
    """Versión web del Seguimiento 2 Punto 2 - análisis rápido automático"""
    import os
    import sys
    import subprocess

    print("=" * 80)
    print("                🎯 SEGUIMIENTO 2 PUNTO 2: ANÁLISIS DE GRAFO (WEB)")
    print("=" * 80)
    print("Versión automática - Análisis Rápido (100 documentos)")
    print("=" * 80)

    try:
        # Configurar rutas
        current_dir = os.path.dirname(os.path.abspath(__file__))
        possible_src_paths = [
            os.path.join(current_dir, '..', '..', '..', 'src'),
            os.path.join(current_dir, '..', '..', 'src'),
            os.path.join(os.getcwd(), 'src'),
            os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'src'))
        ]

        src_path = None
        for path in possible_src_paths:
            if os.path.exists(path):
                src_path = os.path.abspath(path)
                break

        if src_path is None:
            print("❌ ERROR: No se pudo encontrar el directorio 'src'")
            return

        project_root = os.path.dirname(src_path)

        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        # Ejecutar directamente el script main_fast.py sin interacción
        script_path = os.path.join(project_root, 'procesamiento', 'Seguimiento2', 'punto2', 'main_fast.py')

        if os.path.exists(script_path):
            print("📊 Iniciando análisis rápido de 100 documentos...")
            print("⏱️  Tiempo estimado: 1-2 minutos")
            print("🎨 Se generarán visualizaciones automáticamente\n")

            # Ejecutar el script
            result = subprocess.run([sys.executable, script_path],
                                  cwd=os.path.dirname(script_path),
                                  capture_output=True,
                                  text=True,
                                  timeout=300)  # 5 minutos timeout

            # Mostrar salida
            if result.stdout:
                print("SALIDA DEL ANÁLISIS:")
                print(result.stdout)

            if result.stderr:
                print("MENSAJES DE ERROR:")
                print(result.stderr)

            if result.returncode == 0:
                print("\n✅ Análisis completado exitosamente")
                print("📊 Los gráficos están disponibles en la interfaz web")
            else:
                print(f"\n❌ Error en el análisis (código {result.returncode})")

        else:
            print(f"❌ Script no encontrado: {script_path}")

    except subprocess.TimeoutExpired:
        print("❌ El análisis tardó demasiado tiempo (timeout)")
    except Exception as e:
        print(f"❌ Error ejecutando el análisis: {e}")
        import traceback
        traceback.print_exc()

# Importaciones del proyecto - Importación individual para mejor diagnóstico
print("=" * 80)
print("🔍 Importando módulos del proyecto...")
print("=" * 80)

# Diccionario para almacenar los módulos importados y su estado
IMPORTED_MODULES = {}
IMPORTS_OK = True

# Lista de módulos a importar con sus nombres para mensajes
modules_to_import = [
    ("procesamiento.Requerimiento2.requerimiento2Ejecutable", "mainRequerimiento2", "Requerimiento2"),
    ("procesamiento.Requerimiento3.FrecuenciaPalabra", "mainEjecutableRequerimiento3", "Requerimiento3"),
    ("procesamiento.Requerimiento4.clutsteringDatos", "mainRequerimiento4", "Requerimiento4"),
    ("procesamiento.Requerimiento5.requerimiento5Ejecutable", "mainRequerimiento5", "Requerimiento5"),
    ("procesamiento.Seguimiento1.Punto1Seguimiento.mainSeguimiento1", "mainSeguimiento1", "Seguimiento1 Punto1"),
    ("procesamiento.Seguimiento1.punto3Seguimiento.mainSeguimientoPunto3", "seguimiento1Punto3", "Seguimiento1 Punto3"),
    ("procesamiento.Seguimiento2.Punto1.grafoDirigido", "ejecutarGrafoDirigido", "Seguimiento2 Punto1"),
    ("procesamiento.Seguimiento2.punto2.ejecutar", "ejecutarEjecutar", "Seguimiento2 Punto2"),
    ("extractores.analizador", "mainAnalizador", "Analizador"),
    ("procesamiento.unifyBibtext", "unificar", "Unify"),
    ("instalarJupyter", "mainJupyter", "Jupyter"),
]

# Importar cada módulo individualmente
# Módulos opcionales que no afectan IMPORTS_OK si fallan
optional_modules = {"mainJupyter"}  # Jupyter es opcional para versión web

for module_path, function_name, display_name in modules_to_import:
    try:
        module = __import__(module_path, fromlist=[function_name])
        function = getattr(module, function_name)
        IMPORTED_MODULES[function_name] = function
        if function_name in optional_modules:
            print(f"✅ {display_name} importado correctamente (opcional)")
        else:
            print(f"✅ {display_name} importado correctamente")
    except ImportError as e:
        if function_name in optional_modules:
            print(f"⚠️ {display_name} no disponible (opcional - solo en modo consola): {e}")
        else:
            print(f"❌ Error importando {display_name}: {e}")
        IMPORTED_MODULES[function_name] = None
        # Solo marcar como error si no es un módulo opcional
        if function_name not in optional_modules:
            IMPORTS_OK = False
        # No salir, continuar con los demás módulos
    except Exception as e:
        if function_name in optional_modules:
            print(f"⚠️ {display_name} no disponible (opcional): {e}")
        else:
            print(f"⚠️ Error inesperado importando {display_name}: {e}")
            import traceback
            traceback.print_exc()
        IMPORTED_MODULES[function_name] = None
        # Solo marcar como error si no es un módulo opcional
        if function_name not in optional_modules:
            IMPORTS_OK = False

print("=" * 80)
if IMPORTS_OK:
    print("✅ Todos los módulos importados correctamente")
else:
    print("⚠️ Algunos módulos no se pudieron importar. La aplicación puede tener funcionalidad limitada.")
    print("💡 Verifique que todas las dependencias estén instaladas correctamente.")
print("=" * 80)

# Crear funciones stub para módulos no disponibles
def create_stub_function(name):
    def stub(*args, **kwargs):
        raise ImportError(f"El módulo {name} no está disponible. Verifique la instalación.")
    return stub

# Asignar funciones importadas o stubs a variables globales
mainRequerimiento2 = IMPORTED_MODULES.get("mainRequerimiento2") or create_stub_function("Requerimiento2")
mainEjecutableRequerimiento3 = IMPORTED_MODULES.get("mainEjecutableRequerimiento3") or create_stub_function("Requerimiento3")
mainRequerimiento4 = IMPORTED_MODULES.get("mainRequerimiento4") or create_stub_function("Requerimiento4")
mainRequerimiento5 = IMPORTED_MODULES.get("mainRequerimiento5") or create_stub_function("Requerimiento5")
mainSeguimiento1 = IMPORTED_MODULES.get("mainSeguimiento1") or create_stub_function("Seguimiento1")
seguimiento1Punto3 = IMPORTED_MODULES.get("seguimiento1Punto3") or create_stub_function("Seguimiento1 Punto3")
ejecutarGrafoDirigido = IMPORTED_MODULES.get("ejecutarGrafoDirigido") or create_stub_function("Seguimiento2 Punto1")
ejecutarEjecutar = IMPORTED_MODULES.get("ejecutarEjecutar") or create_stub_function("Seguimiento2 Punto2")
mainAnalizador = IMPORTED_MODULES.get("mainAnalizador") or create_stub_function("Analizador")
unificar = IMPORTED_MODULES.get("unificar") or create_stub_function("Unify")
mainJupyter = IMPORTED_MODULES.get("mainJupyter") or create_stub_function("Jupyter")

app = Flask(__name__)
app.secret_key = 'bibliometric-analysis-secret-key'

# Template HTML principal
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proyecto Análisis Bibliométrico</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .menu-item {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 2px solid transparent;
        }
        .menu-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
            border-color: #667eea;
        }
        .menu-item h3 {
            color: #333;
            margin-top: 0;
            font-size: 1.4em;
        }
        .menu-item p {
            color: #666;
            margin-bottom: 15px;
            line-height: 1.5;
        }
        .menu-item .number {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 50%;
            font-weight: bold;
            margin-right: 10px;
        }
        .btn {
            background: #667eea;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            text-decoration: none;
            display: inline-block;
            transition: background 0.3s ease;
        }
        .btn:hover {
            background: #5a6fd8;
        }
        .btn-secondary {
            background: #6c757d;
        }
        .btn-secondary:hover {
            background: #5a6268;
        }
        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid transparent;
            border-radius: 4px;
        }
        .alert-success {
            color: #155724;
            background-color: #d4edda;
            border-color: #c3e6cb;
        }
        .alert-error {
            color: #721c24;
            background-color: #f8d7da;
            border-color: #f5c6cb;
        }
        .status {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 15px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
        }
        .status.ready {
            background: #28a745;
        }
        .status.error {
            background: #dc3545;
        }
    </style>
</head>
<body>
    <div class="container">
        {% if status == 'ready' %}
        <div class="status ready">✅ Sistema Listo</div>
        {% elif status == 'error' %}
        <div class="status error">❌ Error en el Sistema</div>
        {% endif %}

        {% if data_status == 'no_data' %}
        <div class="status" style="background: #fff3cd; color: #856404; border: 1px solid #ffeaa7;">
            ⚠️ No hay datos bibliográficos unificados. Puede unificar archivos BibTeX existentes usando la opción "Unificar y Filtrar Datos", o descargar nuevos datos en modo consola local.
        </div>
        {% endif %}

        <div class="header">
            <h1>📊 Proyecto Análisis Bibliométrico</h1>
            <p>Inteligencia Artificial Generativa en Educación</p>
        </div>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'success' if category == 'success' else 'error' }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="menu-grid">
            <div class="menu-item" style="opacity: 0.6; position: relative;">
                <div style="position: absolute; top: 10px; right: 10px; background: #ffc107; color: #000; padding: 5px 10px; border-radius: 5px; font-size: 0.8em; font-weight: bold;">
                    ⚠️ NO DISPONIBLE EN WEB
                </div>
                <h3><span class="number">1</span>Descargar Documentos</h3>
                <p><strong style="color: #dc3545;">⚠️ La descarga de documentos no está disponible en la versión web.</strong><br>
                La descarga de documentos requiere Selenium y ChromeDriver, que no están disponibles en el despliegue web por limitaciones de recursos.<br>
                <strong>💡 Solución:</strong> Use el modo consola local ejecutando <code>python main.py</code> o <code>python llamados.py</code> con <code>requirements-full.txt</code> instalado.</p>
                <button class="btn" style="background: #6c757d; cursor: not-allowed;" disabled>🚫 No Disponible en Web</button>
            </div>

            <div class="menu-item">
                <h3><span class="number">1b</span>Unificar y Filtrar Datos</h3>
                <p>Unifica y filtra archivos BibTeX ya descargados. Esta funcionalidad está disponible en la versión web.</p>
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="unify_only">
                    <button type="submit" class="btn">🔄 Unificar Archivos</button>
                </form>
            </div>

            <div class="menu-item">
                <h3><span class="number">2</span>Herramientas de Análisis</h3>
                <p>Análisis de similitud textual (disponible) y Jupyter Notebook (solo modo consola).</p>
                <a href="/analysis_tools" class="btn">🔬 Acceder</a>
            </div>

            <div class="menu-item">
                <h3><span class="number">3</span>Análisis de Categoría</h3>
                <p>Analiza la frecuencia de palabras asociadas a "Generative AI in Education".</p>
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="category_analysis">
                    <button type="submit" class="btn">📈 Ejecutar</button>
                </form>
            </div>

            <div class="menu-item">
                <h3><span class="number">4</span>Dendrogramas de Clustering</h3>
                <p>Visualiza los dendrogramas de los tres algoritmos de agrupamiento jerárquico.</p>
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="clustering">
                    <button type="submit" class="btn">🌳 Ejecutar</button>
                </form>
            </div>

            <div class="menu-item">
                <h3><span class="number">5</span>Visualizaciones Avanzadas</h3>
                <p>Mapas de calor, nube de palabras y línea temporal con exportación a PDF.</p>
                <a href="/visualizations" class="btn">📊 Configurar y Ejecutar</a>
            </div>

            <div class="menu-item">
                <h3><span class="number">6-9</span>Análisis Adicionales</h3>
                <p>Seguimientos 1 y 2, análisis complementarios del proyecto.</p>
                <a href="/additional_analysis" class="btn">🔍 Ver Opciones</a>
            </div>
        </div>

        <div style="text-align: center; margin-top: 40px;">
            <p style="color: white; opacity: 0.8;">
                Desarrollado para Analisis de Algoritmos por Miguel Montenegro, Nicolas Peña y jose Taborda
            </p>
        </div>
    </div>
</body>
</html>
"""

ANALYSIS_TOOLS_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Herramientas de Análisis</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .option { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #667eea; }
        .option.disabled { opacity: 0.6; border-left-color: #6c757d; background: #e9ecef; }
        .warning-badge { background: #ffc107; color: #000; padding: 5px 10px; border-radius: 5px; font-size: 0.9em; font-weight: bold; display: inline-block; margin-bottom: 10px; }
        .btn { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }
        .btn:hover { background: #5a6fd8; }
        .btn:disabled { background: #6c757d; cursor: not-allowed; opacity: 0.6; }
        .btn-secondary { background: #6c757d; }
        .btn-secondary:hover { background: #5a6268; }
        .alert-warning { background: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔬 Herramientas de Análisis</h1>
            <p>Selecciona la herramienta que mejor se adapte a tus necesidades</p>
        </div>

        <div class="option disabled">
            <span class="warning-badge">⚠️ NO DISPONIBLE EN VERSIÓN WEB</span>
            <h3>📓 Jupyter Notebook</h3>
            <div class="alert-warning">
                <strong>⚠️ Esta funcionalidad no está disponible en la versión web.</strong><br>
                Jupyter Notebook y sus dependencias (jupyter, ipykernel, etc.) son demasiado pesadas para el despliegue web en Render.<br>
                <strong>💡 Solución:</strong> Para usar Jupyter Notebook, ejecute el proyecto en modo consola local:
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>Instale las dependencias completas: <code>pip install -r requirements-full.txt</code></li>
                    <li>Ejecute el proyecto: <code>python main.py</code> o <code>python llamados.py</code></li>
                    <li>Seleccione la opción de Jupyter Notebook desde el menú</li>
                </ul>
            </div>
            <button type="button" class="btn" disabled>🚫 No Disponible en Web</button>
        </div>

        <div class="option">
            <h3>🎯 Análisis de Similitud Textual (Script)</h3>
            <p>Análisis automático que compara el primer y último documento usando 6 algoritmos de similitud.</p>
            <p><strong>Algoritmos:</strong> Levenshtein, Jaccard, Jaro-Winkler, TF-IDF+Coseno, BERT, Sentence-BERT</p>
            <p><strong>Comparación:</strong> Primer documento vs Último documento (automático)</p>
            <p><strong>✅ Disponible en versión web</strong></p>
            <form method="post" action="/execute">
                <input type="hidden" name="action" value="similarity_analysis">
                <button type="submit" class="btn">📊 Ejecutar Análisis</button>
            </form>
        </div>

        <div class="option">
            <h3>🔍 Análisis de Similitud Personalizado</h3>
            <p>Selecciona manualmente dos artículos específicos para comparar usando todos los algoritmos de similitud.</p>
            <p><strong>Características:</strong> Selección personalizada de artículos, comparación detallada</p>
            <p><strong>✅ Disponible en versión web</strong></p>
            <a href="/similarity_custom" class="btn">🎛️ Configurar Análisis</a>
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <a href="/" class="btn btn-secondary">⬅️ Volver al Menú Principal</a>
        </div>
    </div>
</body>
</html>
"""

SIMILARITY_CUSTOM_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis de Similitud Personalizado</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .article-selector { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #28a745; }
        .article-list { max-height: 300px; overflow-y: auto; border: 1px solid #ddd; border-radius: 5px; padding: 10px; }
        .article-item { padding: 10px; margin: 5px 0; border: 1px solid #eee; border-radius: 5px; cursor: pointer; transition: background 0.3s; }
        .article-item:hover { background: #e9ecef; }
        .article-item.selected { background: #d4edda; border-color: #28a745; }
        .article-title { font-weight: bold; margin-bottom: 5px; }
        .article-meta { font-size: 0.9em; color: #666; }
        .btn { background: #28a745; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }
        .btn:hover { background: #218838; }
        .btn-secondary { background: #6c757d; }
        .btn-secondary:hover { background: #5a6268; }
        .selection-summary { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ffc107; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Análisis de Similitud Personalizado</h1>
            <p>Selecciona dos artículos para comparar</p>
        </div>

        {% if articles %}
        <div class="article-selector">
            <h3>📄 Artículos Disponibles ({{ articles|length }})</h3>
            <p>Selecciona dos artículos haciendo clic en ellos:</p>
            <div class="article-list" id="article-list">
                {% for article in articles %}
                <div class="article-item" data-id="{{ article.id }}" onclick="selectArticle(this)">
                    <div class="article-title">{{ article.title[:80] }}{% if article.title|length > 80 %}...{% endif %}</div>
                    <div class="article-meta">
                        <strong>ID:</strong> {{ article.id }} |
                        <strong>Año:</strong> {{ article.year }} |
                        <strong>Autores:</strong> {{ article.authors[:50] }}{% if article.authors|length > 50 %}...{% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="selection-summary" id="selection-summary" style="display: none;">
            <h4>📋 Artículos Seleccionados:</h4>
            <div id="selected-articles"></div>
        </div>

        <form method="post" action="/execute_similarity_custom" id="similarity-form" style="display: none;">
            <input type="hidden" name="article1_id" id="article1_id">
            <input type="hidden" name="article2_id" id="article2_id">
            <button type="submit" class="btn">🚀 Ejecutar Análisis de Similitud</button>
        </form>
        {% else %}
        <div class="article-selector">
            <h3>❌ No se encontraron artículos</h3>
            <p>No hay artículos disponibles para el análisis. Asegúrate de haber ejecutado "Descargar y Unificar Datos" primero.</p>
        </div>
        {% endif %}

        <div style="text-align: center; margin-top: 30px;">
            <a href="/analysis_tools" class="btn btn-secondary">⬅️ Volver a Herramientas</a>
        </div>
    </div>

    <script>
        let selectedArticles = [];

        function selectArticle(element) {
            const articleId = element.getAttribute('data-id');
            const isSelected = element.classList.contains('selected');

            if (isSelected) {
                // Deseleccionar
                element.classList.remove('selected');
                selectedArticles = selectedArticles.filter(id => id !== articleId);
            } else {
                // Seleccionar (máximo 2)
                if (selectedArticles.length < 2) {
                    element.classList.add('selected');
                    selectedArticles.push(articleId);
                } else {
                    alert('Solo puedes seleccionar 2 artículos para comparar.');
                    return;
                }
            }

            updateSelectionSummary();
        }

        function updateSelectionSummary() {
            const summary = document.getElementById('selection-summary');
            const selectedDiv = document.getElementById('selected-articles');
            const form = document.getElementById('similarity-form');

            if (selectedArticles.length === 0) {
                summary.style.display = 'none';
                form.style.display = 'none';
                return;
            }

            summary.style.display = 'block';
            selectedDiv.innerHTML = '';

            selectedArticles.forEach((id, index) => {
                const articleElement = document.querySelector(`[data-id="${id}"]`);
                const title = articleElement.querySelector('.article-title').textContent;
                selectedDiv.innerHTML += `<p><strong>Artículo ${index + 1}:</strong> ${title} (ID: ${id})</p>`;
            });

            if (selectedArticles.length === 2) {
                form.style.display = 'block';
                document.getElementById('article1_id').value = selectedArticles[0];
                document.getElementById('article2_id').value = selectedArticles[1];
            } else {
                form.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

RESULTS_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados de Ejecución</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .results-card {
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .output-section {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            max-height: 600px;
            overflow-y: auto;
        }
        .image-section {
            text-align: center;
            margin: 20px 0;
        }
        .image-section img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .btn {
            background: #667eea;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            text-decoration: none;
            display: inline-block;
            transition: background 0.3s ease;
            margin: 5px;
        }
        .btn:hover {
            background: #5a6fd8;
        }
        .btn-secondary {
            background: #6c757d;
        }
        .btn-secondary:hover {
            background: #5a6268;
        }
        .status {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: bold;
        }
        .status.running {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        .status.completed {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .loading {
            text-align: center;
            padding: 40px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-bottom: 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Resultados de Ejecución</h1>
            <p>{{ title }}</p>
        </div>

        <div class="results-card">
            {% if status == 'running' %}
            <div class="loading">
                <div class="spinner"></div>
                <h3>⏳ Ejecutando...</h3>
                <p>Por favor espere mientras se procesa la solicitud.</p>
                <p>Esta operación puede tomar varios minutos.</p>
            </div>
            {% elif status == 'completed' %}
            <div class="status completed">✅ Ejecución Completada</div>
            {% elif status == 'error' %}
            <div class="status error">❌ Error en la Ejecución</div>
            {% endif %}

            {% if output %}
            <h3>📝 Salida del Programa:</h3>
            <div class="output-section">{{ output }}</div>
            {% endif %}

            {% if images %}
            <h3>📊 Gráficos Generados:</h3>
            {% for image in images %}
            <div class="image-section">
                <img src="data:image/png;base64,{{ image }}" alt="Gráfico generado">
            </div>
            {% endfor %}
            {% endif %}

            <div style="text-align: center; margin-top: 30px;">
                <a href="/" class="btn">🏠 Volver al Menú Principal</a>
                <button onclick="location.reload()" class="btn btn-secondary">🔄 Actualizar Resultados</button>
            </div>
        </div>
    </div>

    <script>
        // Auto-refresh para ver resultados en tiempo real
        {% if status == 'running' %}
        setTimeout(function() {
            location.reload();
        }, 3000);
        {% endif %}
    </script>
</body>
</html>
"""

DOWNLOAD_UNIFY_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Descargar y Unificar Datos</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 1em; }
        .btn { background: #28a745; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; width: 100%; }
        .btn:hover { background: #218838; }
        .btn-secondary { background: #6c757d; margin-top: 10px; }
        .btn-secondary:hover { background: #5a6268; }
        .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Descargar y Unificar Datos</h1>
            <p>Configure los parámetros de descarga</p>
        </div>

        <div class="info">
            <strong>ℹ️ Información:</strong> Esta función descargará artículos de IEEE y ScienceDirect, luego los unificará en un solo archivo.
            Use 0 para descargar todas las páginas disponibles.
        </div>

        <form method="post" action="/execute_download_unify">
            <div class="form-group">
                <label for="num_ieee">📄 Páginas de IEEE a descargar (0 = todas):</label>
                <input type="number" id="num_ieee" name="num_ieee" min="0" value="0" required>
            </div>

            <div class="form-group">
                <label for="num_science">🔬 Páginas de ScienceDirect a descargar (0 = todas):</label>
                <input type="number" id="num_science" name="num_science" min="0" value="0" required>
            </div>

            <button type="submit" class="btn">🚀 Iniciar Descarga y Unificación</button>
        </form>

        <div style="text-align: center; margin-top: 20px;">
            <a href="/" class="btn btn-secondary">⬅️ Volver al Menú Principal</a>
        </div>
    </div>
</body>
</html>
"""

VISUALIZATIONS_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizaciones Avanzadas</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .option { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #28a745; }
        .btn { background: #28a745; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; width: 100%; }
        .btn:hover { background: #218838; }
        .btn-secondary { background: #6c757d; margin-top: 10px; }
        .btn-secondary:hover { background: #5a6268; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Visualizaciones Avanzadas</h1>
            <p>Selecciona el tipo de análisis a realizar</p>
        </div>

        <div class="option">
            <h3>🔄 Utilizar 100 artículos aleatorios</h3>
            <p>Generará un nuevo fichero simplificado con una muestra aleatoria de 100 artículos.</p>
            <form method="post" action="/execute">
                <input type="hidden" name="action" value="visualizations_random">
                <button type="submit" class="btn">🎲 Ejecutar con Muestra Aleatoria</button>
            </form>
        </div>

        <div class="option">
            <h3>📁 Utilizar artículos ya cargados</h3>
            <p>Procesará los datos existentes en el fichero simplificado sin generar nueva muestra.</p>
            <form method="post" action="/execute">
                <input type="hidden" name="action" value="visualizations_existing">
                <button type="submit" class="btn">📊 Ejecutar con Datos Existentes</button>
            </form>
        </div>

        <div style="text-align: center; margin-top: 20px;">
            <a href="/" class="btn btn-secondary">⬅️ Volver al Menú Principal</a>
        </div>
    </div>
</body>
</html>
"""

SEGUIMIENTO2_P2_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seguimiento 2 Punto 2 - Configuración</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 1em; }
        .form-group input:focus { outline: none; border-color: #667eea; }
        .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #007bff; }
        .btn { background: #28a745; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; width: 100%; }
        .btn:hover { background: #218838; }
        .btn-secondary { background: #6c757d; margin-top: 10px; }
        .btn-secondary:hover { background: #5a6268; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ Seguimiento 2 Punto 2</h1>
            <p>Análisis de Grafos de Coocurrencia</p>
        </div>

        <div class="info">
            <strong>ℹ️ Información:</strong> Este análisis genera grafos de coocurrencia de términos a partir de los abstracts.
            Configure los parámetros para personalizar el análisis.
        </div>

        <form method="post" action="/execute_seguimiento2_p2">
            <div class="form-group">
                <label for="max_documents">📄 Número máximo de documentos a procesar:</label>
                <input type="number" id="max_documents" name="max_documents" min="10" max="1000" value="100" required>
                <small style="color: #666;">Mínimo: 10, Máximo: 1000. Más documentos = análisis más completo pero más lento.</small>
            </div>

            <div class="form-group">
                <label for="min_cooccurrence">🔗 Mínimo de coocurrencias:</label>
                <input type="number" id="min_cooccurrence" name="min_cooccurrence" min="1" max="10" value="1" required>
                <small style="color: #666;">Mínimo: 1, Máximo: 10. Valores más altos = grafos más limpios pero menos conexiones.</small>
            </div>

            <button type="submit" class="btn">🚀 Ejecutar Análisis de Grafos</button>
        </form>

        <div style="text-align: center; margin-top: 20px;">
            <a href="/additional_analysis" class="btn btn-secondary">⬅️ Volver a Análisis Adicionales</a>
        </div>
    </div>
</body>
</html>
"""

# Directorio temporal para almacenar resultados de ejecución
TEMP_RESULTS_DIR = os.path.join(tempfile.gettempdir(), 'flask_bibliometric_results')
os.makedirs(TEMP_RESULTS_DIR, exist_ok=True)

# Crear directorio de output si no existe
output_dir = os.path.join(project_root, 'output')
os.makedirs(output_dir, exist_ok=True)

print(f"Directorio temporal de resultados: {TEMP_RESULTS_DIR}")
print(f"Directorio de output: {output_dir}")
print(f"Directorio src: {src_path}")
print(f"Directorio proyecto: {project_root}")

def save_execution_result(execution_id, result_data):
    """Guarda el resultado de una ejecución en un archivo temporal"""
    try:
        result_file = os.path.join(TEMP_RESULTS_DIR, f"{execution_id}.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False)
        print(f"Resultado guardado exitosamente: {result_file}")
        print(f"Estado: {result_data.get('status', 'unknown')}")
        print(f"Longitud output: {len(result_data.get('output', ''))}")
        print(f"Número de imágenes: {len(result_data.get('images', []))}")
    except Exception as e:
        print(f"Error guardando resultado: {e}")

def load_execution_result(execution_id):
    """Carga el resultado de una ejecución desde un archivo temporal"""
    try:
        result_file = os.path.join(TEMP_RESULTS_DIR, f"{execution_id}.json")
        print(f"Intentando cargar resultado desde: {result_file}")
        if os.path.exists(result_file):
            print(f"Archivo existe, cargando...")
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Resultado cargado exitosamente")
            return data
        else:
            print(f"Archivo no existe: {result_file}")
            # Listar archivos disponibles
            if os.path.exists(TEMP_RESULTS_DIR):
                files = os.listdir(TEMP_RESULTS_DIR)
                print(f"Archivos disponibles en {TEMP_RESULTS_DIR}: {files}")
    except Exception as e:
        print(f"Error cargando resultado: {e}")
    return None

def run_function_with_capture(func, execution_id, *args, **kwargs):
    """Ejecuta una función capturando su salida stdout/stderr"""
    def wrapper():
        # Marcar como ejecutándose
        save_execution_result(execution_id, {
            'output': 'Ejecutando...',
            'images': [],
            'status': 'running'
        })

        # Capturar salida
        output_buffer = io.StringIO()
        images = []

        try:
            print(f"Iniciando ejecución de {execution_id}")

            # Verificar si hay datos disponibles antes de ejecutar
            output_dir = os.path.join(project_root, 'output')
            bib_files = []
            if os.path.exists(output_dir):
                bib_files = [f for f in os.listdir(output_dir) if f.endswith('.bib')]
                print(f"Archivos .bib encontrados: {bib_files}")

            if not bib_files and execution_id.split('_')[0] not in ['download', 'jupyter']:
                # Si no hay archivos .bib y no es descarga/jupyter, mostrar mensaje de error
                error_msg = """❌ No se encontraron datos bibliográficos para procesar.

Para usar las funciones de análisis, primero debe:

1. 📥 Ejecutar "Descargar y Unificar Datos" para obtener artículos de IEEE y ScienceDirect
2. 🔄 Unificar y limpiar los datos descargados

Los archivos .bib resultantes se guardarán en el directorio 'output/' y serán necesarios para:
- Análisis de similitud textual
- Análisis de frecuencia de palabras
- Clustering y visualizaciones
- Todos los seguimientos

Por favor, ejecute primero la descarga de datos desde el menú principal."""
                print("No hay datos disponibles")
                result_data = {
                    'output': error_msg,
                    'images': [],
                    'status': 'error'
                }
                save_execution_result(execution_id, result_data)
                return

            # Limpiar imágenes anteriores si no es una descarga
            if execution_id.split('_')[0] not in ['download']:
                if os.path.exists(output_dir):
                    for file in os.listdir(output_dir):
                        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.svg')):
                            try:
                                os.remove(os.path.join(output_dir, file))
                                print(f"Limpiada imagen anterior: {file}")
                            except Exception as e:
                                print(f"Error limpiando {file}: {e}")

            # Registrar imágenes existentes antes de la ejecución
            existing_images = set()
            if os.path.exists(output_dir):
                existing_images = set(f for f in os.listdir(output_dir)
                                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg')))

            with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
                result = func(*args, **kwargs)
            print(f"Ejecución completada de {execution_id}")

            # Buscar TODAS las imágenes generadas durante esta ejecución
            if os.path.exists(output_dir):
                print(f"Buscando imágenes en {output_dir}")
                all_images = [f for f in os.listdir(output_dir)
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg'))]

                print(f"Imágenes encontradas: {all_images}")

                for file in sorted(all_images):  # Ordenar para consistencia
                    image_path = os.path.join(output_dir, file)
                    print(f"Procesando imagen: {file}")
                    try:
                        # Verificar que el archivo existe y tiene contenido
                        if os.path.exists(image_path) and os.path.getsize(image_path) > 0:
                            with open(image_path, 'rb') as img_file:
                                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                                images.append(img_data)
                                print(f"✅ Imagen {file} convertida a base64 ({len(img_data)} chars)")
                        else:
                            print(f"⚠️ Imagen {file} está vacía o no existe")
                    except Exception as e:
                        output_buffer.write(f"\nError cargando imagen {file}: {e}\n")
                        print(f"❌ Error cargando imagen {file}: {e}")

            result_data = {
                'output': output_buffer.getvalue(),
                'images': images,
                'status': 'completed'
            }
            save_execution_result(execution_id, result_data)
            print(f"Resultado guardado para {execution_id}")

        except Exception as e:
            import traceback
            error_msg = f"Error ejecutando función: {str(e)}\n{traceback.format_exc()}"
            print(f"Error en {execution_id}: {error_msg}")
            result_data = {
                'output': output_buffer.getvalue() + error_msg,
                'images': images,
                'status': 'error'
            }
            save_execution_result(execution_id, result_data)

    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()
    return thread

def run_function_in_thread(func, *args, **kwargs):
    """Ejecuta una función en un hilo separado para no bloquear la interfaz web (legacy)"""
    def wrapper():
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Error ejecutando función: {e}")

    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()
    return thread

@app.route('/')
def index():
    # Determinar el estado basado en si hay módulos disponibles
    if IMPORTS_OK:
        status = 'ready'
    elif any(IMPORTED_MODULES.values()):  # Si al menos algunos módulos están disponibles
        status = 'ready'  # Permitir que funcione con módulos parciales
    else:
        status = 'error'
    
    # Verificar si hay datos disponibles
    output_dir = os.path.join(project_root, 'output')
    bib_files = []
    if os.path.exists(output_dir):
        bib_files = [f for f in os.listdir(output_dir) if f.endswith('.bib')]
    data_status = 'ready' if bib_files else 'no_data'

    return render_template_string(MAIN_TEMPLATE, status=status, data_status=data_status)

@app.route('/analysis_tools')
def analysis_tools():
    return render_template_string(ANALYSIS_TOOLS_TEMPLATE)

@app.route('/similarity_custom')
def similarity_custom():
    # Cargar artículos disponibles
    articles = []
    error_message = None
    
    try:
        from procesamiento.Requerimiento2.requerimiento2Ejecutable import find_bibtex_file, load_bibtex_abstracts

        bibtex_path = find_bibtex_file()
        if bibtex_path:
            articles_df = load_bibtex_abstracts(bibtex_path)
            if not articles_df.empty:
                # Limitar a primeros 100 artículos para mejor rendimiento
                articles_df = articles_df[:100] if len(articles_df) > 100 else articles_df
                # Convertir DataFrame a lista de diccionarios para el template
                for _, row in articles_df.iterrows():
                    articles.append({
                        'id': str(row['id']),
                        'title': str(row['title']),
                        'authors': str(row.get('authors', '')),
                        'year': str(row.get('year', '')),
                        'abstract': str(row.get('abstract', ''))
                    })
            else:
                error_message = "El archivo BibTeX está vacío o no contiene artículos válidos."
        else:
            error_message = "No se encontró archivo BibTeX unificado. Ejecute 'Unificar y Filtrar Datos' primero o suba archivos .bib al directorio output/."
    except ImportError as e:
        error_message = f"Error importando módulos: {e}. Verifique que todas las dependencias estén instaladas."
        print(f"Error cargando artículos: {e}")
    except Exception as e:
        error_message = f"Error cargando artículos: {e}"
        print(f"Error cargando artículos: {e}")
        import traceback
        traceback.print_exc()

    # Si hay error, mostrar mensaje en el template
    if error_message and not articles:
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error - Análisis de Similitud</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 20px; border-radius: 5px; margin: 20px 0; }
                .btn { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }
                .btn:hover { background: #5a6fd8; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ Error al Cargar Artículos</h1>
                <div class="error">
                    <strong>Error:</strong> {{ error_message }}
                </div>
                <p><strong>💡 Soluciones:</strong></p>
                <ul>
                    <li>Ejecute "Unificar y Filtrar Datos" desde el menú principal para generar archivos BibTeX unificados</li>
                    <li>O suba archivos .bib manualmente al directorio output/</li>
                    <li>Verifique que los archivos .bib tengan el formato correcto</li>
                </ul>
                <a href="/" class="btn">⬅️ Volver al Menú Principal</a>
                <a href="/analysis_tools" class="btn">🔬 Volver a Herramientas</a>
            </div>
        </body>
        </html>
        """, error_message=error_message)

    return render_template_string(SIMILARITY_CUSTOM_TEMPLATE, articles=articles)

@app.route('/additional_analysis')
def additional_analysis():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Análisis Adicionales</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 30px; }
            .option { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #28a745; }
            .btn { background: #28a745; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }
            .btn:hover { background: #218838; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #5a6268; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 Análisis Adicionales</h1>
                <p>Seguimientos y análisis complementarios</p>
            </div>

            <div class="option">
                <h3>📈 Seguimiento 1 - Punto 1</h3>
                <p>Análisis correspondiente al seguimiento 1 punto 1.</p>
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="seguimiento1_p1">
                    <button type="submit" class="btn">▶️ Ejecutar</button>
                </form>
            </div>

            <div class="option">
                <h3>📊 Seguimiento 1 - Punto 3</h3>
                <p>Análisis correspondiente al seguimiento 1 punto 3.</p>
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="seguimiento1_p3">
                    <button type="submit" class="btn">▶️ Ejecutar</button>
                </form>
            </div>

            <div class="option">
                <h3>🔗 Seguimiento 2 - Punto 1</h3>
                <p>Algoritmo relacionado al seguimiento 2 punto 1.</p>
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="seguimiento2_p1">
                    <button type="submit" class="btn">▶️ Ejecutar</button>
                </form>
            </div>

            <div class="option">
                <h3>⚡ Seguimiento 2 - Punto 2</h3>
                <p>Análisis de grafos de coocurrencia con parámetros configurables.</p>
                <a href="/seguimiento2_p2_config" class="btn">⚙️ Configurar y Ejecutar</a>
            </div>

            <div class="option">
                <h3>🔍 Analizador de Artículos</h3>
                <p>Análisis avanzado de artículos con muestra aleatoria.</p>
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="article_analyzer">
                    <button type="submit" class="btn">▶️ Ejecutar</button>
                </form>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <a href="/" class="btn btn-secondary">⬅️ Volver al Menú Principal</a>
            </div>
        </div>
    </div>
    </body>
    </html>
    """)

@app.route('/execute', methods=['POST'])
def execute():
    action = request.form.get('action')

    # Verificar si el módulo específico está disponible en lugar de verificar todos
    # Nota: similarity_analysis y similarity_custom usan funciones definidas directamente en web_app.py
    # por lo que no dependen de la importación de mainRequerimiento2
    module_availability = {
        'jupyter': IMPORTED_MODULES.get('mainJupyter') is not None,
        'unify_only': IMPORTED_MODULES.get('unificar') is not None,  # Unificación disponible
        'similarity_analysis': True,  # Siempre disponible (usa funciones locales)
        'category_analysis': IMPORTED_MODULES.get('mainEjecutableRequerimiento3') is not None,
        'clustering': IMPORTED_MODULES.get('mainRequerimiento4') is not None,
        'visualizations_random': IMPORTED_MODULES.get('mainAnalizador') is not None,
        'visualizations_existing': IMPORTED_MODULES.get('mainRequerimiento5') is not None,
        'seguimiento1_p1': IMPORTED_MODULES.get('mainSeguimiento1') is not None,
        'seguimiento1_p3': IMPORTED_MODULES.get('seguimiento1Punto3') is not None,
        'seguimiento2_p1': IMPORTED_MODULES.get('ejecutarGrafoDirigido') is not None,
        'seguimiento2_p2': IMPORTED_MODULES.get('ejecutarEjecutar') is not None,
        'article_analyzer': IMPORTED_MODULES.get('mainAnalizador') is not None,
    }
    
    # Verificar si el módulo requerido está disponible (unify_only y similarity_analysis se manejan después)
    if action not in ['unify_only', 'similarity_analysis'] and action in module_availability and not module_availability[action]:
        flash(f'Error: El módulo requerido para "{action}" no está disponible. Verifique los logs del contenedor Docker para más detalles sobre qué módulos faltan.', 'error')
        return redirect(url_for('index'))

    try:
        execution_id = f"{action}_{int(time.time())}"

        if action == 'jupyter':
            flash('⚠️ Jupyter Notebook no está disponible en la versión web. Use el modo consola local ejecutando: python main.py con requirements-full.txt instalado.', 'error')
            return redirect(url_for('index'))

        elif action == 'unify_only':
            # Solo unificar archivos (sin descargar)
            flash('🔄 Unificando y filtrando archivos BibTeX...', 'success')
            
            def unify_process():
                """Proceso de unificación sin descarga"""
                from procesamiento.unifyBibtext import unificar
                print("Unificando y filtrando archivos BibTeX...")
                unificar()
                print("Proceso completado. Archivos unificados y duplicados guardados en 'output/'.")
            
            run_function_with_capture(unify_process, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'similarity_analysis':
            flash('🎯 Ejecutando análisis de similitud textual (Primer vs Último documento)...', 'success')
            run_function_with_capture(mainRequerimiento2_first_last_web, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'category_analysis':
            flash('📈 Ejecutando análisis de categoría...', 'success')
            run_function_with_capture(mainEjecutableRequerimiento3, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'clustering':
            flash('🌳 Ejecutando análisis de clustering...', 'success')
            run_function_with_capture(mainRequerimiento4, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'visualizations_random':
            flash('📊 Ejecutando visualizaciones con muestra aleatoria...', 'success')
            run_function_with_capture(mainAnalizador, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'visualizations_existing':
            flash('📊 Ejecutando visualizaciones con datos existentes...', 'success')
            run_function_with_capture(mainRequerimiento5, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'seguimiento1_p1':
            flash('📈 Ejecutando seguimiento 1 punto 1...', 'success')
            run_function_with_capture(mainSeguimiento1, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'seguimiento1_p3':
            flash('📊 Ejecutando seguimiento 1 punto 3...', 'success')
            run_function_with_capture(seguimiento1Punto3, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'seguimiento2_p1':
            flash('🔗 Ejecutando seguimiento 2 punto 1...', 'success')
            run_function_with_capture(ejecutarGrafoDirigido, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'seguimiento2_p2':
            flash('⚡ Ejecutando seguimiento 2 punto 2...', 'success')
            run_function_with_capture(ejecutarEjecutar_web, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

        elif action == 'article_analyzer':
            flash('🔍 Ejecutando analizador de artículos...', 'success')
            run_function_with_capture(mainAnalizador, execution_id)
            return redirect(url_for('results', execution_id=execution_id))

    except Exception as e:
        flash(f'❌ Error ejecutando acción: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/execute_similarity_custom', methods=['POST'])
def execute_similarity_custom():
    try:
        article1_id = request.form.get('article1_id')
        article2_id = request.form.get('article2_id')

        if not article1_id or not article2_id:
            flash('❌ Debes seleccionar dos artículos para comparar.', 'error')
            return redirect(url_for('similarity_custom'))

        # Crear ID único para esta ejecución
        execution_id = f"similarity_custom_{int(time.time())}"

        def custom_similarity_analysis():
            """Análisis de similitud personalizado con artículos seleccionados"""
            import os
            import sys
            import pandas as pd
            import warnings
            warnings.filterwarnings('ignore')

            # Configurar rutas
            current_dir = os.path.dirname(os.path.abspath(__file__))
            possible_src_paths = [
                os.path.join(current_dir, '..', '..', '..', 'src'),
                os.path.join(current_dir, '..', '..', 'src'),
                os.path.join(os.getcwd(), 'src'),
                os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'src'))
            ]

            src_path = None
            for path in possible_src_paths:
                if os.path.exists(path):
                    src_path = os.path.abspath(path)
                    break

            if src_path is None:
                print("❌ ERROR: No se pudo encontrar el directorio 'src'")
                return

            project_root = os.path.dirname(src_path)

            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            if project_root not in sys.path:
                sys.path.insert(0, project_root)

            print("=" * 80)
            print("                🎯 ANÁLISIS DE SIMILITUD PERSONALIZADO")
            print("=" * 80)
            print(f"Comparando artículos: {article1_id} vs {article2_id}")
            print("=" * 80)

            try:
                # Importar funciones necesarias
                from procesamiento.Requerimiento2.requerimiento2Ejecutable import (
                    load_bibtex_abstracts, run_similarity_analysis, display_article_info,
                    show_detailed_analysis, create_visualization, find_bibtex_file
                )

                # Buscar archivo BibTeX
                bibtex_path = find_bibtex_file()
                if not bibtex_path:
                    print("\n❌ No se encontró archivo BibTeX unificado")
                    print("Ejecute primero el Requerimiento 1 para generar el archivo unificado")
                    return

                print(f"\n📁 Archivo BibTeX encontrado: {os.path.basename(bibtex_path)}")

                # Cargar abstracts
                abstracts = load_bibtex_abstracts(bibtex_path)
                if abstracts.empty:
                    print("❌ No se pudieron cargar los abstracts")
                    return

                print(f"✅ Se cargaron {len(abstracts)} abstracts exitosamente")

                # Buscar los artículos seleccionados en el DataFrame
                article1_row = abstracts[abstracts['id'] == article1_id]
                article2_row = abstracts[abstracts['id'] == article2_id]

                if article1_row.empty or article2_row.empty:
                    print(f"❌ No se pudieron encontrar los artículos seleccionados: {article1_id}, {article2_id}")
                    return

                abstract1_data = {
                    'title': str(article1_row.iloc[0]['title']),
                    'abstract': str(article1_row.iloc[0]['abstract']),
                    'year': str(article1_row.iloc[0]['year'])
                }
                abstract2_data = {
                    'title': str(article2_row.iloc[0]['title']),
                    'abstract': str(article2_row.iloc[0]['abstract']),
                    'year': str(article2_row.iloc[0]['year'])
                }

                print(f"📄 Artículo 1: {abstract1_data['title'][:60]}...")
                print(f"📄 Artículo 2: {abstract2_data['title'][:60]}...")

                # Mostrar información básica
                print(f"\n📊 Información del Artículo 1:")
                print(f"   ID: {article1_id}")
                print(f"   Título: {abstract1_data['title'][:50]}...")
                print(f"   Año: {abstract1_data['year']}")
                print(f"   Longitud abstract: {len(abstract1_data['abstract'])} caracteres")

                print(f"\n📊 Información del Artículo 2:")
                print(f"   ID: {article2_id}")
                print(f"   Título: {abstract2_data['title'][:50]}...")
                print(f"   Año: {abstract2_data['year']}")
                print(f"   Longitud abstract: {len(abstract2_data['abstract'])} caracteres")

                # Ejecutar análisis de similitud
                print("\n🔍 Ejecutando análisis de similitud de 6 algoritmos...")
                analyzer = run_similarity_analysis(abstract1_data, abstract2_data)
                print("✅ Análisis de similitud completado")

                # Mostrar resultados detallados
                print("\n📈 RESULTADOS DETALLADOS:")
                show_detailed_analysis(analyzer)

                # Generar visualización
                print("\n🎨 Generando gráfico de comparación...")
                create_visualization(analyzer.compare_all())
                print("✅ Gráfico generado exitosamente")

                print("\n🎯 Análisis de similitud personalizado completado exitosamente")
                print("   Los resultados y gráficos están disponibles en la interfaz web")

            except Exception as e:
                print(f"❌ Error en el análisis personalizado: {e}")
                import traceback
                traceback.print_exc()

        flash('🎯 Ejecutando análisis de similitud personalizado...', 'success')
        run_function_with_capture(custom_similarity_analysis, execution_id)

        return redirect(url_for('results', execution_id=execution_id))

    except Exception as e:
        flash(f'❌ Error iniciando análisis personalizado: {str(e)}', 'error')
        return redirect(url_for('similarity_custom'))

@app.route('/download_unify')
def download_unify():
    # Redirigir con mensaje de error - solo descarga no disponible en web
    # La unificación está disponible desde el menú principal
    flash('⚠️ La descarga de documentos no está disponible en la versión web. Use el modo consola local con requirements-full.txt instalado. La unificación de archivos está disponible desde el menú principal (opción 1b).', 'error')
    return redirect(url_for('index'))

@app.route('/execute_download_unify', methods=['POST'])
def execute_download_unify():
    # Funcionalidad deshabilitada en versión web
    flash('⚠️ La descarga de documentos no está disponible en la versión web. Esta funcionalidad requiere Selenium y ChromeDriver que no están disponibles en el despliegue web. Use el modo consola local ejecutando: python main.py con requirements-full.txt instalado.', 'error')
    return redirect(url_for('index'))

@app.route('/seguimiento2_p2_config')
def seguimiento2_p2_config():
    return render_template_string(SEGUIMIENTO2_P2_TEMPLATE)

@app.route('/execute_seguimiento2_p2', methods=['POST'])
def execute_seguimiento2_p2():
    if IMPORTED_MODULES.get('ejecutarEjecutar') is None:
        flash('Error: El módulo de Seguimiento 2 Punto 2 no está disponible. Verifique los logs del contenedor Docker.', 'error')
        return redirect(url_for('seguimiento2_p2_config'))

    try:
        max_documents = int(request.form.get('max_documents', 100))
        min_cooccurrence = int(request.form.get('min_cooccurrence', 1))

        # Validar parámetros
        if max_documents < 10 or max_documents > 1000:
            flash('❌ El número de documentos debe estar entre 10 y 1000.', 'error')
            return redirect(url_for('seguimiento2_p2_config'))

        if min_cooccurrence < 1 or min_cooccurrence > 10:
            flash('❌ El mínimo de coocurrencias debe estar entre 1 y 10.', 'error')
            return redirect(url_for('seguimiento2_p2_config'))

        # Crear ID único para esta ejecución
        execution_id = f"seguimiento2_p2_{int(time.time())}"

        def custom_seguimiento2_p2():
            """Seguimiento 2 punto 2 con parámetros personalizados"""
            import os
            import sys
            import subprocess

            print("=" * 80)
            print("                ⚡ SEGUIMIENTO 2 PUNTO 2: ANÁLISIS DE GRAFO (PERSONALIZADO)")
            print("=" * 80)
            print(f"Parámetros: MAX_DOCUMENTS={max_documents}, MIN_COOCCURRENCE={min_cooccurrence}")
            print("=" * 80)

            try:
                # Configurar rutas
                current_dir = os.path.dirname(os.path.abspath(__file__))
                possible_src_paths = [
                    os.path.join(current_dir, '..', '..', '..', 'src'),
                    os.path.join(current_dir, '..', '..', 'src'),
                    os.path.join(os.getcwd(), 'src'),
                    os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'src'))
                ]

                src_path = None
                for path in possible_src_paths:
                    if os.path.exists(path):
                        src_path = os.path.abspath(path)
                        break

                if src_path is None:
                    print("❌ ERROR: No se pudo encontrar el directorio 'src'")
                    return

                project_root = os.path.dirname(src_path)

                if src_path not in sys.path:
                    sys.path.insert(0, src_path)
                if project_root not in sys.path:
                    sys.path.insert(0, project_root)

                # Ejecutar el script main_fast.py con parámetros modificados
                script_path = os.path.join(project_root, 'procesamiento', 'Seguimiento2', 'punto2', 'main_fast.py')

                if os.path.exists(script_path):
                    print(f"📊 Iniciando análisis personalizado de {max_documents} documentos...")
                    print(f"⏱️  Tiempo estimado: {max_documents//50 + 1}-{max_documents//25 + 2} minutos")
                    print("🎨 Se generarán visualizaciones automáticamente\n")

                    # Modificar las variables globales en el script
                    # Leer el archivo y reemplazar las constantes
                    with open(script_path, 'r', encoding='utf-8') as f:
                        script_content = f.read()

                    # Reemplazar las constantes
                    script_content = script_content.replace(
                        'MAX_DOCUMENTS = 100  # Número de documentos a procesar (análisis rápido estándar)',
                        f'MAX_DOCUMENTS = {max_documents}  # Número de documentos a procesar (personalizado)'
                    )
                    script_content = script_content.replace(
                        'MIN_COOCCURRENCE = 1  # Mínimo de coocurrencias (aumenta para menos ruido)',
                        f'MIN_COOCCURRENCE = {min_cooccurrence}  # Mínimo de coocurrencias (personalizado)'
                    )

                    # Reemplazar la manipulación de rutas relativa con rutas absolutas
                    script_path_dir = os.path.dirname(script_path)
                    parent_parent_parent = os.path.abspath(os.path.join(script_path_dir, '..', '..', '..'))
                    script_content = script_content.replace(
                        'sys.path.insert(0, str(Path(__file__).parent.parent.parent))',
                        f'sys.path.insert(0, r"{parent_parent_parent}")'
                    )

                    # Crear un archivo temporal con las modificaciones
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
                        temp_file.write(script_content)
                        temp_script_path = temp_file.name

                    try:
                        # Ejecutar el script modificado
                        result = subprocess.run([sys.executable, temp_script_path],
                                              cwd=os.path.dirname(script_path),
                                              capture_output=True,
                                              text=True,
                                              timeout=600)  # 10 minutos timeout

                        # Mostrar salida
                        if result.stdout:
                            print("SALIDA DEL ANÁLISIS:")
                            print(result.stdout)

                        if result.stderr:
                            print("MENSAJES DE ERROR:")
                            print(result.stderr)

                        if result.returncode == 0:
                            print("\n✅ Análisis personalizado completado exitosamente")
                            print("📊 Los gráficos están disponibles en la interfaz web")
                        else:
                            print(f"\n❌ Error en el análisis personalizado (código {result.returncode})")

                    finally:
                        # Limpiar archivo temporal
                        try:
                            os.unlink(temp_script_path)
                        except:
                            pass

                else:
                    print(f"❌ Script no encontrado: {script_path}")

            except subprocess.TimeoutExpired:
                print("❌ El análisis personalizado tardó demasiado tiempo (timeout)")
            except Exception as e:
                print(f"❌ Error ejecutando el análisis personalizado: {e}")
                import traceback
                traceback.print_exc()

        flash(f'⚡ Ejecutando análisis personalizado (Documentos: {max_documents}, Coocurrencias mínimas: {min_cooccurrence})...', 'success')
        run_function_with_capture(custom_seguimiento2_p2, execution_id)

        return redirect(url_for('results', execution_id=execution_id))

    except Exception as e:
        flash(f'❌ Error iniciando análisis personalizado: {str(e)}', 'error')
        return redirect(url_for('seguimiento2_p2_config'))

@app.route('/visualizations')
def visualizations():
    return render_template_string(VISUALIZATIONS_TEMPLATE)

@app.route('/results/<execution_id>')
def results(execution_id):
    result = load_execution_result(execution_id)

    if result is None:
        return render_template_string(RESULTS_TEMPLATE,
                                    title="Resultado No Encontrado",
                                    status="error",
                                    output="No se encontraron resultados para esta ejecución.",
                                    images=[])

    return render_template_string(RESULTS_TEMPLATE,
                                title=f"Resultados - {execution_id.split('_')[0].title()}",
                                status=result.get('status', 'unknown'),
                                output=result.get('output', ''),
                                images=result.get('images', []))

@app.route('/test')
def test():
    """Endpoint de prueba para verificar funcionamiento"""
    output_dir = os.path.join(project_root, 'output')
    bib_files = []
    if os.path.exists(output_dir):
        bib_files = [f for f in os.listdir(output_dir) if f.endswith('.bib')]

    # Crear lista de módulos disponibles y faltantes
    available_modules = [name for name, func in IMPORTED_MODULES.items() if func is not None]
    missing_modules = [name for name, func in IMPORTED_MODULES.items() if func is None]

    return {
        'status': 'ok',
        'imports_ok': IMPORTS_OK,
        'available_modules': available_modules,
        'missing_modules': missing_modules,
        'bib_files': bib_files,
        'temp_dir': TEMP_RESULTS_DIR,
        'output_dir': output_dir,
        'project_root': project_root,
        'pythonpath': os.environ.get('PYTHONPATH', 'No definido'),
        'sys_path': sys.path[:5]  # Primeros 5 elementos de sys.path
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Iniciando servidor web en puerto {port}")
    print("🌐 Accede a http://localhost:8000")
    print(f"🧪 Endpoint de prueba: http://localhost:{port}/test")
    app.run(host='0.0.0.0', port=port, debug=False)
