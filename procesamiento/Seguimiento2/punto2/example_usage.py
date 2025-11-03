"""
Ejemplos de uso del módulo de análisis de grafo de coocurrencia.

Este script muestra cómo utilizar las clases principales del módulo
en diferentes escenarios.
"""

import sys
from pathlib import Path

# Agregar ruta al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cooccurrence_graph import build_cooccurrence_graph_from_abstracts
from graph_analyzer import GraphAnalyzer
from graph_visualizer import GraphVisualizer
from utils import (
    load_abstracts_from_bibtex,
    save_graph_statistics,
    get_node_info,
    print_node_info,
    search_terms
)


def example_1_basic_usage():
    """Ejemplo 1: Uso básico del grafo de coocurrencia."""
    print("\n" + "="*70)
    print("EJEMPLO 1: USO BÁSICO")
    print("="*70)
    
    # Crear algunos textos de ejemplo
    abstracts = [
        "Machine learning and deep learning are transformative technologies in artificial intelligence",
        "Natural language processing enables machines to understand human language",
        "Deep learning models require large amounts of training data",
        "Artificial intelligence applications include computer vision and robotics",
        "Training data quality is crucial for machine learning model performance"
    ]
    
    # Construir grafo
    print("\n1. Construyendo grafo de coocurrencia...")
    cg = build_cooccurrence_graph_from_abstracts(abstracts, min_cooccurrence=1)
    
    # Obtener estadísticas
    stats = cg.get_statistics()
    print(f"\n2. Estadísticas del grafo:")
    print(f"   - Nodos (términos): {stats['total_nodes']}")
    print(f"   - Aristas (coocurrencias): {stats['total_edges']}")
    print(f"   - Densidad: {stats['density']:.4f}")


def example_2_degree_analysis():
    """Ejemplo 2: Análisis de grados de nodos."""
    print("\n" + "="*70)
    print("EJEMPLO 2: ANÁLISIS DE GRADOS")
    print("="*70)
    
    abstracts = [
        "Generative AI includes models like GPT and BERT for natural language processing",
        "Machine learning algorithms power artificial intelligence systems",
        "Deep learning requires significant computational resources and training data",
        "Transformers revolutionized natural language processing and machine learning",
        "AI applications span computer vision, robotics, and natural language understanding"
    ]
    
    cg = build_cooccurrence_graph_from_abstracts(abstracts)
    analyzer = GraphAnalyzer(cg.get_graph())
    
    print("\n1. Términos más conectados (Top 10):")
    top_nodes = analyzer.get_top_nodes_by_degree(10)
    
    for i, (term, degree) in enumerate(top_nodes, 1):
        print(f"   {i:2d}. {term:30s} - Conexiones: {degree}")


def example_3_connected_components():
    """Ejemplo 3: Detección de componentes conexas."""
    print("\n" + "="*70)
    print("EJEMPLO 3: COMPONENTES CONEXAS")
    print("="*70)
    
    abstracts = [
        "Machine learning and deep learning for AI applications",
        "Computer vision uses convolutional neural networks",
        "Image recognition and object detection in computer vision",
        "NLP processes text and language understanding",
        "Sentiment analysis in natural language processing",
        "Quantum computing and quantum algorithms research",
        "Quantum supremacy in quantum information theory"
    ]
    
    cg = build_cooccurrence_graph_from_abstracts(abstracts)
    analyzer = GraphAnalyzer(cg.get_graph())
    
    components = analyzer.get_connected_components_with_stats()
    
    print(f"\nTotal de componentes conexas: {len(components)}\n")
    
    for comp in components:
        print(f"Componente {comp['id']}:")
        print(f"  - Tamaño: {comp['size']} nodos")
        print(f"  - Aristas: {comp['edges']}")
        print(f"  - Densidad: {comp['density']:.4f}")
        print(f"  - Términos: {', '.join(comp['nodes'][:5])}...")
        print()


def example_4_centrality_measures():
    """Ejemplo 4: Medidas de centralidad."""
    print("\n" + "="*70)
    print("EJEMPLO 4: MEDIDAS DE CENTRALIDAD")
    print("="*70)
    
    abstracts = [
        "Machine learning, deep learning, and neural networks",
        "Deep learning models for computer vision applications",
        "Computer vision, image recognition, and neural networks",
        "Machine learning algorithms and neural network architectures",
        "Deep learning frameworks and neural network training"
    ]
    
    cg = build_cooccurrence_graph_from_abstracts(abstracts)
    analyzer = GraphAnalyzer(cg.get_graph())
    
    print("\n1. Centralidad de Grado (Top 5):")
    degree_centrality = analyzer.get_centrality_measures('degree')
    top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for i, (term, centrality) in enumerate(top_degree, 1):
        print(f"   {i}. {term:25s} - {centrality:.4f}")
    
    print("\n2. Coeficiente de Clustering (Top 5):")
    clustering = analyzer.get_clustering_coefficient()
    top_clustering = sorted(clustering.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for i, (term, coeff) in enumerate(top_clustering, 1):
        print(f"   {i}. {term:25s} - {coeff:.4f}")


def example_5_from_bibtex():
    """Ejemplo 5: Cargar desde archivo BibTeX real."""
    print("\n" + "="*70)
    print("EJEMPLO 5: CARGA DESDE ARCHIVO BIBTEX")
    print("="*70)
    
    bibtex_file = Path(r'C:\Users\ANGEL\Documents\GitHub\ProyectoAlgoritmos\output\unified_cleaned.bib')
    
    if not bibtex_file.exists():
        print(f"✗ Archivo no encontrado: {bibtex_file}")
        return
    
    print(f"\nCargando abstracts desde: {bibtex_file}")
    abstracts, _ = load_abstracts_from_bibtex(str(bibtex_file), max_abstracts=50)
    
    if not abstracts:
        print("No se pudieron cargar abstracts")
        return
    
    cg = build_cooccurrence_graph_from_abstracts(abstracts)
    analyzer = GraphAnalyzer(cg.get_graph())
    
    stats = cg.get_statistics()
    print(f"\nEstadísticas del grafo:")
    print(f"  - Nodos: {stats['total_nodes']}")
    print(f"  - Aristas: {stats['total_edges']}")
    print(f"  - Documentos: {stats['total_documents']}")
    print(f"  - Densidad: {stats['density']:.4f}")
    
    print(f"\nTop 10 términos más conectados:")
    top_nodes = analyzer.get_top_nodes_by_degree(10)
    for i, (term, degree) in enumerate(top_nodes, 1):
        print(f"  {i:2d}. {term:30s} - {degree} conexiones")


def example_6_node_information():
    """Ejemplo 6: Obtener información detallada de un nodo."""
    print("\n" + "="*70)
    print("EJEMPLO 6: INFORMACIÓN DE NODOS")
    print("="*70)
    
    abstracts = [
        "Machine learning is fundamental to artificial intelligence development",
        "Artificial intelligence includes machine learning and deep learning",
        "Deep learning with neural networks improves machine learning performance"
    ]
    
    cg = build_cooccurrence_graph_from_abstracts(abstracts)
    analyzer = GraphAnalyzer(cg.get_graph())
    graph = cg.get_graph()
    
    # Obtener información del nodo "machine learning"
    node_name = "machine learning"
    node_info = get_node_info(graph, analyzer, node_name)
    
    if node_info:
        print(f"\nInformación del término: '{node_name}'")
        print(f"  - Grado: {node_info['degree']}")
        print(f"  - Frecuencia: {node_info['frequency']}")
        
        if 'clustering_coefficient' in node_info:
            print(f"  - Coeficiente de Clustering: {node_info['clustering_coefficient']:.4f}")
        
        print(f"\n  Términos relacionados:")
        for neighbor in node_info['neighbors']:
            weight = node_info['edges_weights'][neighbor]
            print(f"    • {neighbor} (coocurrencias: {weight})")


def example_7_search_terms():
    """Ejemplo 7: Búsqueda de términos."""
    print("\n" + "="*70)
    print("EJEMPLO 7: BÚSQUEDA DE TÉRMINOS")
    print("="*70)
    
    abstracts = [
        "Machine learning and deep learning for AI",
        "Computer vision applications",
        "Natural language processing",
        "Computer graphics and visualization",
        "Machine intelligence systems"
    ]
    
    cg = build_cooccurrence_graph_from_abstracts(abstracts)
    graph = cg.get_graph()
    
    # Buscar términos que contengan "machine"
    print("\nBuscando términos que contengan 'machine':")
    results = search_terms(graph, '*machine*')
    for term in results:
        print(f"  • {term}")
    
    # Buscar términos que contengan "learning"
    print("\nBuscando términos que contengan 'learning':")
    results = search_terms(graph, '*learning*')
    for term in results:
        print(f"  • {term}")


def example_8_visualization():
    """Ejemplo 8: Generar visualizaciones."""
    print("\n" + "="*70)
    print("EJEMPLO 8: VISUALIZACIÓN")
    print("="*70)
    
    abstracts = [
        "Machine learning and deep learning in AI applications",
        "Deep learning neural networks for computer vision",
        "Computer vision and image recognition technology",
        "Natural language processing with machine learning",
        "Artificial intelligence applications in various domains"
    ]
    
    cg = build_cooccurrence_graph_from_abstracts(abstracts)
    analyzer = GraphAnalyzer(cg.get_graph())
    visualizer = GraphVisualizer(cg.get_graph())
    
    output_dir = Path(__file__).parent / 'example_output'
    output_dir.mkdir(exist_ok=True)
    
    print(f"\nGenerando visualizaciones en: {output_dir}\n")
    
    # Grafo principal
    print("  1. Generando grafo principal...")
    visualizer.plot_graph(save_path=str(output_dir / 'example_graph.png'))
    
    # Distribución de grados
    print("  2. Generando distribución de grados...")
    visualizer.plot_degree_distribution(analyzer, 
                                       save_path=str(output_dir / 'example_degrees.png'))
    
    # Nodos principales
    print("  3. Generando gráfico de nodos principales...")
    visualizer.plot_top_nodes(analyzer, k=10,
                             save_path=str(output_dir / 'example_top_nodes.png'))
    
    print("\n✓ Visualizaciones generadas exitosamente")


def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "="*70)
    print("EJEMPLOS DE USO - ANÁLISIS DE GRAFO DE COOCURRENCIA")
    print("="*70)
    
    try:
        example_1_basic_usage()
        example_2_degree_analysis()
        example_3_connected_components()
        example_4_centrality_measures()
        example_6_node_information()
        example_7_search_terms()
        
        # Este ejemplo requiere archivo BibTeX
        try:
            example_5_from_bibtex()
        except Exception as e:
            print(f"\n✗ Ejemplo 5 omitido: {e}")
        
        # Este ejemplo genera archivos
        try:
            example_8_visualization()
        except Exception as e:
            print(f"\n✗ Ejemplo 8 omitido: {e}")
        
        print("\n" + "="*70)
        print("✓ TODOS LOS EJEMPLOS COMPLETADOS")
        print("="*70 + "\n")
    
    except Exception as e:
        print(f"\n✗ Error durante ejecución: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()