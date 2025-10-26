"""
Jaccard Similarity Algorithm

EXPLICACIÓN MATEMÁTICA:
El coeficiente de Jaccard es una medida de similitud entre conjuntos definida como:

    J(A, B) = |A ∩ B| / |A ∪ B|

Donde:
- A ∩ B: Intersección (elementos comunes)
- A ∪ B: Unión (elementos totales únicos)
- J(A, B) ∈ [0, 1]

INTERPRETACIÓN:
- 0: No hay similitud (conjuntos disjuntos)
- 1: Similitud máxima (conjuntos idénticos)

PROCESO ALGORITMO:
1. Tokenizar ambos strings
2. Crear conjuntos (sets) de tokens
3. Calcular intersección (palabras comunes)
4. Calcular unión (palabras únicas totales)
5. Dividir intersección entre unión
"""

def tokenize(text):
    """
    Tokeniza el texto en palabras individuales
    
    Args:
        text (str): Texto a tokenizar
        
    Returns:
        list: Lista de tokens en minúsculas
    """
    return text.lower().split()


def jaccard_similarity(text1, text2, use_words=True, use_chars=False):
    """
    Calcula la similitud de Jaccard entre dos textos
    
    Args:
        text1 (str): Primer texto
        text2 (str): Segundo texto
        use_words (bool): Si True, usa palabras como tokens
        use_chars (bool): Si True, usa caracteres como tokens
        
    Returns:
        dict: Diccionario con:
            - similarity: Valor de similitud [0, 1]
            - intersection_size: Tamaño de la intersección
            - union_size: Tamaño de la unión
            - tokens1: Tokens del primer texto
            - tokens2: Tokens del segundo texto
            - intersection: Elementos comunes
            - union: Elementos únicos totales
    """
    
    if not text1 or not text2:
        return {
            'similarity': 0.0,
            'intersection_size': 0,
            'union_size': 0,
            'tokens1': [],
            'tokens2': [],
            'intersection': set(),
            'union': set()
        }
    
    # Seleccionar tokens según parámetros
    if use_chars:
        tokens1 = set(text1.lower())
        tokens2 = set(text2.lower())
    else:  # use_words por defecto
        tokens1 = set(tokenize(text1))
        tokens2 = set(tokenize(text2))
    
    # Calcular intersección y unión
    intersection = tokens1 & tokens2  # Elementos comunes
    union = tokens1 | tokens2  # Elementos únicos totales
    
    # Evitar división por cero
    if len(union) == 0:
        similarity = 1.0 if len(intersection) == 0 else 0.0
    else:
        similarity = len(intersection) / len(union)
    
    return {
        'similarity': similarity,
        'intersection_size': len(intersection),
        'union_size': len(union),
        'tokens1': list(tokens1),
        'tokens2': list(tokens2),
        'intersection': list(intersection),
        'union': list(union)
    }


def jaccard_distance(text1, text2, use_words=True, use_chars=False):
    """
    Calcula la distancia de Jaccard (1 - Similitud de Jaccard)
    
    Args:
        text1 (str): Primer texto
        text2 (str): Segundo texto
        use_words (bool): Si True, usa palabras como tokens
        use_chars (bool): Si True, usa caracteres como tokens
        
    Returns:
        float: Distancia de Jaccard [0, 1]
    """
    result = jaccard_similarity(text1, text2, use_words, use_chars)
    return 1.0 - result['similarity']


def jaccard_similarity_detailed(text1, text2, use_words=True):
    """
    Calcula la similitud de Jaccard con explicación paso a paso
    
    Args:
        text1 (str): Primer texto
        text2 (str): Segundo texto
        use_words (bool): Si True, usa palabras como tokens
        
    Returns:
        dict: Diccionario con detalles del cálculo
    """
    
    # Paso 1: Tokenizar
    tokens1 = set(tokenize(text1))
    tokens2 = set(tokenize(text2))
    
    # Paso 2: Calcular intersección
    intersection = tokens1 & tokens2
    
    # Paso 3: Calcular unión
    union = tokens1 | tokens2
    
    # Paso 4: Aplicar fórmula
    similarity = len(intersection) / len(union) if len(union) > 0 else 0.0
    
    return {
        'text1': text1,
        'text2': text2,
        'paso_1_tokens_texto1': sorted(list(tokens1)),
        'paso_2_tokens_texto2': sorted(list(tokens2)),
        'paso_3_interseccion': sorted(list(intersection)),
        'paso_3_interseccion_size': len(intersection),
        'paso_4_union': sorted(list(union)),
        'paso_4_union_size': len(union),
        'paso_5_formula': f'|A ∩ B| / |A ∪ B| = {len(intersection)} / {len(union)}',
        'resultado_similitud_jaccard': round(similarity, 4),
        'resultado_distancia_jaccard': round(1.0 - similarity, 4)
    }