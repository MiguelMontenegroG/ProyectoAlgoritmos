"""
Script principal para análisis de grafo de coocurrencia de términos.
Integra carga de datos, construcción del grafo, análisis y visualización.
"""

import sys
import os
from pathlib import Path

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


def load_abstracts_from_bibtex(file_path):
    """
    Carga abstracts desde un archivo BibTeX.
    
    Args:
        file_path (str): Ruta al archivo .bib
        
    Returns:
        list: Lista de abstracts
    """
    try:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        with open(file_path, 'r', encoding='utf-8') as bibtex_file:
            entries = bibtexparser.load(bibtex_file, parser=parser).entries
        
        abstracts = []
        for entry in entries:
            if 'abstract' in entry and entry['abstract'].strip():
                abstracts.append(entry['abstract'])
        
        print(f"✓ Se cargaron {len(abstracts)} abstracts de {len(entries)} entradas")
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
    """Función principal."""
    
    print("\n" + "="*70)
    print("  ANÁLISIS DE GRAFO DE COOCURRENCIA DE TÉRMINOS")
    print("="*70)
    
    # Configuración
    bibtex_file = r'C:\Users\ANGEL\Documents\GitHub\ProyectoAlgoritmos\output\unified_cleaned.bib'
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # 1. Cargar abstracts
    print_section("1. CARGA DE DATOS")
    abstracts = load_abstracts_from_bibtex(bibtex_file)
    
    if not abstracts:
        print("✗ No se pudieron cargar abstracts. Abortando...")
        return
    
    # 2. Construir grafo de coocurrencia
    print_section("2. CONSTRUCCIÓN DEL GRAFO DE COOCURRENCIA")
    print("Procesando documentos y construyendo grafo...")
    cg = build_cooccurrence_graph_from_abstracts(abstracts, min_cooccurrence=1)
    stats = cg.get_statistics()
    
    print(f"✓ Grafo construido exitosamente:")
    print(f"  • Nodos (términos únicos): {stats['total_nodes']}")
    print(f"  • Aristas (coocurrencias): {stats['total_edges']}")
    print(f"  • Documentos procesados: {stats['total_documents']}")
    print(f"  • Densidad del grafo: {stats['density']:.6f}")
    print(f"  • Grado promedio: {stats['average_degree']:.2f}")
    
    # 3. Análisis del grafo
    print_section("3. ANÁLISIS DEL GRAFO")
    analyzer = GraphAnalyzer(cg.get_graph())
    full_report = analyzer.get_graph_statistics_report()
    print_report(full_report)
    
    # 4. Grado de nodos
    print_section("4. GRADO DE NODOS")
    degrees = analyzer.calculate_node_degrees()
    print(f"Total de nodos: {len(degrees)}\n")
    
    print("TOP 15 TÉRMINOS POR GRADO:")
    top_nodes = analyzer.get_top_nodes_by_degree(15)
    for i, (node, degree) in enumerate(top_nodes, 1):
        print(f"  {i:2d}. {node:30s} - Grado: {degree:3d}")
    
    # 5. Componentes conexas
    print_section("5. DETECCIÓN DE COMPONENTES CONEXAS")
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
    print_section("6. MEDIDAS DE CENTRALIDAD")
    
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
    print_section("7. DETECCIÓN DE CLIQUES")
    cliques = analyzer.find_cliques(min_size=3)
    print(f"Número de cliques (mínimo 3 nodos): {len(cliques)}\n")
    
    for i, clique in enumerate(sorted(cliques, key=len, reverse=True)[:10], 1):
        print(f"  Clique {i} (tamaño {len(clique)}): {', '.join(clique)}")
    
    # 8. Generar visualizaciones
    print_section("8. GENERANDO VISUALIZACIONES")
    
    visualizer = GraphVisualizer(cg.get_graph(), figsize=(16, 12))
    
    # Grafo principal
    print("  • Generando grafo principal...")
    visualizer.plot_graph(layout_type='spring', figsize=(16, 12),
                         save_path=str(output_dir / 'cooccurrence_graph.png'))
    
    # Componentes conexas
    print("  • Generando visualización de componentes...")
    visualizer.plot_connected_components(analyzer, figsize=(15, 10),
                                        save_path=str(output_dir / 'connected_components.png'))
    
    # Distribución de grados
    print("  • Generando distribución de grados...")
    visualizer.plot_degree_distribution(analyzer, 
                                       save_path=str(output_dir / 'degree_distribution.png'))
    
    # Nodos principales
    print("  • Generando gráfico de nodos principales...")
    visualizer.plot_top_nodes(analyzer, k=15, 
                             save_path=str(output_dir / 'top_nodes.png'))
    
    # Coeficiente de clustering
    print("  • Generando distribución de clustering...")
    visualizer.plot_clustering_coefficient_distribution(analyzer,
                                                       save_path=str(output_dir / 'clustering_distribution.png'))
    
    # 9. Generar reporte JSON
    print_section("9. GENERANDO REPORTES")
    json_report = generate_json_report(analyzer, output_dir / 'analysis_report.json')
    print(f"✓ Reporte JSON guardado en: {output_dir / 'analysis_report.json'}")
    
    # 10. Resumen final
    print_section("10. RESUMEN FINAL")
    print(f"Resultados guardados en: {output_dir}")
    print("\nArchivos generados:")
    for file in sorted(output_dir.glob('*')):
        if file.is_file():
            size_kb = file.stat().st_size / 1024
            print(f"  • {file.name} ({size_kb:.1f} KB)")
    
    print("\n✓ Análisis completado exitosamente")


if __name__ == "__main__":
    main()