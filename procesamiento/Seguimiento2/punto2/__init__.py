"""
Módulo Seguimiento2-punto2: Análisis de Grafo de Coocurrencia de Términos

Este módulo implementa un sistema completo para:
1. Construir un grafo no dirigido que represente relaciones entre términos según su coocurrencia
2. Calcular el grado de cada nodo para identificar términos más relacionados
3. Detectar grupos de términos conectados mediante análisis de componentes conexas
"""

from .cooccurrence_graph import CooccurrenceGraph, build_cooccurrence_graph_from_abstracts
from .graph_analyzer import GraphAnalyzer
from .graph_visualizer import GraphVisualizer

__version__ = '1.0.0'
__author__ = 'Proyecto Algoritmos'
__all__ = ['CooccurrenceGraph', 'GraphAnalyzer', 'GraphVisualizer', 'build_cooccurrence_graph_from_abstracts']