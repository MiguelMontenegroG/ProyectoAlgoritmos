#!/usr/bin/env python3
"""
Script de prueba para verificar que Requerimiento 2 funciona
"""

import os
import sys

# Configurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
src_path = os.path.join(project_root, 'src')

print(f"Directorio actual: {current_dir}")
print(f"Raíz del proyecto: {project_root}")
print(f"Directorio src: {src_path}")

# Agregar al path
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"Python path: {sys.path}")

# Verificar estructura
print(f"¿Existe src?: {os.path.exists(src_path)}")
print(f"¿Existe src/similarity?: {os.path.exists(os.path.join(src_path, 'similarity'))}")

# Intentar importar
try:
    from src.similarity.text_similarity_analyzer import TextSimilarityAnalyzer
    print("✅ Importación exitosa de TextSimilarityAnalyzer")
except ImportError as e:
    print(f"❌ Error importando TextSimilarityAnalyzer: {e}")

try:
    import numpy
    print("✅ NumPy disponible")
except ImportError:
    print("❌ NumPy no disponible")

try:
    import pandas
    print("✅ Pandas disponible")
except ImportError:
    print("❌ Pandas no disponible")