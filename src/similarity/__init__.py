"""
Módulo de similitud textual
Implementa 6 algoritmos de similitud: 4 clásicos + 2 con IA
"""

# Algoritmos clásicos
from .edit_distance import edit_distance
from .jaccard_similarity import (
    jaccard_similarity,
    jaccard_distance,
    jaccard_similarity_detailed
)
from .jaro_winkler import (
    jaro_similarity,
    jaro_winkler_similarity,
    jaro_winkler_distance,
    jaro_winkler_detailed
)

# Modelos IA
try:
    from .bert_similarity import (
        bert_similarity,
        bert_similarity_detailed,
        get_bert_embeddings
    )
except ImportError:
    pass

try:
    from .sentence_bert_similarity import (
        sentence_bert_similarity,
        sentence_bert_similarity_detailed,
        sentence_bert_similarity_matrix,
        sentence_bert_embeddings
    )
except ImportError:
    pass

# Analizador integrado
from .text_similarity_analyzer import (
    TextSimilarityAnalyzer,
    analyze_abstracts
)

__all__ = [
    # Clásicos
    'edit_distance',
    'jaccard_similarity',
    'jaccard_distance',
    'jaccard_similarity_detailed',
    'jaro_similarity',
    'jaro_winkler_similarity',
    'jaro_winkler_distance',
    'jaro_winkler_detailed',
    # IA
    'bert_similarity',
    'bert_similarity_detailed',
    'sentence_bert_similarity',
    'sentence_bert_similarity_detailed',
    'sentence_bert_similarity_matrix',
    # Integrador
    'TextSimilarityAnalyzer',
    'analyze_abstracts'
]