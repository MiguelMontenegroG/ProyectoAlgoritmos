"""
Módulo para analizar grafos de coocurrencia.
Proporciona métricas y análisis de componentes conexas.
"""

import networkx as nx
from collections import defaultdict, Counter
import heapq


class GraphAnalyzer:
    """Analiza las propiedades de un grafo de coocurrencia."""
    
    def __init__(self, graph):
        """
        Inicializa el analizador.
        
        Args:
            graph (nx.Graph): Grafo a analizar
        """
        self.graph = graph
        self.degree_dict = None
        self.connected_components = None
        
    def calculate_node_degrees(self):
        """
        Calcula el grado de cada nodo.
        
        Returns:
            dict: Diccionario con grados de cada nodo
        """
        self.degree_dict = dict(self.graph.degree())
        return self.degree_dict
    
    def get_top_nodes_by_degree(self, k=10):
        """
        Obtiene los k nodos con mayor grado.
        
        Args:
            k (int): Número de nodos a retornar
            
        Returns:
            list: Lista de tuplas (nodo, grado)
        """
        if self.degree_dict is None:
            self.calculate_node_degrees()
        
        return sorted(self.degree_dict.items(), key=lambda x: x[1], reverse=True)[:k]
    
    def get_connected_components(self):
        """
        Detecta componentes conexas del grafo.
        
        Returns:
            list: Lista de componentes conexas (cada una es un conjunto de nodos)
        """
        self.connected_components = list(nx.connected_components(self.graph))
        return self.connected_components
    
    def get_connected_components_with_stats(self):
        """
        Retorna componentes conexas con estadísticas.
        
        Returns:
            list: Lista de dicts con info de cada componente
        """
        if self.connected_components is None:
            self.get_connected_components()
        
        components_stats = []
        for i, component in enumerate(self.connected_components):
            subgraph = self.graph.subgraph(component)
            stats = {
                'id': i,
                'size': len(component),
                'nodes': list(component),
                'edges': subgraph.number_of_edges(),
                'density': nx.density(subgraph) if len(component) > 1 else 0,
                'average_degree': sum(dict(subgraph.degree()).values()) / len(component)
            }
            components_stats.append(stats)
        
        # Ordenar por tamaño descendente
        return sorted(components_stats, key=lambda x: x['size'], reverse=True)
    
    def get_node_neighbors(self, node, only_direct=True):
        """
        Obtiene los vecinos de un nodo.
        
        Args:
            node: Nodo a consultar
            only_direct (bool): Si True, solo vecinos directos. Si False, todos alcanzables.
            
        Returns:
            list: Lista de vecinos
        """
        if node not in self.graph:
            return []
        
        if only_direct:
            return list(self.graph.neighbors(node))
        else:
            # BFS para obtener todos los nodos alcanzables
            visited = set()
            queue = [node]
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                queue.extend(self.graph.neighbors(current))
            return list(visited - {node})
    
    def get_edge_weights_distribution(self):
        """
        Retorna la distribución de pesos de las aristas.
        
        Returns:
            dict: Distribución de pesos
        """
        weights = [data['weight'] for _, _, data in self.graph.edges(data=True)]
        distribution = Counter(weights)
        return dict(sorted(distribution.items()))
    
    def get_centrality_measures(self, measure='betweenness'):
        """
        Calcula medidas de centralidad de los nodos.
        
        Args:
            measure (str): Tipo de centralidad ('betweenness', 'closeness', 'degree', 'eigenvector')
            
        Returns:
            dict: Centralidad de cada nodo
        """
        if measure == 'betweenness':
            return nx.betweenness_centrality(self.graph, weight='weight')
        elif measure == 'closeness':
            return nx.closeness_centrality(self.graph, distance='weight')
        elif measure == 'degree':
            if self.degree_dict is None:
                self.calculate_node_degrees()
            max_degree = max(self.degree_dict.values()) if self.degree_dict else 1
            return {node: degree/max_degree for node, degree in self.degree_dict.items()}
        elif measure == 'eigenvector':
            try:
                return nx.eigenvector_centrality(self.graph, weight='weight', max_iter=1000)
            except:
                return self.get_centrality_measures('degree')
        else:
            return {}
    
    def get_triangles(self):
        """
        Calcula el número de triángulos (ciclos de 3 nodos).
        
        Returns:
            dict: Número de triángulos por nodo
        """
        return nx.triangles(self.graph)
    
    def get_clustering_coefficient(self):
        """
        Calcula el coeficiente de clustering para cada nodo.
        
        Returns:
            dict: Coeficiente de clustering por nodo
        """
        return nx.clustering(self.graph, weight='weight')
    
    def get_average_clustering_coefficient(self):
        """Retorna el coeficiente de clustering promedio del grafo."""
        return nx.average_clustering(self.graph, weight='weight')
    
    def find_cliques(self, min_size=3):
        """
        Encuentra cliques (subgrafos completamente conectados).
        
        Args:
            min_size (int): Tamaño mínimo de cliques
            
        Returns:
            list: Lista de cliques
        """
        cliques = list(nx.find_cliques(self.graph))
        return [c for c in cliques if len(c) >= min_size]
    
    def get_graph_diameter(self):
        """
        Retorna el diámetro del grafo.
        
        Returns:
            int or float: Diámetro del grafo
        """
        if self.graph.number_of_nodes() == 0:
            return 0
        
        if not nx.is_connected(self.graph):
            # Para grafos desconectados, retorna el diámetro de la componente más grande
            largest_cc = max(nx.connected_components(self.graph), key=len)
            subgraph = self.graph.subgraph(largest_cc)
            return nx.diameter(subgraph)
        
        return nx.diameter(self.graph)
    
    def get_graph_statistics_report(self):
        """
        Genera un reporte completo de estadísticas del grafo.
        
        Returns:
            dict: Reporte completo
        """
        self.calculate_node_degrees()
        
        report = {
            'basic_stats': {
                'nodes': self.graph.number_of_nodes(),
                'edges': self.graph.number_of_edges(),
                'density': nx.density(self.graph)
            },
            'degree_stats': {
                'average_degree': sum(self.degree_dict.values()) / len(self.degree_dict) if self.degree_dict else 0,
                'max_degree': max(self.degree_dict.values()) if self.degree_dict else 0,
                'min_degree': min(self.degree_dict.values()) if self.degree_dict else 0
            },
            'connectivity': {
                'is_connected': nx.is_connected(self.graph),
                'num_components': nx.number_connected_components(self.graph),
                'diameter': self.get_graph_diameter()
            },
            'clustering': {
                'avg_clustering_coefficient': self.get_average_clustering_coefficient(),
                'triangles': sum(self.get_triangles().values()) // 3  # Dividir por 3 porque cada triángulo se cuenta 3 veces
            },
            'top_nodes_by_degree': self.get_top_nodes_by_degree(10)
        }
        
        return report