#!/usr/bin/env python3
"""
Script para verificar e instalar todas las dependencias necesarias del proyecto.
Incluye verificación funcional de Kaleido (exportación de imágenes con Plotly).
"""

import importlib
import subprocess
import sys
import tempfile
import os


def check_installed(package_name):
    """Verifica si un paquete está instalado"""
    try:
        # Mapeo para paquetes cuyo nombre difiere del módulo importable
        module_map = {
            "python-dotenv": "dotenv",
            "scikit-learn": "sklearn",
            "kaleido": None,  # Kaleido no se importa, solo se verifica con pip
            "torch": "torch",
            "torchaudio": "torchaudio",
            "torchvision": "torchvision"
        }

        mod_name = module_map.get(package_name, package_name.replace("-", "_"))

        # Kaleido no tiene módulo importable, se verifica con pip show
        if mod_name is None:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0 and "Name:" in result.stdout

        importlib.import_module(mod_name)
        return True
    except ImportError:
        return False


def install_packages():
    """Verifica e instala las dependencias necesarias"""

    print("=" * 60)
    print("🔧 VERIFICADOR DE DEPENDENCIAS - Proyecto Análisis Textual")
    print("=" * 60)

    # Paquetes obligatorios
    required = {
        'pandas': 'Manipulación de datos',
        'scikit-learn': 'Algoritmos de ML',
        'nltk': 'Procesamiento de lenguaje natural',
        'bibtexparser': 'Lectura de archivos BibTeX',
        'requests': 'Solicitudes HTTP',
        'tqdm': 'Barras de progreso',
        'numpy': 'Cálculos numéricos',
        'matplotlib': 'Gráficas',
        'reportlab': 'Creación de PDFs',
        'plotly': 'Visualización interactiva',
        'geopy': 'Geocodificación de ubicaciones',
        'pycountry': 'Información de países',
        'wordcloud': 'Generación de nubes de palabras',
        'scipy': 'Cálculos científicos',
        'python-dotenv': 'Cargar variables de entorno',
        'selenium': 'Automatización de navegadores',
        'kaleido': 'Exportación de gráficos Plotly a imágenes'
    }

    # Paquetes opcionales (excluyendo torch para evitar reinstalación de versión pesada)
    optional = {
        'transformers': 'Modelos BERT',
        'sentence-transformers': 'Sentence-BERT para similitud semántica',
        'seaborn': 'Gráficas estadísticas'
    }

    # Combinar todos los paquetes
    all_packages = {**required, **optional}

    missing = []

    print("\n📦 Verificando dependencias necesarias...\n")

    # Paso 1: verificar instalación
    for pkg, desc in all_packages.items():
        if check_installed(pkg):
            print(f"  ✓ {pkg:<25} ✅  ({desc})")
        else:
            print(f"  ✗ {pkg:<25} ❌  No instalado ({desc})")
            missing.append(pkg)

    # Paso 2: instalar los paquetes faltantes
    if missing:
        print("\n⚠️  Instalando paquetes faltantes...\n")
        for package in missing:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-U", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"  ✓ {package} instalado correctamente")
            except Exception as e:
                print(f"  ❌ No se pudo instalar {package}: {type(e).__name__}")
    else:
        print("\n✅ Todas las dependencias estaban ya instaladas correctamente.")

    # Paso 3: verificación final
    print("\n🔍 Verificación final...\n")
    still_missing = [pkg for pkg in all_packages if not check_installed(pkg)]

    if still_missing:
        print("⚠️  Algunos paquetes no se pudieron instalar:")
        for pkg in still_missing:
            print(f"   - {pkg}")
        print("\nIntenta instalarlos manualmente con:")
        print(f"   pip install {' '.join(still_missing)}")
    else:
        print("🎉 Todas las dependencias instaladas correctamente")

    print("=" * 60)

    # Paso 4: verificación funcional de Kaleido
    verificar_kaleido_funcional()


def verificar_kaleido_funcional():
    """Verifica si Kaleido realmente puede exportar imágenes con Plotly"""
    print("\n🧪 Verificando funcionalidad de Kaleido...\n")
    try:
        import plotly.express as px
        import plotly.io as pio

        # Crear gráfico de prueba
        fig = px.scatter(x=[1, 2, 3], y=[3, 1, 2], title="Prueba Kaleido")
        temp_path = os.path.join(tempfile.gettempdir(), "kaleido_test.png")

        # Intentar exportar
        fig.write_image(temp_path)

        if os.path.exists(temp_path):
            print(f"✅ Kaleido funciona correctamente (archivo generado en {temp_path})")
            os.remove(temp_path)
        else:
            raise RuntimeError("Kaleido no generó el archivo de prueba.")
    except Exception as e:
        print(f"⚠️ Error al verificar Kaleido: {e}")
        print("🔁 Reinstalando Kaleido automáticamente...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "kaleido"])
            print("✅ Kaleido reinstalado correctamente.")
        except Exception as e2:
            print(f"❌ Falló la reinstalación de Kaleido: {type(e2).__name__}")


if __name__ == "__main__":
    install_packages()