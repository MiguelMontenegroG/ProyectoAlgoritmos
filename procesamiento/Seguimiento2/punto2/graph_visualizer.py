"""
Módulo para visualizar grafos de coocurrencia.
Proporciona funcionalidades para generar gráficos estáticos e interactivos.
"""

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import numpy as np


class GraphVisualizer:
    """Visualiza grafos de coocurrencia."""
    
    def __init__(self, graph, figsize=(14, 10)):
        """
        Inicializa el visualizador.
        
        Args:
            graph (nx.Graph): Grafo a visualizar
            figsize (tuple): Tamaño de la figura (ancho, alto)
        """
        self.graph = graph
        self.figsize = figsize
        self.pos = None
    
    def calculate_layout(self, layout_type='spring', seed=42):
        """
        Calcula las posiciones de los nodos.
        
        Args:
            layout_type (str): Tipo de layout ('spring', 'circular', 'kamada_kawai')
            seed (int): Seed para reproducibilidad
            
        Returns:
            dict: Diccionario con posiciones
        """
        if layout_type == 'spring':
            self.pos = nx.spring_layout(self.graph, k=2, iterations=50, seed=seed)
        elif layout_type == 'circular':
            self.pos = nx.circular_layout(self.graph)
        elif layout_type == 'kamada_kawai':
            self.pos = nx.kamada_kawai_layout(self.graph)
        else:
            self.pos = nx.spring_layout(self.graph, seed=seed)
        
        return self.pos
    
    def plot_graph(self, layout_type='spring', node_size_method='degree', 
                   figsize=None, title="Grafo de Coocurrencia de Términos", 
                   save_path=None, show_labels=True):
        """
        Genera una visualización del grafo.
        
        Args:
            layout_type (str): Tipo de layout
            node_size_method (str): Método para tamaño de nodos ('degree', 'frequency')
            figsize (tuple): Tamaño de figura
            title (str): Título del gráfico
            save_path (str): Ruta para guardar la imagen
            show_labels (bool): Si mostrar etiquetas
        """
        if figsize:
            self.figsize = figsize
        
        # Calcular layout
        if self.pos is None:
            self.calculate_layout(layout_type)
        
        # Crear figura
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Calcular tamaño de nodos
        if node_size_method == 'degree':
            node_sizes = [self.graph.degree(node) * 100 for node in self.graph.nodes()]
        elif node_size_method == 'frequency':
            node_sizes = [self.graph.nodes[node].get('frequency', 1) * 100 for node in self.graph.nodes()]
        else:
            node_sizes = [300] * self.graph.number_of_nodes()
        
        # Calcular ancho de aristas basado en peso
        edges = self.graph.edges()
        weights = [self.graph[u][v]['weight'] for u, v in edges]
        max_weight = max(weights) if weights else 1
        edge_widths = [2 + (w / max_weight) * 3 for w in weights]
        
        # Dibujar grafo
        nx.draw_networkx_nodes(self.graph, self.pos, node_size=node_sizes, 
                              node_color='lightblue', ax=ax, alpha=0.9, 
                              edgecolors='darkblue', linewidths=2)
        
        nx.draw_networkx_edges(self.graph, self.pos, width=edge_widths, 
                              alpha=0.5, edge_color='gray', ax=ax)
        
        if show_labels:
            nx.draw_networkx_labels(self.graph, self.pos, font_size=8, 
                                   font_weight='bold', ax=ax)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Agregar leyenda
        legend_text = f"Nodos: {self.graph.number_of_nodes()} | Aristas: {self.graph.number_of_edges()}"
        ax.text(0.02, 0.02, legend_text, transform=ax.transAxes, 
               fontsize=10, verticalalignment='bottom',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico guardado en: {save_path}")
        
        return fig, ax
    
    def plot_connected_components(self, analyzer, figsize=None, save_path=None):
        """
        Visualiza las componentes conexas del grafo.
        
        Args:
            analyzer: Objeto GraphAnalyzer
            figsize (tuple): Tamaño de figura
            save_path (str): Ruta para guardar
        """
        if figsize:
            self.figsize = figsize
        
        components = analyzer.get_connected_components()
        n_components = len(components)
        
        # Calcular disposición de subplots
        cols = min(3, n_components)
        rows = (n_components + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
        if n_components == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        for idx, component in enumerate(components):
            ax = axes[idx]
            
            # Crear subgrafo
            subgraph = self.graph.subgraph(component)
            
            # Calcular layout para la componente
            pos = nx.spring_layout(subgraph, k=2, iterations=50)
            
            # Dibujar
            node_sizes = [subgraph.degree(node) * 100 for node in subgraph.nodes()]
            
            nx.draw_networkx_nodes(subgraph, pos, node_size=node_sizes, 
                                  node_color='lightcoral', ax=ax, alpha=0.9,
                                  edgecolors='darkred', linewidths=2)
            
            nx.draw_networkx_edges(subgraph, pos, width=2, alpha=0.5, 
                                  edge_color='gray', ax=ax)
            
            nx.draw_networkx_labels(subgraph, pos, font_size=8, 
                                   font_weight='bold', ax=ax)
            
            title = f"Componente {idx+1} (Nodos: {len(component)})"
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.axis('off')
        
        # Ocultar subplots vacíos
        for idx in range(n_components, len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico de componentes guardado en: {save_path}")
        
        return fig, axes
    
    def plot_degree_distribution(self, analyzer, save_path=None):
        """
        Genera un histograma de distribución de grados.
        
        Args:
            analyzer: Objeto GraphAnalyzer
            save_path (str): Ruta para guardar
        """
        degrees = dict(analyzer.calculate_node_degrees())
        degree_values = list(degrees.values())
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histograma
        ax1.hist(degree_values, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Grado del nodo', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
        ax1.set_title('Distribución de Grados', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de probabilidad acumulada
        sorted_degrees = sorted(degree_values)
        cumulative = np.arange(1, len(sorted_degrees) + 1) / len(sorted_degrees)
        ax2.plot(sorted_degrees, cumulative, marker='o', linestyle='-', 
                color='darkblue', alpha=0.7)
        ax2.set_xlabel('Grado del nodo', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Probabilidad acumulada', fontsize=12, fontweight='bold')
        ax2.set_title('Probabilidad Acumulada de Grados', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico de distribución guardado en: {save_path}")
        
        return fig, (ax1, ax2)
    
    def plot_top_nodes(self, analyzer, k=15, save_path=None):
        """
        Visualiza los nodos con mayor grado.
        
        Args:
            analyzer: Objeto GraphAnalyzer
            k (int): Número de nodos a mostrar
            save_path (str): Ruta para guardar
        """
        top_nodes = analyzer.get_top_nodes_by_degree(k)
        
        if not top_nodes:
            print("No hay nodos para visualizar")
            return
        
        nodes, degrees = zip(*top_nodes)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(nodes)))
        bars = ax.barh(range(len(nodes)), degrees, color=colors, edgecolor='black', linewidth=1.5)
        
        ax.set_yticks(range(len(nodes)))
        ax.set_yticklabels(nodes, fontsize=11)
        ax.set_xlabel('Grado', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {k} Términos por Grado (Conexiones)', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        ax.grid(True, axis='x', alpha=0.3)
        
        # Agregar valores en las barras
        for i, (bar, degree) in enumerate(zip(bars, degrees)):
            ax.text(degree, bar.get_y() + bar.get_height()/2, f' {int(degree)}',
                   va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico de nodos principales guardado en: {save_path}")
        
        return fig, ax
    
    def plot_clustering_coefficient_distribution(self, analyzer, save_path=None):
        """
        Visualiza la distribución del coeficiente de clustering.
        
        Args:
            analyzer: Objeto GraphAnalyzer
            save_path (str): Ruta para guardar
        """
        clustering_coeff = analyzer.get_clustering_coefficient()
        values = list(clustering_coeff.values())
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(values, bins=20, color='mediumpurple', edgecolor='black', alpha=0.7)
        ax.axvline(np.mean(values), color='red', linestyle='--', linewidth=2, label=f'Media: {np.mean(values):.3f}')
        ax.set_xlabel('Coeficiente de Clustering', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
        ax.set_title('Distribución del Coeficiente de Clustering', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico de clustering guardado en: {save_path}")
        
        return fig, ax