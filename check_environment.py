#!/usr/bin/env python3
"""
Script para verificar el estado del ambiente
"""
import sys

def check_environment():
    """Verifica qué paquetes están instalados"""
    
    print("\n" + "="*60)
    print("🔍 VERIFICADOR DE AMBIENTE")
    print("="*60)
    
    print(f"\n📌 Python: {sys.version.split()[0]}")
    print(f"   Ubicación: {sys.executable}\n")
    
    # Paquetes obligatorios
    required = ['pandas', 'scikit-learn', 'nltk', 'bibtexparser']
    
    # Paquetes visualización
    visualization = ['matplotlib', 'seaborn', 'jupyter']
    
    # Paquetes IA
    ai_models = ['transformers', 'torch', 'sentence_transformers']
    
    all_packages = {
        '📦 OBLIGATORIOS': required,
        '📊 VISUALIZACIÓN': visualization,
        '🤖 MODELOS IA': ai_models,
    }
    
    total_installed = 0
    total_missing = 0
    
    for category, packages in all_packages.items():
        print(f"\n{category}")
        print("-" * 60)
        
        for package in packages:
            try:
                mod = __import__(package.replace('-', '_'))
                
                # Intenta obtener versión
                version = getattr(mod, '__version__', 'desconocida')
                
                print(f"  ✓ {package:<25} v{version}")
                total_installed += 1
            except ImportError:
                print(f"  ❌ {package:<25} NO INSTALADO")
                total_missing += 1
    
    print("\n" + "="*60)
    print(f"📊 RESUMEN: {total_installed} instalado(s), {total_missing} faltante(s)")
    print("="*60)
    
    # Recomendaciones
    if total_missing > 0:
        print("\n💡 INSTALACIÓN RECOMENDADA:\n")
        print("  1. Básico (necesario para funcionar):")
        print("     python -m pip install pandas scikit-learn nltk bibtexparser\n")
        
        print("  2. Con visualización (recomendado):")
        print("     python -m pip install matplotlib seaborn jupyter\n")
        
        print("  3. Con modelos IA (mejor precisión):")
        print("     python -m pip install transformers torch sentence-transformers\n")
        
        print("  O instala todo de una vez:")
        print("     python install_dependencies.py\n")
        
        print("  O usa requirements.txt:")
        print("     pip install -r requirements.txt\n")
    else:
        print("\n✅ ¡TODOS LOS PAQUETES ESTÁN INSTALADOS!\n")
        print("   Puedes ejecutar:\n")
        print("   jupyter notebook Text_Similarity_Analysis.ipynb\n")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    check_environment()