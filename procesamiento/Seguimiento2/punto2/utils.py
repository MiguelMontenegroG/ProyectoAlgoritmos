"""
Utilidades auxiliares para el análisis de grafo de coocurrencia.
"""

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from pathlib import Path
import json
from datetime import datetime


def load_abstracts_from_bibtex(file_path, max_abstracts=None, sample=False):
    """
    Carga abstracts desde un archivo BibTeX.
    
    Args:
        file_path (str o Path): Ruta al archivo .bib
        max_abstracts (int): Número máximo de abstracts a cargar (None = todos)
        sample (bool): Si True, carga una muestra aleatoria
        
    Returns:
        tuple: (abstracts_list, entries_dict)
    """
    try:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        
        with open(file_path, 'r', encoding='utf-8') as bibtex_file:
            entries = bibtexparser.load(bibtex_file, parser=parser).entries
        
        abstracts = []
        abstracts_data = []
        
        for entry in entries:
            if 'abstract' in entry and entry['abstract'].strip():
                abstracts.append(entry['abstract'])
                abstracts_data.append({
                    'id': entry.get('ID', 'unknown'),
                    'title': entry.get('title', 'Unknown'),
                    'author': entry.get('author', 'Unknown'),
                    'year': entry.get('year', 'Unknown'),
                    'abstract': entry['abstract']
                })
        
        if max_abstracts and len(abstracts) > max_abstracts:
            if sample:
                import random
                indices = random.sample(range(len(abstracts)), max_abstracts)
                abstracts = [abstracts[i] for i in indices]
                abstracts_data = [abstracts_data[i] for i in indices]
            else:
                abstracts = abstracts[:max_abstracts]
                abstracts_data = abstracts_data[:max_abstracts]
        
        print(f"✓ Cargados {len(abstracts)} abstracts")
        return abstracts, abstracts_data
    
    except Exception as e:
        print(f"✗ Error al cargar abstracts: {str(e)}")
        return [], []


def save_graph_statistics(graph, analyzer, output_path):
    """
    Guarda estadísticas del grafo en un archivo JSON.
    
    Args:
        graph: Objeto networkx.Graph
        analyzer: Objeto GraphAnalyzer
        output_path (str o Path): Ruta de salida
    """
    try:
        analyzer.calculate_node_degrees()
        components = analyzer.get_connected_components_with_stats()
        
        stats = {
            'timestamp': datetime.now().isoformat(),
            'graph': {
                'nodes': graph.number_of_nodes(),
                'edges': graph.number_of_edges(),
                'density': float(__import__('networkx').density(graph)),
            },
            'degrees': dict(analyzer.degree_dict),
            'top_nodes': analyzer.get_top_nodes_by_degree(20),
            'components': components,
            'metrics': {
                'avg_clustering': float(analyzer.get_average_clustering_coefficient()),
                'diameter': int(analyzer.get_graph_diameter())
            }
        }
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✓ Estadísticas guardadas en: {output_path}")
        return stats
    
    except Exception as e:
        print(f"✗ Error al guardar estadísticas: {str(e)}")
        return None


def export_graph_to_gexf(graph, output_path):
    """
    Exporta el grafo a formato GEXF (compatible con Gephi).
    
    Args:
        graph: Objeto networkx.Graph
        output_path (str o Path): Ruta de salida
    """
    try:
        import networkx as nx
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        nx.write_gexf(graph, str(output_path))
        print(f"✓ Grafo exportado a GEXF: {output_path}")
    except Exception as e:
        print(f"✗ Error al exportar grafo: {str(e)}")


def export_graph_to_graphml(graph, output_path):
    """
    Exporta el grafo a formato GraphML.
    
    Args:
        graph: Objeto networkx.Graph
        output_path (str o Path): Ruta de salida
    """
    try:
        import networkx as nx
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        nx.write_graphml(graph, str(output_path))
        print(f"✓ Grafo exportado a GraphML: {output_path}")
    except Exception as e:
        print(f"✗ Error al exportar grafo: {str(e)}")


def export_components_to_csv(analyzer, output_path):
    """
    Exporta información de componentes a CSV.
    
    Args:
        analyzer: Objeto GraphAnalyzer
        output_path (str o Path): Ruta de salida
    """
    try:
        import csv
        
        components = analyzer.get_connected_components_with_stats()
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Component_ID', 'Size', 'Edges', 'Density', 'Avg_Degree', 'Nodes'])
            
            for comp in components:
                writer.writerow([
                    comp['id'],
                    comp['size'],
                    comp['edges'],
                    f"{comp['density']:.4f}",
                    f"{comp['average_degree']:.2f}",
                    '|'.join(comp['nodes'])
                ])
        
        print(f"✓ Componentes exportadas a CSV: {output_path}")
    
    except Exception as e:
        print(f"✗ Error al exportar componentes: {str(e)}")


def print_component_details(component, graph):
    """
    Imprime detalles detallados de una componente.
    
    Args:
        component (dict): Estadísticas de la componente
        graph: Objeto networkx.Graph
    """
    print(f"\n{'='*70}")
    print(f"COMPONENTE {component['id']}")
    print(f"{'='*70}")
    print(f"Tamaño: {component['size']} nodos")
    print(f"Aristas: {component['edges']}")
    print(f"Densidad: {component['density']:.4f}")
    print(f"Grado promedio: {component['average_degree']:.2f}")
    
    print(f"\nNodos:")
    subgraph = graph.subgraph(component['nodes'])
    degrees = dict(subgraph.degree())
    sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    
    for node, degree in sorted_nodes[:10]:
        print(f"  • {node:30s} (grado: {degree})")
    
    if len(sorted_nodes) > 10:
        print(f"  ... y {len(sorted_nodes) - 10} más")


def get_node_info(graph, analyzer, node):
    """
    Retorna información detallada de un nodo específico.
    
    Args:
        graph: Objeto networkx.Graph
        analyzer: Objeto GraphAnalyzer
        node: Nombre del nodo
        
    Returns:
        dict: Información del nodo
    """
    if node not in graph:
        return None
    
    info = {
        'name': node,
        'degree': graph.degree(node),
        'neighbors': list(graph.neighbors(node)),
        'frequency': graph.nodes[node].get('frequency', 0),
        'edges_weights': {neighbor: graph[node][neighbor]['weight'] for neighbor in graph.neighbors(node)}
    }
    
    clustering = analyzer.get_clustering_coefficient()
    if node in clustering:
        info['clustering_coefficient'] = clustering[node]
    
    return info


def print_node_info(node_info):
    """Imprime información de un nodo de forma legible."""
    if not node_info:
        print("Nodo no encontrado")
        return
    
    print(f"\n{'='*70}")
    print(f"INFORMACIÓN DEL NODO: {node_info['name']}")
    print(f"{'='*70}")
    print(f"Grado: {node_info['degree']}")
    print(f"Frecuencia: {node_info['frequency']}")
    
    if 'clustering_coefficient' in node_info:
        print(f"Coeficiente de Clustering: {node_info['clustering_coefficient']:.4f}")
    
    print(f"\nVecinos directos ({len(node_info['neighbors'])}):")
    for neighbor in sorted(node_info['neighbors']):
        weight = node_info['edges_weights'][neighbor]
        print(f"  • {neighbor:30s} (coocurrencias: {weight})")


def search_terms(graph, search_pattern, limit=10):
    """
    Busca términos que coincidan con un patrón.
    
    Args:
        graph: Objeto networkx.Graph
        search_pattern (str): Patrón de búsqueda (puede usar * como comodín)
        limit (int): Número máximo de resultados
        
    Returns:
        list: Términos coincidentes
    """
    import re
    
    # Convertir patrón a regex
    pattern = search_pattern.replace('*', '.*').replace('?', '.')
    regex = re.compile(f'^{pattern}$', re.IGNORECASE)
    
    matches = [node for node in graph.nodes() if regex.match(node)]
    return matches[:limit]