"""
Ejemplo simple de uso del analizador de similitud textual
"""

from src.similarity.text_similarity_analyzer import TextSimilarityAnalyzer

# Dos abstracts de ejemplo
abstract1 = """
Machine learning is a subset of artificial intelligence that enables systems 
to learn and improve from experience without being explicitly programmed. 
It focuses on developing algorithms that can access data and use it to learn 
for themselves. Deep learning is part of machine learning methods based on 
artificial neural networks with representation learning.
"""

abstract2 = """
Artificial intelligence encompasses machine learning, which allows computers 
to learn from data without explicit programming. Machine learning algorithms 
identify patterns in data and make predictions or decisions based on those patterns. 
Deep neural networks represent a significant advancement in machine learning capabilities, 
enabling computers to process complex information efficiently.
"""

# Abstract completamente diferente
abstract3 = """
Quantum computing represents a paradigm shift in computational technology, 
leveraging quantum mechanics principles like superposition and entanglement. 
Unlike classical computers that use bits, quantum computers use quantum bits or qubits, 
which can exist in multiple states simultaneously. This allows quantum computers 
to perform certain calculations exponentially faster than classical computers.
"""

print("="*80)
print("EJEMPLO: Análisis de Similitud Textual")
print("="*80)

# Análisis 1: Abstracts similares
print("\n✓ ANÁLISIS 1: Abstracts Similares (ML)")
print("-" * 80)

analyzer1 = TextSimilarityAnalyzer(abstract1, abstract2)
print("\nTexto 1 (primeras 150 caracteres):")
print(abstract1[:150] + "...")
print("\nTexto 2 (primeras 150 caracteres):")
print(abstract2[:150] + "...")

# Calcular todos los algoritmos
print("\n\nCalculando similitud con todos los algoritmos...")
analyzer1.compute_all()

# Obtener comparación
comparison1 = analyzer1.compare_all()

print("\nRESULTADOS:")
for algo, similitud in comparison1['similarities'].items():
    print(f"  {algo:25} {similitud:.4f} {'█' * int(similitud*20)}")

print(f"\nPromedio de similitud: {sum(comparison1['values'])/len(comparison1['values']):.4f}")

# Análisis 2: Abstracts muy diferentes
print("\n\n" + "="*80)
print("✓ ANÁLISIS 2: Abstracts Diferentes (ML vs. Quantum Computing)")
print("-" * 80)

analyzer2 = TextSimilarityAnalyzer(abstract1, abstract3)
print("\nTexto 1: Machine Learning (primeras 150 caracteres)")
print(abstract1[:150] + "...")
print("\nTexto 3: Quantum Computing (primeras 150 caracteres)")
print(abstract3[:150] + "...")

print("\n\nCalculando similitud...")
analyzer2.compute_all()
comparison2 = analyzer2.compare_all()

print("\nRESULTADOS:")
for algo, similitud in comparison2['similarities'].items():
    print(f"  {algo:25} {similitud:.4f} {'█' * int(similitud*20)}")

print(f"\nPromedio de similitud: {sum(comparison2['values'])/len(comparison2['values']):.4f}")

# Análisis 3: Análisis detallado de un algoritmo
print("\n\n" + "="*80)
print("✓ ANÁLISIS 3: Detalles Paso a Paso (Jaro-Winkler)")
print("="*80)

from src.similarity.jaro_winkler import jaro_winkler_detailed

ejemplo_text1 = "Machine Learning"
ejemplo_text2 = "Machne Lerning"  # Con errores tipográficos

detailed = jaro_winkler_detailed(ejemplo_text1, ejemplo_text2)

print(f"\nTexto 1: {detailed['texto1']}")
print(f"Texto 2: {detailed['texto2']}")

print(f"\nPaso 1: Longitudes")
print(f"  |s1| = {detailed['paso_1_longitud_s1']}")
print(f"  |s2| = {detailed['paso_1_longitud_s2']}")

print(f"\nPaso 2: Ventana de búsqueda")
print(f"  match_window = {detailed['paso_2_ventana_coincidencia']}")

print(f"\nPaso 3-5: JARO")
print(f"  Caracteres coincidentes: {detailed['paso_3_caracteres_coincidentes']}")
print(f"  Transposiciones: {detailed['paso_4_transposiciones']}")
print(f"  Similitud JARO: {detailed['paso_5_jaro_resultado']}")

print(f"\nPaso 6-8: JARO-WINKLER")
print(f"  Prefijo común: '{detailed['paso_6_prefijo_comun']}'")
print(f"  Longitud prefijo: {detailed['paso_6_longitud_prefijo']}")
print(f"  Factor escala: {detailed['paso_7_factor_escala']}")
print(f"  Similitud JARO-WINKLER: {detailed['resultado_jaro_winkler']}")

# Análisis 4: Jaccard
print("\n\n" + "="*80)
print("✓ ANÁLISIS 4: Detalles Paso a Paso (Jaccard)")
print("="*80)

from src.similarity.jaccard_similarity import jaccard_similarity_detailed

ejemplo_text1 = "machine learning algorithm"
ejemplo_text2 = "deep learning algorithm model"

detailed_jaccard = jaccard_similarity_detailed(ejemplo_text1, ejemplo_text2)

print(f"\nTexto 1: {detailed_jaccard['texto1']}")
print(f"Texto 2: {detailed_jaccard['texto2']}")

print(f"\nPaso 1: Tokens Texto 1")
print(f"  {detailed_jaccard['paso_1_tokens_texto1']}")

print(f"\nPaso 2: Tokens Texto 2")
print(f"  {detailed_jaccard['paso_2_tokens_texto2']}")

print(f"\nPaso 3: Intersección (palabras comunes)")
print(f"  {detailed_jaccard['paso_3_interseccion']}")
print(f"  Tamaño: {detailed_jaccard['paso_3_interseccion_size']}")

print(f"\nPaso 4: Unión (palabras únicas)")
print(f"  Tamaño: {detailed_jaccard['paso_4_union_size']}")

print(f"\nPaso 5: Fórmula Jaccard")
print(f"  {detailed_jaccard['paso_5_formula']}")
print(f"  Similitud: {detailed_jaccard['resultado_similitud_jaccard']}")

# Conclusión
print("\n\n" + "="*80)
print("CONCLUSIÓN")
print("="*80)
print("""
Este ejemplo demuestra el uso de los 6 algoritmos de similitud textual:

ALGORITMOS CLÁSICOS:
1. Levenshtein    - Basado en ediciones de caracteres
2. Jaccard        - Basado en conjuntos de palabras
3. Jaro-Winkler   - Optimizado para errores tipográficos
4. TF-IDF+Coseno  - Vectorización estadística

MODELOS DE IA:
5. BERT           - Contexto bidireccional
6. Sentence-BERT  - Optimizado para similitud semántica

Para máxima precisión en similitud de abstracts científicos:
→ Usa SENTENCE-BERT (all-MiniLM-L6-v2)

Para análisis interactivo:
→ Ejecuta: jupyter notebook Text_Similarity_Analysis.ipynb
""")

print("\n✓ Ejemplo completado exitosamente")