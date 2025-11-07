#!/usr/bin/env python3
"""
Script para verificar e instalar todas las dependencias necesarias del proyecto.
"""

import importlib
import subprocess
import sys

def check_installed(package_name):
    """Verifica si un paquete está instalado"""
    try:
        importlib.import_module(package_name)
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
        'selenium': 'Automatización de navegadores'
    }

    # Paquetes opcionales
    optional = {
        'transformers': 'Modelos BERT',
        'torch': 'Framework de deep learning',
        'sentence-transformers': 'Sentence-BERT para similitud semántica',
        'seaborn': 'Gráficas estadísticas'
    }

    # Combinar todos los paquetes que instala el script
    all_packages = {**required, **optional}

    missing = []

    print("\n📦 Verificando dependencias necesarias...\n")

    # 🔹 Paso 1: verificar cuáles están instaladas
    for pkg, desc in all_packages.items():
        # Algunos nombres de módulos difieren del paquete (guiones -> guiones bajos)
        mod_name = pkg.replace("-", "_")
        if check_installed(mod_name):
            print(f"  ✓ {pkg:<25} ✅  ({desc})")
        else:
            print(f"  ✗ {pkg:<25} ❌  No instalado ({desc})")
            missing.append(pkg)

    # 🔹 Paso 2: si todas están instaladas, terminar
    if not missing:
        print("\n✅ Todas las dependencias instaladas correctamente.")
        print("=" * 60)
        return

    # 🔹 Paso 3: instalar solo las que faltan
    print("\n⚠️  Se detectaron paquetes faltantes. Instalando...\n")
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

    # 🔹 Paso 4: verificar nuevamente después de instalar
    print("\n🔍 Verificación final...\n")
    still_missing = [pkg for pkg in missing if not check_installed(pkg.replace("-", "_"))]

    if still_missing:
        print("⚠️  Algunos paquetes no se pudieron instalar:")
        for pkg in still_missing:
            print(f"   - {pkg}")
        print("\nIntenta instalarlos manualmente:")
        print(f"   pip install {' '.join(still_missing)}")
    else:
        print("🎉 Todas las dependencias instaladas correctamente")

    print("=" * 60)


if __name__ == "__main__":
    install_packages()

