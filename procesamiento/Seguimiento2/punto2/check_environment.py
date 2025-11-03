"""
Script para verificar que el ambiente está correctamente configurado.
Comprueba que todos los módulos requeridos estén instalados.
"""

import sys
from pathlib import Path


def check_import(module_name, package_name=None):
    """
    Verifica que un módulo pueda ser importado.
    
    Args:
        module_name (str): Nombre del módulo a importar
        package_name (str): Nombre alternativo del paquete (si difiere)
        
    Returns:
        tuple: (success, version)
    """
    try:
        module = __import__(module_name)
        version = getattr(module, '__version__', 'desconocida')
        return True, version
    except ImportError:
        return False, None


def check_file_exists(file_path, description=""):
    """
    Verifica que un archivo exista.
    
    Args:
        file_path (str o Path): Ruta del archivo
        description (str): Descripción del archivo
        
    Returns:
        bool: True si existe
    """
    path = Path(file_path)
    return path.exists()


def print_header(text):
    """Imprime un encabezado."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def print_success(text):
    """Imprime un mensaje de éxito."""
    print(f"  ✓ {text}")


def print_error(text):
    """Imprime un mensaje de error."""
    print(f"  ✗ {text}")


def print_warning(text):
    """Imprime un mensaje de advertencia."""
    print(f"  ⚠ {text}")


def main():
    """Verifica la configuración del ambiente."""
    
    print("\n" + "="*70)
    print("  VERIFICACIÓN DE AMBIENTE - ANÁLISIS DE GRAFO DE COOCURRENCIA")
    print("="*70)
    
    errors = []
    warnings = []
    
    # 1. Verificar Python
    print_header("1. VERIFICACIÓN DE PYTHON")
    python_version = sys.version_info
    py_version_str = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
    
    if python_version.major >= 3 and python_version.minor >= 7:
        print_success(f"Python {py_version_str}")
    else:
        errors.append(f"Python {py_version_str} (se requiere >= 3.7)")
        print_error(f"Python {py_version_str} (se requiere >= 3.7)")
    
    # 2. Verificar módulos obligatorios
    print_header("2. MÓDULOS OBLIGATORIOS")
    
    required_modules = [
        ('networkx', 'NetworkX'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('matplotlib', 'Matplotlib'),
        ('nltk', 'NLTK'),
        ('bibtexparser', 'BibtexParser'),
        ('sklearn', 'Scikit-learn'),
    ]
    
    for module_name, display_name in required_modules:
        success, version = check_import(module_name)
        if success:
            print_success(f"{display_name} {version}")
        else:
            errors.append(f"{display_name} no instalado")
            print_error(f"{display_name} no instalado")
    
    # 3. Verificar módulos opcionales
    print_header("3. MÓDULOS OPCIONALES")
    
    optional_modules = [
        ('seaborn', 'Seaborn'),
        ('jupyter', 'Jupyter'),
    ]
    
    for module_name, display_name in optional_modules:
        success, version = check_import(module_name)
        if success:
            print_success(f"{display_name} {version}")
        else:
            warnings.append(f"{display_name} no instalado (opcional)")
            print_warning(f"{display_name} no instalado (opcional)")
    
    # 4. Verificar archivos del proyecto
    print_header("4. ARCHIVOS DEL PROYECTO")
    
    project_root = Path(__file__).parent
    required_files = [
        (project_root / 'cooccurrence_graph.py', 'cooccurrence_graph.py'),
        (project_root / 'graph_analyzer.py', 'graph_analyzer.py'),
        (project_root / 'graph_visualizer.py', 'graph_visualizer.py'),
        (project_root / 'main.py', 'main.py'),
        (project_root / '__init__.py', '__init__.py'),
    ]
    
    for file_path, display_name in required_files:
        if check_file_exists(file_path):
            print_success(f"{display_name}")
        else:
            errors.append(f"{display_name} no encontrado")
            print_error(f"{display_name} no encontrado")
    
    # 5. Verificar archivo BibTeX
    print_header("5. DATOS DE ENTRADA")
    
    bibtex_file = Path(r'C:\Users\ANGEL\Documents\GitHub\ProyectoAlgoritmos\output\unified_cleaned.bib')
    
    if check_file_exists(bibtex_file):
        size_mb = bibtex_file.stat().st_size / 1024 / 1024
        print_success(f"Archivo BibTeX encontrado ({size_mb:.2f} MB)")
    else:
        warnings.append(f"Archivo BibTeX no encontrado: {bibtex_file}")
        print_warning(f"Archivo BibTeX no encontrado")
    
    # 6. Verificar carpeta de salida
    print_header("6. VERIFICACIÓN DE CARPETA DE SALIDA")
    
    output_dir = project_root / 'output'
    try:
        output_dir.mkdir(exist_ok=True)
        print_success(f"Carpeta de salida disponible: {output_dir}")
    except Exception as e:
        errors.append(f"No se puede crear carpeta de salida: {e}")
        print_error(f"No se puede crear carpeta de salida: {e}")
    
    # 7. Resumen
    print_header("7. RESUMEN")
    
    if not errors:
        print_success("✓ Ambiente correctamente configurado")
        print("\nPuedes ejecutar: python main.py")
    else:
        print_error(f"Se encontraron {len(errors)} errores:")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print(f"\n⚠ Se encontraron {len(warnings)} advertencias:")
        for warning in warnings:
            print(f"  • {warning}")
    
    # 8. Instrucciones de instalación
    if errors:
        print_header("INSTRUCCIONES DE INSTALACIÓN")
        print("\nPara instalar las dependencias faltantes, ejecuta:")
        print("  pip install -r requirements.txt")
        print("\nO instala manualmente:")
        for module_name, display_name in required_modules:
            success, _ = check_import(module_name)
            if not success:
                print(f"  pip install {module_name}")
    
    print("\n" + "="*70 + "\n")
    
    return len(errors) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)