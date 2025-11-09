"""
Requerimiento 2: Análisis de Similitud Textual
Implementa 6 algoritmos de similitud textual para comparar abstracts científicos
"""

import os
import sys
import subprocess
import warnings
warnings.filterwarnings('ignore')

# Agregar rutas necesarias - método más robusto
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
    print("❌ ERROR: No se pudo encontrar el directorio 'src'")
    print("Rutas buscadas:")
    for path in possible_src_paths:
        print(f"  - {path} (existe: {os.path.exists(path)})")
    sys.exit(1)

project_root = os.path.dirname(src_path)

print(f"📁 Directorio src encontrado: {src_path}")
print(f"📁 Raíz del proyecto: {project_root}")

# Asegurar que src esté en el path
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# También configurar PYTHONPATH como variable de entorno
current_pythonpath = os.environ.get('PYTHONPATH', '')
os.environ['PYTHONPATH'] = f"{src_path}{os.pathsep}{project_root}{os.pathsep}{current_pythonpath}".rstrip(os.pathsep)

# Función para verificar e instalar dependencias
def check_and_install_dependencies():
    """Verifica dependencias y las instala si faltan"""
    print("🔍 Verificando dependencias del Requerimiento 2...")

    # Verificar si podemos importar los módulos críticos
    missing_deps = []
    try:
        import numpy
    except ImportError:
        missing_deps.append('numpy')

    try:
        import pandas
    except ImportError:
        missing_deps.append('pandas')

    try:
        import sklearn
    except ImportError:
        missing_deps.append('scikit-learn')

    try:
        import matplotlib
    except ImportError:
        missing_deps.append('matplotlib')

    try:
        import bibtexparser
    except ImportError:
        missing_deps.append('bibtexparser')

    if missing_deps:
        print(f"❌ Faltan dependencias críticas: {', '.join(missing_deps)}")
        print("🚀 Ejecutando instalador automático...")
        try:
            result = subprocess.run([sys.executable, os.path.join(current_dir, 'install_requerimiento2.py')],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Instalación completada. Reinicie el script para continuar.")
                print("💡 Presione Enter para salir...")
                input()
                sys.exit(0)
            else:
                print("❌ Error en la instalación automática")
                print("Salida del instalador:")
                print(result.stdout)
                print(result.stderr)
                return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Error ejecutando instalador: {e}")
            return False
    else:
        print("✅ Dependencias críticas verificadas")

    # Verificar estructura src (ya verificada arriba, pero confirmamos)
    similarity_path = os.path.join(src_path, 'similarity')
    if not os.path.exists(similarity_path):
        print(f"❌ Directorio src/similarity no encontrado: {similarity_path}")
        return False

    return True

# Verificar e instalar dependencias antes de continuar
if not check_and_install_dependencies():
    print("❌ No se pueden resolver las dependencias. Verifique la instalación manualmente.")
    sys.exit(1)

# Importaciones del proyecto (después de verificar dependencias)
try:
    from src.similarity.text_similarity_analyzer import TextSimilarityAnalyzer
    from src.similarity.jaccard_similarity import jaccard_similarity_detailed
    from src.similarity.jaro_winkler import jaro_winkler_detailed
    SIMILARITY_AVAILABLE = True
    print("✅ Módulos de similitud cargados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos de similitud: {e}")
    SIMILARITY_AVAILABLE = False

# Importaciones para BibTeX
try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.customization import convert_to_unicode
    BIBTEX_AVAILABLE = True
except ImportError:
    BIBTEX_AVAILABLE = False

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display, HTML

# Configuración de visualización
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_bibtex_abstracts(filepath):
    """
    Carga abstracts del archivo BibTeX

    Args:
        filepath (str): Ruta al archivo BibTeX

    Returns:
        pd.DataFrame: DataFrame con columnas id, title, abstract, year, authors
    """
    if not BIBTEX_AVAILABLE:
        print("❌ bibtexparser no está disponible. Instale con: pip install bibtexparser")
        import pandas as pd
        return pd.DataFrame()

    if not os.path.exists(filepath):
        print(f"❌ El archivo no existe: {filepath}")
        import pandas as pd
        return pd.DataFrame()
    
    try:
        # Verificar tamaño del archivo
        file_size = os.path.getsize(filepath)
        print(f"📁 Cargando archivo: {os.path.basename(filepath)} ({file_size:,} bytes)")
        
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        parser.ignore_nonstandard_types = False  # No ignorar tipos no estándar
        parser.common_strings = []  # No usar strings comunes

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            bibtex_db = bibtexparser.load(f, parser=parser)

        print(f"📊 Total de entradas en el archivo: {len(bibtex_db.entries)}")
        
        abstracts_list = []
        entries_with_abstract = 0
        entries_without_abstract = 0
        
        for entry in bibtex_db.entries:
            if 'abstract' in entry and entry['abstract'] and entry['abstract'].strip():
                abstracts_list.append({
                    'id': entry.get('ID', 'Unknown'),
                    'title': entry.get('title', 'No title'),
                    'abstract': entry['abstract'],
                    'year': entry.get('year', 'N/A'),
                    'authors': entry.get('author', 'N/A')
                })
                entries_with_abstract += 1
            else:
                entries_without_abstract += 1

        print(f"✅ Entradas con abstract: {entries_with_abstract}")
        if entries_without_abstract > 0:
            print(f"⚠️ Entradas sin abstract: {entries_without_abstract}")

        # Convertir a DataFrame para compatibilidad con el código existente
        import pandas as pd
        df = pd.DataFrame(abstracts_list)
        
        if df.empty:
            print("⚠️ ADVERTENCIA: No se encontraron entradas con abstract en el archivo")
            print("💡 El archivo puede estar vacío o las entradas no tienen el campo 'abstract'")
        else:
            print(f"✅ Se cargaron {len(df)} abstracts exitosamente")
        
        return df
    except Exception as e:
        print(f"❌ Error cargando BibTeX: {e}")
        import traceback
        traceback.print_exc()
        import pandas as pd
        return pd.DataFrame()


def find_bibtex_file():
    """
    Busca automáticamente el archivo BibTeX unificado

    Returns:
        str: Ruta al archivo BibTeX encontrado
    """
    # Buscar desde múltiples ubicaciones posibles
    search_roots = [
        project_root,  # Raíz del proyecto
        os.getcwd(),   # Directorio actual de trabajo
        os.path.dirname(os.path.abspath(__file__)),  # Directorio del script actual
    ]
    
    # Agregar rutas relativas comunes
    for root in search_roots:
        # Posibles ubicaciones del archivo BibTeX
        possible_paths = [
            os.path.join(root, 'output', 'unified_cleaned.bib'),
            os.path.join(root, 'output', 'unifed_reducido.bib'),
            os.path.join(root, 'output', 'unified_with_metadata.bib'),
            os.path.join(root, 'unified_cleaned.bib'),
            os.path.join(root, 'unifed_reducido.bib'),
            os.path.join(root, 'procesamiento', '..', 'output', 'unified_cleaned.bib'),
            os.path.join(root, '..', 'output', 'unified_cleaned.bib'),
        ]
        
        for path in possible_paths:
            # Resolver rutas relativas
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                print(f"📁 Archivo BibTeX encontrado en: {abs_path}")
                return abs_path

    # Buscar archivos .bib en el directorio output (último recurso)
    for root in search_roots:
        output_dir = os.path.join(root, 'output')
        if os.path.exists(output_dir):
            try:
                for file in os.listdir(output_dir):
                    if file.endswith('.bib') and file not in ['duplicates.bib']:
                        file_path = os.path.join(output_dir, file)
                        print(f"📁 Archivo BibTeX encontrado en: {file_path}")
                        return file_path
            except Exception as e:
                print(f"⚠️ Error buscando en {output_dir}: {e}")
                continue
    
    print("❌ No se encontró archivo BibTeX unificado")
    print("💡 Rutas buscadas:")
    for root in search_roots:
        print(f"   - {root}")
        output_dir = os.path.join(root, 'output')
        if os.path.exists(output_dir):
            print(f"     └─ output/ existe: {output_dir}")
        else:
            print(f"     └─ output/ no existe")
    return None


def select_articles_interactive(abstracts):
    """
    Permite seleccionar artículos de forma interactiva

    Args:
        abstracts (pd.DataFrame): DataFrame de abstracts disponibles

    Returns:
        tuple: (abstract1_data, abstract2_data) o (None, None) si cancelado
    """
    if abstracts.empty:
        print("❌ No hay abstracts disponibles")
        return None, None

    print(f"\n📚 Se encontraron {len(abstracts)} abstracts disponibles")
    print("\n" + "="*80)
    print("SELECCIÓN DE ARTÍCULOS PARA COMPARAR")
    print("="*80)

    # Mostrar tabla de artículos disponibles
    display_table = abstracts[['id', 'title', 'year']].head(10).reset_index()
    display_table = display_table[['index', 'id', 'title', 'year']]
    print("\nPrimeros 10 artículos disponibles:")
    print(display_table.to_string(index=False))

    if len(abstracts) > 10:
        print(f"\n... y {len(abstracts) - 10} artículos más")

    # Seleccionar primer artículo
    while True:
        try:
            idx1 = input(f"\n👉 Seleccione el primer artículo (0-{len(abstracts)-1}): ").strip()
            if not idx1:
                print("❌ Selección cancelada")
                return None, None

            idx1 = int(idx1)
            if 0 <= idx1 < len(abstracts):
                break
            else:
                print(f"❌ Índice inválido. Use un número entre 0 y {len(abstracts)-1}")
        except ValueError:
            print("❌ Por favor ingrese un número válido")

    # Seleccionar segundo artículo
    while True:
        try:
            idx2 = input(f"👉 Seleccione el segundo artículo (0-{len(abstracts)-1}): ").strip()
            if not idx2:
                print("❌ Selección cancelada")
                return None, None

            idx2 = int(idx2)
            if 0 <= idx2 < len(abstracts) and idx2 != idx1:
                break
            elif idx2 == idx1:
                print("❌ Seleccione un artículo diferente al primero")
            else:
                print(f"❌ Índice inválido. Use un número entre 0 y {len(abstracts)-1}")
        except ValueError:
            print("❌ Por favor ingrese un número válido")

    abstract1_data = abstracts.iloc[idx1].to_dict()
    abstract2_data = abstracts.iloc[idx2].to_dict()

    return abstract1_data, abstract2_data


def display_article_info(article_data, number):
    """
    Muestra información detallada de un artículo

    Args:
        article_data (dict): Datos del artículo
        number (int): Número del artículo (1 o 2)
    """
    print(f"\n{'='*80}")
    print(f"📄 ARTÍCULO {number}: {article_data['id']}")
    print(f"{'='*80}")
    print(f"📖 Título: {article_data['title']}")
    print(f"👥 Autores: {article_data['authors']}")
    print(f"📅 Año: {article_data['year']}")
    print(f"\n📝 Abstract ({len(article_data['abstract'])} caracteres):")
    print("-" * 40)
    print(article_data['abstract'])
    print("-" * 40)


def run_similarity_analysis(abstract1_data, abstract2_data):
    """
    Ejecuta el análisis completo de similitud

    Args:
        abstract1_data (dict): Datos del primer artículo
        abstract2_data (dict): Datos del segundo artículo
    """
    if not SIMILARITY_AVAILABLE:
        print("❌ Módulos de similitud no disponibles")
        return

    print(f"\n🔍 ANALIZANDO SIMILITUD TEXTUAL")
    print("="*80)

    # Crear analizador
    analyzer = TextSimilarityAnalyzer(
        abstract1_data['abstract'],
        abstract2_data['abstract']
    )

    # Calcular todos los algoritmos
    print("⏳ Calculando similitud con todos los algoritmos...")
    results = analyzer.compute_all()
    comparison = analyzer.compare_all()

    # Mostrar resultados
    print(f"\n📊 RESULTADOS DE SIMILITUD:")
    print("-" * 50)
    results_df = pd.DataFrame([
        {'Algoritmo': name, 'Similitud': value}
        for name, value in comparison['similarities'].items()
    ]).reset_index(drop=True)

    print(results_df.to_string(index=False))

    print(f"\n🏆 RANKING (Mayor a menor similitud):")
    for i, (name, value) in enumerate(comparison['similarities'].items(), 1):
        bars = '█' * int(value*20)
        print(f"{i}. {name:25} {value:.4f} {bars}")

    # En modo web, no preguntar por análisis detallado (se hace después)
    # Preguntar si mostrar análisis detallado
    try:
        while True:
            show_detailed = input(f"\n❓ ¿Desea ver el análisis detallado paso a paso? (s/n): ").strip().lower()
            if show_detailed in ['s', 'si', 'y', 'yes', 'n', 'no']:
                break
            print("❌ Responda 's' para sí o 'n' para no")

        if show_detailed in ['s', 'si', 'y', 'yes']:
            show_detailed_analysis(analyzer)
    except:
        # En caso de error (modo no interactivo), no mostrar análisis detallado
        pass

    return analyzer


def show_detailed_analysis(analyzer):
    """
    Muestra análisis detallado paso a paso

    Args:
        analyzer (TextSimilarityAnalyzer): Analizador configurado
    """
    print(f"\n🔬 ANÁLISIS DETALLADO PASO A PASO")
    print("="*80)

    detailed_results = analyzer.get_detailed_analysis('all')

    # Análisis Jaccard
    if 'jaccard' in detailed_results:
        jac = detailed_results['jaccard']
        print(f"\n📐 ALGORITMO: SIMILITUD DE JACCARD")
        print("-" * 40)
        print("Fórmula: J(A, B) = |A ∩ B| / |A ∪ B|")

        print(f"\n📊 PASO A PASO:")
        print(f"  1. Tokens Texto 1: {len(jac['paso_1_tokens_texto1'])} palabras")
        print(f"  2. Tokens Texto 2: {len(jac['paso_2_tokens_texto2'])} palabras")
        print(f"  3. Intersección: {jac['paso_3_interseccion_size']} palabras comunes")
        print(f"  4. Unión: {jac['paso_4_union_size']} palabras únicas")
        print(f"  5. Similitud: {jac['resultado_similitud_jaccard']:.4f}")

    # Análisis Jaro-Winkler
    if 'jaro_winkler' in detailed_results:
        jw = detailed_results['jaro_winkler']
        print(f"\n📐 ALGORITMO: SIMILITUD JARO-WINKLER")
        print("-" * 40)
        print("Fórmula: jaro_winkler = jaro + (l × p × (1 - jaro))")

        print(f"\n📊 PASO A PASO:")
        print(f"  1. Longitud Texto 1: {jw['paso_1_longitud_s1']} caracteres")
        print(f"  2. Longitud Texto 2: {jw['paso_1_longitud_s2']} caracteres")
        print(f"  3. Ventana coincidencia: {jw['paso_2_ventana_coincidencia']}")
        print(f"  4. Similitud JARO: {jw['paso_5_jaro_resultado']:.4f}")
        print(f"  5. Prefijo común: '{jw['paso_6_prefijo_comun']}' ({jw['paso_6_longitud_prefijo']} chars)")
        print(f"  6. Similitud JARO-WINKLER: {jw['resultado_jaro_winkler']:.4f}")

    # Análisis BERT (si disponible)
    if 'bert' in detailed_results:
        bert = detailed_results['bert']
        print(f"\n🤖 MODELO IA: BERT")
        print("-" * 40)
        print("Arquitectura: Transformer Bidireccional")

        print(f"\n📊 PASO A PASO:")
        print(f"  1. Modelo: {bert.get('paso_1_modelo', 'N/A')}")
        print(f"  2. Dimensión embeddings: {bert.get('paso_3_embedding_dimension', 'N/A')}")
        print(f"  3. Similitud coseno: {bert.get('resultado_similitud_bert', 'N/A'):.4f}")

    # Análisis Sentence-BERT (si disponible)
    if 'sentence_bert' in detailed_results:
        sbert = detailed_results['sentence_bert']
        print(f"\n🚀 MODELO IA: SENTENCE-BERT")
        print("-" * 40)
        print("Optimizado para similitud semántica de oraciones")

        print(f"\n📊 PASO A PASO:")
        print(f"  1. Modelo: {sbert.get('modelo', 'N/A')}")
        print(f"  2. Similitud semántica: {sbert.get('similitud', 'N/A'):.4f}")


def create_visualization(comparison_results):
    """
    Crea visualización de los resultados de similitud

    Args:
        comparison_results (dict): Resultados de comparación
    """
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Datos para visualización
        algorithms = list(comparison_results['similarities'].keys())
        values = list(comparison_results['similarities'].values())

        # Gráfico de barras
        colors = plt.cm.viridis(np.linspace(0, 1, len(algorithms)))
        bars = ax1.barh(algorithms, values, color=colors)
        ax1.set_xlabel('Similitud', fontsize=12, fontweight='bold')
        ax1.set_title('Comparación de Similitud por Algoritmo', fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 1)
        ax1.grid(axis='x', alpha=0.3)

        # Añadir valores en las barras
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax1.text(value + 0.02, i, f'{value:.3f}', va='center', fontweight='bold')

        # Gráfico radar (si hay suficientes algoritmos)
        if len(algorithms) >= 3:
            angles = np.linspace(0, 2*np.pi, len(algorithms), endpoint=False).tolist()
            angles += angles[:1]
            values_radar = values + values[:1]

            ax2 = plt.subplot(122, projection='polar')
            ax2.plot(angles, values_radar, 'o-', linewidth=2, color='steelblue')
            ax2.fill(angles, values_radar, alpha=0.25, color='steelblue')
            ax2.set_xticks(angles[:-1])
            ax2.set_xticklabels(algorithms, fontsize=9)
            ax2.set_ylim(0, 1)
            ax2.set_title('Gráfico Radar de Similitudes', fontsize=14, fontweight='bold', pad=20)
            ax2.grid(True)

        plt.tight_layout()

        # Guardar gráfico
        output_dir = os.path.join(project_root, 'output')
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'similitud_textual_analisis.png'), dpi=300, bbox_inches='tight')
        print(f"\n💾 Gráfico guardado en: output/similitud_textual_analisis.png")

        # No mostrar plt.show() en entorno web
        plt.close()

    except Exception as e:
        print(f"⚠️ Error creando visualización: {e}")


def mainRequerimiento2():
    """
    Función principal del Requerimiento 2
    """
    print("\n" + "="*80)
    print("🎯 REQUERIMIENTO 2: ANÁLISIS DE SIMILITUD TEXTUAL".center(80))
    print("="*80)
    print("Implementa 6 algoritmos de similitud textual:")
    print("• 4 Clásicos: Levenshtein, Jaccard, Jaro-Winkler, TF-IDF+Coseno")
    print("• 2 con IA: BERT, Sentence-BERT")
    print("="*80)

    # Verificar dependencias
    if not SIMILARITY_AVAILABLE:
        print("\n❌ Error: Módulos de similitud no disponibles")
        print("Ejecute el instalador de dependencias primero")
        return

    if not BIBTEX_AVAILABLE:
        print("\n❌ Error: bibtexparser no disponible")
        print("Instale con: pip install bibtexparser")
        return

    # Buscar archivo BibTeX
    bibtex_path = find_bibtex_file()
    if not bibtex_path:
        print("\n❌ No se encontró archivo BibTeX unificado")
        print("Ejecute primero el Requerimiento 1 para generar el archivo unificado")
        return

    print(f"\n📁 Archivo BibTeX encontrado: {os.path.basename(bibtex_path)}")

    # Cargar abstracts
    print("\n⏳ Cargando abstracts del archivo BibTeX...")
    abstracts = load_bibtex_abstracts(bibtex_path)

    if abstracts.empty:
        print("❌ No se pudieron cargar abstracts del archivo")
        return

    print(f"✅ Se cargaron {len(abstracts)} abstracts exitosamente")

    # Bucle principal
    while True:
        # Seleccionar artículos
        abstract1_data, abstract2_data = select_articles_interactive(abstracts)

        if abstract1_data is None or abstract2_data is None:
            break

        # Mostrar información de los artículos seleccionados
        display_article_info(abstract1_data, 1)
        display_article_info(abstract2_data, 2)

        # Ejecutar análisis
        analyzer = TextSimilarityAnalyzer(
            abstract1_data['abstract'],
            abstract2_data['abstract']
        )

        # Calcular similitudes
        results = analyzer.compute_all()
        comparison = analyzer.compare_all()

        # Mostrar resultados principales
        print(f"\n📊 RESULTADOS DE SIMILITUD:")
        print("-" * 50)
        results_df = pd.DataFrame([
            {'Algoritmo': name, 'Similitud': value}
            for name, value in comparison['similarities'].items()
        ]).reset_index(drop=True)

        print(results_df.to_string(index=False))

        print(f"\n🏆 RANKING (Mayor a menor similitud):")
        for i, (name, value) in enumerate(comparison['similarities'].items(), 1):
            bars = '█' * int(value*20)
            print(f"{i}. {name:25} {value:.4f} {bars}")

        # Preguntar por análisis detallado
        while True:
            show_detailed = input(f"\n❓ ¿Ver análisis detallado paso a paso? (s/n): ").strip().lower()
            if show_detailed in ['s', 'si', 'y', 'yes', 'n', 'no']:
                break
            print("❌ Responda 's' para sí o 'n' para no")

        if show_detailed in ['s', 'si', 'y', 'yes']:
            show_detailed_analysis(analyzer)

        # Preguntar por visualización
        while True:
            show_viz = input(f"\n❓ ¿Generar gráficos comparativos? (s/n): ").strip().lower()
            if show_viz in ['s', 'si', 'y', 'yes', 'n', 'no']:
                break
            print("❌ Responda 's' para sí o 'n' para no")

        if show_viz in ['s', 'si', 'y', 'yes']:
            create_visualization(comparison)

        # Preguntar si continuar
        while True:
            continuar = input(f"\n❓ ¿Analizar otros artículos? (s/n): ").strip().lower()
            if continuar in ['s', 'si', 'y', 'yes', 'n', 'no']:
                break
            print("❌ Responda 's' para sí o 'n' para no")

        if continuar in ['n', 'no']:
            break

        print("\n" + "="*80)

    print("\n👋 ¡Gracias por usar el análisis de similitud textual!")
    print("Los resultados se guardaron en la carpeta 'output/'")


if __name__ == "__main__":
    mainRequerimiento2()