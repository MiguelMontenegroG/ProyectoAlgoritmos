"""
Script principal con barras de progreso para análisis de grafo de coocurrencia.
Proporciona visibilidad del proceso de análisis en tiempo real.
"""

import sys
import os
from pathlib import Path
import time

# Intentar importar tqdm, si no está disponible usar alternativa simple
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("⚠️  tqdm no instalado. Instalando...")
    os.system("pip install tqdm --quiet")
    try:
        from tqdm import tqdm
        TQDM_AVAILABLE = True
    except:
        TQDM_AVAILABLE = False

# Agregar rutas al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cooccurrence_graph import build_cooccurrence_graph_from_abstracts
from graph_analyzer import GraphAnalyzer
from graph_visualizer import GraphVisualizer
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import json
from datetime import datetime


class ProgressTracker:
    """Rastreador simple de progreso sin dependencias externas."""
    
    @staticmethod
    def bar(iterable, desc="", total=None):
        """Retorna una barra de progreso o el iterable según disponibilidad."""
        if TQDM_AVAILABLE:
            return tqdm(iterable, desc=desc, total=total)
        else:
            return iterable


def load_abstracts_from_bibtex(file_path):
    """
    Carga abstracts desde un archivo BibTeX con seguimiento.
    
    Args:
        file_path (str): Ruta al archivo .bib
        
    Returns:
        list: Lista de abstracts
    """
    try:
        print("📖 Leyendo archivo BibTeX...")
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        with open(file_path, 'r', encoding='utf-8') as bibtex_file:
            entries = bibtexparser.load(bibtex_file, parser=parser).entries
        
        abstracts = []
        print(f"📝 Extrayendo abstracts de {len(entries)} entradas...")
        
        for entry in ProgressTracker.bar(entries, desc="  Extrayendo", total=len(entries)):
            if 'abstract' in entry and entry['abstract'].strip():
                abstracts.append(entry['abstract'])
        
        print(f"✓ Se cargaron {len(abstracts)} abstracts de {len(entries)} entradas\n")
        return abstracts
    
    except Exception as e:
        print(f"✗ Error al cargar abstracts: {str(e)}")
        return []


def print_section(title):
    """Imprime un título de sección."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_report(report):
    """Imprime un reporte de estadísticas."""
    print("ESTADÍSTICAS BÁSICAS:")
    for key, value in report['basic_stats'].items():
        if isinstance(value, float):
            print(f"  • {key}: {value:.4f}")
        else:
            print(f"  • {key}: {value}")
    
    print("\nESTADÍSTICAS DE GRADO:")
    for key, value in report['degree_stats'].items():
        if isinstance(value, float):
            print(f"  • {key}: {value:.4f}")
        else:
            print(f"  • {key}: {value}")
    
    print("\nCONECTIVIDAD:")
    for key, value in report['connectivity'].items():
        print(f"  • {key}: {value}")
    
    print("\nCLUSTERING:")
    for key, value in report['clustering'].items():
        if isinstance(value, float):
            print(f"  • {key}: {value:.4f}")
        else:
            print(f"  • {key}: {value}")


def generate_json_report(analyzer, output_path):
    """Genera un reporte en formato JSON."""
    
    analyzer.calculate_node_degrees()
    components_stats = analyzer.get_connected_components_with_stats()
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'graph_stats': {
            'nodes': analyzer.graph.number_of_nodes(),
            'edges': analyzer.graph.number_of_edges(),
            'density': float(analyzer.graph.number_of_nodes() > 0 and 
                           len(list(analyzer.graph.edges())) / (analyzer.graph.number_of_nodes() * (analyzer.graph.number_of_nodes() - 1) / 2) or 0),
            'is_connected': bool(__import__('networkx').is_connected(analyzer.graph))
        },
        'degree_analysis': {
            'top_nodes': analyzer.get_top_nodes_by_degree(20),
            'degree_distribution': dict(analyzer.calculate_node_degrees())
        },
        'connected_components': components_stats,
        'clustering': {
            'average_coefficient': float(analyzer.get_average_clustering_coefficient()),
            'triangles': sum(analyzer.get_triangles().values()) // 3
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return report


def main():
    """Función principal con seguimiento de progreso."""
    
    print("\n" + "="*70)
    print("  ANÁLISIS DE GRAFO DE COOCURRENCIA - CON MONITOREO")
    print("="*70)
    print("⏱️  Tiempo total estimado: 5-15 minutos")
    print("📊 Puedes ver el progreso en tiempo real abajo\n")
    
    start_time = time.time()
    
    # Configuración
    bibtex_file = r'C:\Users\ANGEL\Documents\GitHub\ProyectoAlgoritmos\output\unified_cleaned.bib'
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # 1. Cargar abstracts
    print_section("1️⃣  CARGA DE DATOS")
    abstracts = load_abstracts_from_bibtex(bibtex_file)
    
    if not abstracts:
        print("✗ No se pudieron cargar abstracts. Abortando...")
        return
    
    # 2. Construir grafo de coocurrencia
    print_section("2️⃣  CONSTRUCCIÓN DEL GRAFO DE COOCURRENCIA")
    print("🔗 Procesando documentos y construyendo grafo...\n")
    
    start_graph = time.time()
    cg = build_cooccurrence_graph_from_abstracts(abstracts, min_cooccurrence=1)
    stats = cg.get_statistics()
    graph_time = time.time() - start_graph
    
    print(f"\n✓ Grafo construido exitosamente:")
    print(f"  • Nodos (términos únicos): {stats['total_nodes']}")
    print(f"  • Aristas (coocurrencias): {stats['total_edges']}")
    print(f"  • Documentos procesados: {stats['total_documents']}")
    print(f"  • Densidad del grafo: {stats['density']:.6f}")
    print(f"  • Grado promedio: {stats['average_degree']:.2f}")
    print(f"  • Tiempo: {graph_time:.2f}s\n")
    
    # 3. Análisis del grafo
    print_section("3️⃣  ANÁLISIS DEL GRAFO")
    print("📈 Calculando propiedades del grafo...\n")
    
    start_analysis = time.time()
    analyzer = GraphAnalyzer(cg.get_graph())
    full_report = analyzer.get_graph_statistics_report()
    analysis_time = time.time() - start_analysis
    
    print_report(full_report)
    print(f"\n⏱️  Tiempo de análisis: {analysis_time:.2f}s\n")
    
    # 4. Grado de nodos
    print_section("4️⃣  GRADO DE NODOS")
    print("🔢 Calculando grado de nodos...\n")
    
    degrees = analyzer.calculate_node_degrees()
    print(f"Total de nodos: {len(degrees)}\n")
    
    print("TOP 15 TÉRMINOS POR GRADO:")
    top_nodes = analyzer.get_top_nodes_by_degree(15)
    for i, (node, degree) in enumerate(top_nodes, 1):
        print(f"  {i:2d}. {node:30s} - Grado: {degree:3d}")
    
    # 5. Componentes conexas
    print_section("5️⃣  DETECCIÓN DE COMPONENTES CONEXAS")
    print("🔍 Detectando componentes conexas...\n")
    
    components_stats = analyzer.get_connected_components_with_stats()
    print(f"Número total de componentes: {len(components_stats)}\n")
    
    for i, comp in enumerate(components_stats[:10], 1):  # Mostrar primeras 10
        print(f"Componente {i}:")
        print(f"  • Tamaño: {comp['size']} nodos")
        print(f"  • Aristas: {comp['edges']}")
        print(f"  • Densidad: {comp['density']:.4f}")
        print(f"  • Grado promedio: {comp['average_degree']:.2f}")
        if comp['size'] <= 10:
            print(f"  • Términos: {', '.join(comp['nodes'])}")
        else:
            print(f"  • Términos (primeros 5): {', '.join(comp['nodes'][:5])} ...")
        print()
    
    if len(components_stats) > 10:
        print(f"... y {len(components_stats) - 10} componentes más.\n")
    
    # 6. Centralidad
    print_section("6️⃣  MEDIDAS DE CENTRALIDAD")
    print("🎯 Calculando medidas de centralidad...\n")
    
    print("CENTRALIDAD DE GRADO (Normalizados):")
    degree_centrality = analyzer.get_centrality_measures('degree')
    sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (node, centrality) in enumerate(sorted_degree, 1):
        print(f"  {i:2d}. {node:30s} - Centralidad: {centrality:.4f}")
    
    print("\nCLUSTERING COEFFICIENT:")
    clustering = analyzer.get_clustering_coefficient()
    sorted_clustering = sorted(clustering.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (node, coeff) in enumerate(sorted_clustering, 1):
        print(f"  {i:2d}. {node:30s} - Coeficiente: {coeff:.4f}")
    
    # 7. Cliques
    print_section("7️⃣  DETECCIÓN DE CLIQUES")
    print("🔗 Buscando cliques (subgrafos completamente conectados)...\n")
    
    cliques = analyzer.find_cliques(min_size=3)
    print(f"Número de cliques (mínimo 3 nodos): {len(cliques)}\n")
    
    for i, clique in enumerate(sorted(cliques, key=len, reverse=True)[:10], 1):
        print(f"  Clique {i} (tamaño {len(clique)}): {', '.join(clique)}")
    
    # 8. Generar visualizaciones
    print_section("8️⃣  GENERANDO VISUALIZACIONES")
    print("🎨 Generando gráficos...\n")
    
    start_viz = time.time()
    visualizer = GraphVisualizer(cg.get_graph(), figsize=(16, 12))
    
    # Grafo principal
    print("  ▪ Generando grafo principal...", end=" ", flush=True)
    visualizer.plot_graph(layout_type='spring', figsize=(16, 12),
                         save_path=str(output_dir / 'cooccurrence_graph.png'))
    print("✓")
    
    # Componentes conexas
    print("  ▪ Generando visualización de componentes...", end=" ", flush=True)
    visualizer.plot_connected_components(analyzer, figsize=(15, 10),
                                        save_path=str(output_dir / 'connected_components.png'))
    print("✓")
    
    # Distribución de grados
    print("  ▪ Generando distribución de grados...", end=" ", flush=True)
    visualizer.plot_degree_distribution(analyzer, 
                                       save_path=str(output_dir / 'degree_distribution.png'))
    print("✓")
    
    # Nodos principales
    print("  ▪ Generando gráfico de nodos principales...", end=" ", flush=True)
    visualizer.plot_top_nodes(analyzer, k=15, 
                             save_path=str(output_dir / 'top_nodes.png'))
    print("✓")
    
    # Coeficiente de clustering
    print("  ▪ Generando distribución de clustering...", end=" ", flush=True)
    visualizer.plot_clustering_coefficient_distribution(analyzer,
                                                       save_path=str(output_dir / 'clustering_distribution.png'))
    print("✓")
    
    viz_time = time.time() - start_viz
    print(f"\n⏱️  Tiempo de visualizaciones: {viz_time:.2f}s\n")
    
    # 9. Generar reporte JSON
    print_section("9️⃣  GENERANDO REPORTES")
    print("📄 Guardando reporte JSON...", end=" ", flush=True)
    json_report = generate_json_report(analyzer, output_dir / 'analysis_report.json')
    print("✓")
    print(f"   Guardado en: {output_dir / 'analysis_report.json'}\n")
    
    # 10. Resumen final
    print_section("🔟 RESUMEN FINAL")
    print(f"📁 Resultados guardados en:")
    print(f"   {output_dir}\n")
    
    print("📋 Archivos generados:")
    total_size = 0
    for file in sorted(output_dir.glob('*')):
        if file.is_file():
            size_kb = file.stat().st_size / 1024
            total_size += size_kb
            print(f"   • {file.name:40s} ({size_kb:8.1f} KB)")
    
    print(f"\n   📊 Tamaño total: {total_size/1024:.2f} MB\n")
    
    # Tiempo total
    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    
    print("="*70)
    print(f"✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
    print(f"⏱️  Tiempo total: {minutes}m {seconds}s")
    print("="*70)
    print("\n💡 Próximos pasos:")
    print("   1. Ver las imágenes PNG en la carpeta 'output'")
    print("   2. Analizar el archivo 'analysis_report.json' para datos detallados")
    print("   3. Usar main_fast.py para análisis rápidos con menos documentos\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Análisis interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la ejecución: {str(e)}")
        import traceback
        traceback.print_exc()