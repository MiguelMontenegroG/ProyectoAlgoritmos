"""
Aplicación web Flask para el proyecto de análisis bibliométrico
Permite acceso web a todas las funcionalidades del proyecto
"""

import os
import sys
import subprocess
from flask import Flask, render_template_string, request, redirect, url_for, flash, session
import threading
import time

# Configurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importaciones del proyecto
try:
    from procesamiento.Requerimiento2.requerimiento2Ejecutable import mainRequerimiento2
    from procesamiento.Requerimiento3.FrecuenciaPalabra import mainEjecutableRequerimiento3
    from procesamiento.Requerimiento4.clutsteringDatos import mainRequerimiento4
    from procesamiento.Requerimiento5.requerimiento5Ejecutable import mainRequerimiento5
    from procesamiento.Seguimiento1.Punto1Seguimiento.mainSeguimiento1 import mainSeguimiento1
    from procesamiento.Seguimiento1.punto3Seguimiento.mainSeguimientoPunto3 import seguimiento1Punto3
    from procesamiento.Seguimiento2.Punto1.grafoDirigido import ejecutarGrafoDirigido
    from procesamiento.Seguimiento2.punto2.ejecutar import ejecutarEjecutar
    from extractores.analizador import mainAnalizador
    from procesamiento.unifyBibtext import unificar
    from instalarJupyter import mainJupyter
    IMPORTS_OK = True
except ImportError as e:
    print(f"Error importando módulos: {e}")
    IMPORTS_OK = False

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
            <div class="menu-item">
                <h3><span class="number">1</span>Descargar y Unificar Datos</h3>
                <p>Descarga automáticamente artículos de IEEE y ScienceDirect, luego unifica y limpia los datos BibTeX.</p>
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="download_unify">
                    <button type="submit" class="btn">🚀 Ejecutar</button>
                </form>
            </div>

            <div class="menu-item">
                <h3><span class="number">2</span>Herramientas de Análisis</h3>
                <p>Jupyter Notebook para análisis detallado o script interactivo de similitud textual.</p>
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
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="visualizations">
                    <button type="submit" class="btn">📊 Ejecutar</button>
                </form>
            </div>

            <div class="menu-item">
                <h3><span class="number">6-9</span>Análisis Adicionales</h3>
                <p>Seguimientos 1 y 2, análisis complementarios del proyecto.</p>
                <a href="/additional_analysis" class="btn">🔍 Ver Opciones</a>
            </div>
        </div>

        <div style="text-align: center; margin-top: 40px;">
            <p style="color: white; opacity: 0.8;">
                🚀 Desarrollado para el análisis bibliométrico de la Universidad del Quindío
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
        .btn { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }
        .btn:hover { background: #5a6fd8; }
        .btn-secondary { background: #6c757d; }
        .btn-secondary:hover { background: #5a6268; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔬 Herramientas de Análisis</h1>
            <p>Selecciona la herramienta que mejor se adapte a tus necesidades</p>
        </div>

        <div class="option">
            <h3>📓 Jupyter Notebook</h3>
            <p>Entorno interactivo completo con explicaciones detalladas paso a paso. Ideal para aprendizaje y análisis profundo.</p>
            <p><strong>Características:</strong> Celdas ejecutables, gráficos interactivos, documentación integrada</p>
            <form method="post" action="/execute">
                <input type="hidden" name="action" value="jupyter">
                <button type="submit" class="btn">🚀 Abrir Jupyter</button>
            </form>
        </div>

        <div class="option">
            <h3>🎯 Análisis de Similitud Textual</h3>
            <p>Script interactivo rápido para comparar abstracts usando 6 algoritmos de similitud.</p>
            <p><strong>Algoritmos:</strong> Levenshtein, Jaccard, Jaro-Winkler, TF-IDF+Coseno, BERT, Sentence-BERT</p>
            <form method="post" action="/execute">
                <input type="hidden" name="action" value="similarity_analysis">
                <button type="submit" class="btn">📊 Ejecutar Análisis</button>
            </form>
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <a href="/" class="btn btn-secondary">⬅️ Volver al Menú Principal</a>
        </div>
    </div>
</body>
</html>
"""

def run_function_in_thread(func, *args, **kwargs):
    """Ejecuta una función en un hilo separado para no bloquear la interfaz web"""
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
    if not IMPORTS_OK:
        status = 'error'
    else:
        status = 'ready'
    return render_template_string(MAIN_TEMPLATE, status=status)

@app.route('/analysis_tools')
def analysis_tools():
    return render_template_string(ANALYSIS_TOOLS_TEMPLATE)

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
                <p>Algoritmo relacionado al seguimiento 2 punto 2.</p>
                <form method="post" action="/execute">
                    <input type="hidden" name="action" value="seguimiento2_p2">
                    <button type="submit" class="btn">▶️ Ejecutar</button>
                </form>
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

    if not IMPORTS_OK:
        flash('Error: Los módulos del proyecto no están disponibles. Verifique la instalación.', 'error')
        return redirect(url_for('index'))

    try:
        if action == 'download_unify':
            flash('🚀 Iniciando descarga y unificación de datos...', 'success')
            # Nota: Esta función requiere interacción del usuario, por lo que no se puede ejecutar en web
            flash('⚠️ Esta función requiere interacción manual. Use la versión de consola.', 'error')

        elif action == 'jupyter':
            flash('📓 Iniciando Jupyter Notebook...', 'success')
            run_function_in_thread(mainJupyter)

        elif action == 'similarity_analysis':
            flash('🎯 Ejecutando análisis de similitud textual...', 'success')
            run_function_in_thread(mainRequerimiento2)

        elif action == 'category_analysis':
            flash('📈 Ejecutando análisis de categoría...', 'success')
            run_function_in_thread(mainEjecutableRequerimiento3)

        elif action == 'clustering':
            flash('🌳 Ejecutando análisis de clustering...', 'success')
            run_function_in_thread(mainRequerimiento4)

        elif action == 'visualizations':
            flash('📊 Ejecutando visualizaciones avanzadas...', 'success')
            run_function_in_thread(mainRequerimiento5)

        elif action == 'seguimiento1_p1':
            flash('📈 Ejecutando seguimiento 1 punto 1...', 'success')
            run_function_in_thread(mainSeguimiento1)

        elif action == 'seguimiento1_p3':
            flash('📊 Ejecutando seguimiento 1 punto 3...', 'success')
            run_function_in_thread(seguimiento1Punto3)

        elif action == 'seguimiento2_p1':
            flash('🔗 Ejecutando seguimiento 2 punto 1...', 'success')
            run_function_in_thread(ejecutarGrafoDirigido)

        elif action == 'seguimiento2_p2':
            flash('⚡ Ejecutando seguimiento 2 punto 2...', 'success')
            run_function_in_thread(ejecutarEjecutar)

        elif action == 'article_analyzer':
            flash('🔍 Ejecutando analizador de artículos...', 'success')
            run_function_in_thread(mainAnalizador)

        else:
            flash('❌ Acción no reconocida.', 'error')

    except Exception as e:
        flash(f'❌ Error ejecutando acción: {str(e)}', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Iniciando servidor web en puerto {port}")
    print("🌐 Accede a http://localhost:8000"    app.run(host='0.0.0.0', port=port, debug=False)