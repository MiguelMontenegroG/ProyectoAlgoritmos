"""
Configuración centralizada para el análisis de grafo de coocurrencia.
"""

from pathlib import Path

# ============================================================================
# RUTAS Y DIRECTORIOS
# ============================================================================

# Directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# Ruta del archivo BibTeX con documentos unificados
BIBTEX_FILE = PROJECT_ROOT / 'output' / 'unified_cleaned.bib'

# Directorio de salida
OUTPUT_DIR = Path(__file__).parent / 'output'

# ============================================================================
# PARÁMETROS DE COOCURRENCIA
# ============================================================================

# Mínimo número de coocurrencias para crear una arista
MIN_COOCCURRENCE = 1

# Idioma para procesamiento de texto
LANGUAGE = 'english'

# Aplicar lematización
USE_LEMMATIZATION = True

# ============================================================================
# PARÁMETROS DE VISUALIZACIÓN
# ============================================================================

# Tamaño de figura por defecto (ancho, alto)
DEFAULT_FIGSIZE = (14, 10)

# DPI para guardar imágenes
IMAGE_DPI = 300

# Tipo de layout por defecto ('spring', 'circular', 'kamada_kawai')
DEFAULT_LAYOUT = 'spring'

# Método para tamaño de nodos ('degree', 'frequency')
NODE_SIZE_METHOD = 'degree'

# Mostrar etiquetas de nodos
SHOW_NODE_LABELS = True

# ============================================================================
# PARÁMETROS DE ANÁLISIS
# ============================================================================

# Número de nodos principales a mostrar
TOP_NODES_COUNT = 15

# Número de cliques mínimos para mostrar
MIN_CLIQUE_SIZE = 3

# Número máximo de cliques a mostrar
MAX_CLIQUES_TO_SHOW = 10

# ============================================================================
# VERBOSIDAD
# ============================================================================

# Nivel de verbosidad (0=silencioso, 1=normal, 2=verboso)
VERBOSITY = 1

# ============================================================================
# VALIDACIONES
# ============================================================================

def validate_config():
    """Valida la configuración."""
    errors = []
    
    if not BIBTEX_FILE.exists():
        errors.append(f"Archivo BibTeX no encontrado: {BIBTEX_FILE}")
    
    if MIN_COOCCURRENCE < 1:
        errors.append("MIN_COOCCURRENCE debe ser >= 1")
    
    if LANGUAGE not in ['english', 'spanish', 'french', 'german']:
        errors.append(f"Idioma no soportado: {LANGUAGE}")
    
    if IMAGE_DPI < 72:
        errors.append("IMAGE_DPI debe ser >= 72")
    
    return errors


def print_config():
    """Imprime la configuración actual."""
    print("\n" + "="*70)
    print("CONFIGURACIÓN ACTUAL")
    print("="*70)
    print(f"\nRUTAS:")
    print(f"  • Archivo BibTeX: {BIBTEX_FILE}")
    print(f"  • Directorio de salida: {OUTPUT_DIR}")
    
    print(f"\nPARAMETROS DE COOCURRENCIA:")
    print(f"  • Mínimo de coocurrencia: {MIN_COOCCURRENCE}")
    print(f"  • Idioma: {LANGUAGE}")
    print(f"  • Lematización: {USE_LEMMATIZATION}")
    
    print(f"\nPARAMETROS DE VISUALIZACIÓN:")
    print(f"  • Tamaño de figura: {DEFAULT_FIGSIZE}")
    print(f"  • DPI: {IMAGE_DPI}")
    print(f"  • Layout: {DEFAULT_LAYOUT}")
    
    print(f"\nPARAMETROS DE ANÁLISIS:")
    print(f"  • Nodos principales: {TOP_NODES_COUNT}")
    print(f"  • Tamaño mínimo de cliques: {MIN_CLIQUE_SIZE}")
    print()