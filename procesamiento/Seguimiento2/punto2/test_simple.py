#!/usr/bin/env python
"""Test simple del grafo de coocurrencia."""

import sys
sys.path.insert(0, '.')

from cooccurrence_graph import build_cooccurrence_graph_from_abstracts
from graph_analyzer import GraphAnalyzer

# Test simple
abstracts = [
    'Machine learning and deep learning are powerful',
    'Deep learning requires large training data',
    'Machine learning models use neural networks',
    'Artificial intelligence includes machine learning',
    'Neural networks power deep learning systems'
]

print("=" * 70)
print("TEST SIMPLE - CONSTRUCCIÓN DEL GRAFO")
print("=" * 70)

print("\n1. Construyendo grafo de coocurrencia...")
cg = build_cooccurrence_graph_from_abstracts(abstracts)

print("2. Obteniendo estadísticas...")
stats = cg.get_statistics()

print("\n✓ Grafo construido exitosamente")
print(f"  • Nodos (términos únicos): {stats['total_nodes']}")
print(f"  • Aristas (coocurrencias): {stats['total_edges']}")
print(f"  • Densidad: {stats['density']:.4f}")

print("\n3. Analizando grados de nodos...")
analyzer = GraphAnalyzer(cg.get_graph())
top_nodes = analyzer.get_top_nodes_by_degree(5)

print("\nTérminos más conectados:")
for i, (term, degree) in enumerate(top_nodes, 1):
    print(f"  {i}. {term:25s} - Grado: {degree}")

print("\n4. Detectando componentes conexas...")
components = analyzer.get_connected_components()
print(f"\n✓ Se encontraron {len(components)} componente(s) conexa(s)")

print("\n" + "=" * 70)
print("✓✓ TEST COMPLETADO EXITOSAMENTE")
print("=" * 70)