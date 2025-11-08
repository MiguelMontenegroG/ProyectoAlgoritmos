"""
Instalador específico para dependencias del Requerimiento 2
Análisis de Similitud Textual - No interfiere con otros instaladores
"""

import importlib
import subprocess
import sys
import os

def check_installed(package_name):
    """Verifica si un paquete está instalado"""
    try:
        # Mapeo para paquetes cuyo nombre difiere del módulo importable
        module_map = {
            "python-dotenv": "dotenv",
            "scikit-learn": "sklearn",
            "kaleido": None,  # Kaleido no se importa, solo se verifica con pip
            "sentence-transformers": "sentence_transformers"
        }

        mod_name = module_map.get(package_name, package_name.replace("-", "_"))

        # Algunos paquetes no tienen módulo importable directo
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

def install_package(package_name):
    """Instala un paquete específico"""
    try:
        print(f"📦 Instalando {package_name}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", package_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"✅ {package_name} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package_name}: {e}")
        return False

def install_requerimiento2_dependencies():
    """Instala todas las dependencias necesarias para el Requerimiento 2"""

    print("=" * 70)
    print("🔧 INSTALADOR REQUERIMIENTO 2 - Análisis de Similitud Textual")
    print("=" * 70)

    # Dependencias críticas para similitud textual
    critical_deps = {
        'numpy': 'Cálculos numéricos',
        'pandas': 'Manipulación de datos',
        'scikit-learn': 'Algoritmos de ML y TF-IDF',
        'matplotlib': 'Gráficas básicas',
        'seaborn': 'Gráficas avanzadas',
        'bibtexparser': 'Lectura de archivos BibTeX'
    }

    # Dependencias para modelos de IA
    ai_deps = {
        'torch': 'Framework de deep learning',
        'transformers': 'Modelos BERT',
        'sentence-transformers': 'Sentence-BERT para similitud semántica'
    }

    # Combinar todas las dependencias
    all_deps = {**critical_deps, **ai_deps}

    missing_critical = []
    missing_ai = []

    print("\n🔍 Verificando dependencias críticas...\n")

    # Verificar dependencias críticas
    for pkg, desc in critical_deps.items():
        if check_installed(pkg):
            print(f"  ✅ {pkg:<20} - {desc}")
        else:
            print(f"  ❌ {pkg:<20} - {desc}")
            missing_critical.append(pkg)

    print("\n🤖 Verificando dependencias de IA...\n")

    # Verificar dependencias de IA
    for pkg, desc in ai_deps.items():
        if check_installed(pkg):
            print(f"  ✅ {pkg:<20} - {desc}")
        else:
            print(f"  ❌ {pkg:<20} - {desc}")
            missing_ai.append(pkg)

    # Instalar dependencias faltantes
    all_missing = missing_critical + missing_ai

    if all_missing:
        print(f"\n⚠️  Instalando {len(all_missing)} paquetes faltantes...\n")

        success_count = 0
        for package in all_missing:
            if install_package(package):
                success_count += 1

        print(f"\n📊 Resultado: {success_count}/{len(all_missing)} paquetes instalados correctamente")

        if success_count < len(all_missing):
            print("❌ Algunos paquetes no se pudieron instalar. Verifique su conexión a internet.")
            return False
    else:
        print("\n✅ Todas las dependencias ya están instaladas!")

    # Verificación final
    print("\n🔍 Verificación final...")
    all_ok = True
    for pkg in all_deps.keys():
        if not check_installed(pkg):
            print(f"❌ {pkg} aún no está disponible")
            all_ok = False

    if all_ok:
        print("✅ Todas las dependencias del Requerimiento 2 están listas!")
        return True
    else:
        print("❌ Algunas dependencias aún faltan. Intente ejecutar nuevamente.")
        return False

def verify_src_structure():
    """Verifica que la estructura src/ esté disponible"""
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Buscar el directorio src de múltiples formas
    possible_src_paths = [
        # Desde procesamiento/Requerimiento2/ hacia arriba
        os.path.join(current_dir, '..', '..', '..', 'src'),
        # Desde la raíz del proyecto
        os.path.join(current_dir, '..', '..', 'src'),
        # Ruta absoluta si estamos en la raíz
        os.path.join(os.getcwd(), 'src'),
        # Buscar hacia arriba desde el directorio actual
        os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'src'))
    ]

    src_path = None
    for path in possible_src_paths:
        if os.path.exists(path):
            src_path = os.path.abspath(path)
            break

    if src_path is None:
        print("❌ Directorio src no encontrado")
        print("Rutas buscadas:")
        for path in possible_src_paths:
            print(f"  - {path} (existe: {os.path.exists(path)})")
        return False

    similarity_path = os.path.join(src_path, 'similarity')
    if not os.path.exists(similarity_path):
        print(f"❌ Directorio src/similarity no encontrado en: {similarity_path}")
        return False

    # Verificar archivos críticos
    critical_files = [
        'text_similarity_analyzer.py',
        'jaccard_similarity.py',
        'jaro_winkler.py'
    ]

    for file in critical_files:
        file_path = os.path.join(similarity_path, file)
        if not os.path.exists(file_path):
            print(f"❌ Archivo faltante: {file_path}")
            return False

    print(f"✅ Estructura src/ verificada correctamente en: {src_path}")
    return True

if __name__ == "__main__":
    print("🚀 Iniciando instalación de dependencias para Requerimiento 2...")

    # Verificar estructura del proyecto
    if not verify_src_structure():
        print("❌ Error en la estructura del proyecto. Verifique que todos los archivos estén presentes.")
        sys.exit(1)

    # Instalar dependencias
    if install_requerimiento2_dependencies():
        print("\n🎉 ¡Instalación completada! Ya puede ejecutar el Requerimiento 2.")
        sys.exit(0)
    else:
        print("\n❌ La instalación falló. Verifique los errores anteriores.")
        sys.exit(1)