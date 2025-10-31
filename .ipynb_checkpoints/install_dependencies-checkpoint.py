#!/usr/bin/env python3
"""
Script para instalar todas las dependencias necesarias del proyecto
"""
import subprocess
import sys

def install_packages():
    """Instala todas las dependencias necesarias"""
    
    print("=" * 60)
    print("🔧 INSTALADOR DE DEPENDENCIAS - Proyecto Análisis Textual")
    print("=" * 60)
    
    # Paquetes obligatorios
    required = {
        'pandas': 'Manipulación de datos',
        'scikit-learn': 'Algoritmos de ML',
        'nltk': 'Procesamiento de lenguaje natural',
        'bibtexparser': 'Lectura de archivos BibTeX',
    }
    
    # Paquetes opcionales
    optional = {
        'matplotlib': 'Gráficas y visualización',
        'seaborn': 'Gráficas estadísticas',
        'transformers': 'Modelos BERT',
        'torch': 'Framework de deep learning',
        'sentence-transformers': 'Sentence-BERT para similitud semántica',
    }
    
    print("\n📦 [OBLIGATORIOS] Instalando paquetes esenciales...\n")
    for package, description in required.items():
        print(f"  • {package:<20} ({description})")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-U", package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"    ✓ Instalado correctamente\n")
        except Exception as e:
            print(f"    ❌ Error: {e}\n")
    
    print("\n📊 [OPCIONALES] Paquetes para visualización e IA...\n")
    failed = []
    for package, description in optional.items():
        print(f"  • {package:<20} ({description})")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-U", package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"    ✓ Instalado correctamente\n")
        except Exception as e:
            print(f"    ⚠️  No se instaló: {type(e).__name__}\n")
            failed.append(package)
    
    print("=" * 60)
    print("✅ Instalación completada")
    
    if failed:
        print(f"\n⚠️  {len(failed)} paquete(s) opcional(es) no se instaló(aron):")
        for pkg in failed:
            print(f"   - {pkg}")
        print("\nIntenta instalarlos manualmente:")
        print(f"   pip install {' '.join(failed)}")
    else:
        print("\n🎉 Todos los paquetes se instalaron correctamente")
    
    print("=" * 60)

if __name__ == "__main__":
    install_packages()