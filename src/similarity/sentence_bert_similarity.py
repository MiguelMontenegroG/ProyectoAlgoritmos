"""
Sentence-BERT (SBERT) Similarity

EXPLICACIÓN MATEMÁTICA:
Sentence-BERT es una especialización de BERT entrenada específicamente para
calcular similitudes semánticas entre oraciones y documentos.

VENTAJAS SOBRE BERT CLÁSICO:
1. Siamese Network Architecture:
   - Dos redes neuronales idénticas
   - Comparten pesos
   - Procesan dos textos simultáneamente
   
2. Función de similitud de triplet:
   - Minimiza distancia entre textos similares
   - Maximiza distancia entre textos disímiles
   
3. Mean Pooling:
   - Promedio de todos los tokens (no solo [CLS])
   - Captura información distribuida

MODELO ESTÁNDAR:
- all-MiniLM-L6-v2: 384 dimensiones, muy rápido
- all-mpnet-base-v2: 768 dimensiones, más preciso
- paraphrase-MiniLM-L6-v2: Optimizado para parafrasis

SIMILITUD DE COSENO NORMALIZADO:
    cos(u, v) = (u · v) / (||u|| × ||v||)
    
Resultado: [0, 1] para mean pooling normalizado
"""

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarities
    import numpy as np
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


def get_sentence_bert_model(model_name='all-MiniLM-L6-v2'):
    """
    Carga el modelo Sentence-BERT
    
    Args:
        model_name (str): Nombre del modelo
        
    Returns:
        SentenceTransformer: Modelo cargado
    """
    
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise ImportError("sentence-transformers no está instalado. Ejecuta: pip install sentence-transformers")
    
    return SentenceTransformer(model_name)


def sentence_bert_embeddings(texts, model_name='all-MiniLM-L6-v2'):
    """
    Obtiene embeddings de Sentence-BERT para una lista de textos
    
    Args:
        texts (list): Lista de textos
        model_name (str): Nombre del modelo
        
    Returns:
        dict: Diccionario con:
            - embeddings: Matriz de embeddings
            - model_name: Modelo usado
            - embedding_dim: Dimensión del embedding
    """
    
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise ImportError("sentence-transformers no está instalado")
    
    model = get_sentence_bert_model(model_name)
    embeddings = model.encode(texts, convert_to_numpy=True)
    
    return {
        'embeddings': embeddings,
        'model_name': model_name,
        'embedding_dim': embeddings.shape[1],
        'num_texts': len(texts)
    }


def sentence_bert_similarity(text1, text2, model_name='all-MiniLM-L6-v2'):
    """
    Calcula similitud Sentence-BERT entre dos textos
    
    Args:
        text1 (str): Primer texto
        text2 (str): Segundo texto
        model_name (str): Nombre del modelo SBERT
        
    Returns:
        dict: Diccionario con:
            - similarity: Similitud SBERT [0, 1]
            - embedding1: Embedding del primer texto (muestra)
            - embedding2: Embedding del segundo texto (muestra)
            - model_name: Modelo usado
    """
    
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise ImportError("sentence-transformers no está instalado")
    
    result = sentence_bert_embeddings([text1, text2], model_name)
    
    embeddings = result['embeddings']
    embedding1 = embeddings[0]
    embedding2 = embeddings[1]
    
    # Calcular similitud de coseno
    similarity = cosine_similarities([embedding1], [embedding2])[0][0]
    
    # Asegurar que esté en [0, 1]
    similarity = float(max(0.0, min(1.0, similarity)))
    
    return {
        'similarity': similarity,
        'embedding1_sample': embedding1[:10].tolist(),
        'embedding2_sample': embedding2[:10].tolist(),
        'embedding1_dimension': len(embedding1),
        'embedding2_dimension': len(embedding2),
        'model_name': model_name,
        'distance': 1.0 - similarity
    }


def sentence_bert_similarity_matrix(texts, model_name='all-MiniLM-L6-v2'):
    """
    Calcula matriz de similitud para múltiples textos
    
    Args:
        texts (list): Lista de textos
        model_name (str): Nombre del modelo
        
    Returns:
        dict: Diccionario con:
            - similarity_matrix: Matriz n×n de similitud
            - texts: Textos procesados
            - model_name: Modelo usado
    """
    
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise ImportError("sentence-transformers no está instalado")
    
    result = sentence_bert_embeddings(texts, model_name)
    embeddings = result['embeddings']
    
    # Calcular matriz de similitud
    similarity_matrix = cosine_similarities(embeddings, embeddings)
    
    return {
        'similarity_matrix': similarity_matrix,
        'texts': texts,
        'model_name': model_name,
        'embedding_dim': result['embedding_dim'],
        'num_texts': len(texts)
    }


def sentence_bert_similarity_detailed(text1, text2, model_name='all-MiniLM-L6-v2'):
    """
    Calcula similitud Sentence-BERT con explicación paso a paso
    
    Args:
        text1 (str): Primer texto
        text2 (str): Segundo texto
        model_name (str): Nombre del modelo
        
    Returns:
        dict: Diccionario con detalles del cálculo
    """
    
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise ImportError("sentence-transformers no está instalado")
    
    result = sentence_bert_embeddings([text1, text2], model_name)
    
    embeddings = result['embeddings']
    embedding1 = embeddings[0]
    embedding2 = embeddings[1]
    
    # Calcular paso a paso
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    
    embedding1_norm = embedding1 / norm1
    embedding2_norm = embedding2 / norm2
    
    dot_product = np.dot(embedding1_norm, embedding2_norm)
    similarity = float(max(0.0, min(1.0, dot_product)))
    
    # Descripción del modelo
    model_descriptions = {
        'all-MiniLM-L6-v2': 'Rápido, 384 dims, ideal para aplicaciones rápidas',
        'all-mpnet-base-v2': 'Preciso, 768 dims, mejor rendimiento semántico',
        'paraphrase-MiniLM-L6-v2': 'Optimizado para detectar parafrasis',
        'all-distilroberta-v1': 'DistilRoBERTa, balance velocidad-precisión'
    }
    
    return {
        'texto1': text1[:100] + '...' if len(text1) > 100 else text1,
        'texto2': text2[:100] + '...' if len(text2) > 100 else text2,
        'paso_1_modelo': model_name,
        'paso_1_descripcion': model_descriptions.get(model_name, 'Modelo personalizado'),
        'paso_2_arquitectura': 'Siamese Network con Mean Pooling',
        'paso_3_tokenizacion': 'AutoTokenizer (WordPiece)',
        'paso_4_embedding_dimension': len(embedding1),
        'paso_5_mean_pooling': 'Promedio de todos los tokens después de [CLS]',
        'paso_6_normalizacion_norma1': round(norm1, 4),
        'paso_6_normalizacion_norma2': round(norm2, 4),
        'paso_6_embedding1_normalizado': embedding1_norm[:5].tolist(),
        'paso_6_embedding2_normalizado': embedding2_norm[:5].tolist(),
        'paso_7_producto_punto': round(dot_product, 4),
        'paso_8_formula': 'cos(u, v) = (u · v) / (||u|| × ||v||)',
        'resultado_similitud_sbert': round(similarity, 4),
        'resultado_distancia_sbert': round(1.0 - similarity, 4)
    }