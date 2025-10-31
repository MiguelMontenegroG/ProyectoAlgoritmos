"""
BERT Similarity using Transformers

EXPLICACIÓN MATEMÁTICA:
BERT (Bidirectional Encoder Representations from Transformers) es un modelo de red neuronal
pre-entrenado que captura la representación contextual de palabras en vectores densos.

PROCESO:
1. Tokenización con WordPiece (similar a BPE)
2. Embedding de tokens
3. Agregación de capas BERT para obtener vector de representación
4. Cálculo de similitud de coseno entre vectores

VECTOR EMBEDDING:
- Dimensión estándar: 768 (en BERT-base)
- Se usa la salida de la capa final o promedio de capas
- Cada posición en el vector captura significado contextual

SIMILITUD DE COSENO:
    cos(u, v) = (u · v) / (||u|| × ||v||)

Donde:
- u · v: Producto punto
- ||u||, ||v||: Normas (magnitudes) de los vectores
- Resultado: [-1, 1], típicamente [0, 1] para embeddings

VENTAJAS:
- Captura contexto bidireccional
- Semánticamente rico
- Maneja homónimos y polisemia
"""

try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    import torch.nn.functional as F
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


def get_bert_embeddings(texts, model_name='bert-base-uncased', batch_size=32):
    """
    Obtiene embeddings BERT para una lista de textos
    
    Args:
        texts (list): Lista de textos
        model_name (str): Nombre del modelo de Hugging Face
        batch_size (int): Tamaño de lote para procesamiento
        
    Returns:
        dict: Diccionario con:
            - embeddings: Matriz de embeddings (n_texts, 768)
            - model_name: Nombre del modelo usado
            - embedding_dim: Dimensión del embedding
    """
    
    if not TRANSFORMERS_AVAILABLE:
        raise ImportError("transformers y torch no están instalados. Ejecuta: pip install transformers torch")
    
    # Cargar tokenizador y modelo
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name, output_hidden_states=True)
    model.eval()
    
    embeddings = []
    
    with torch.no_grad():
        for text in texts:
            # Tokenizar
            inputs = tokenizer(text, return_tensors='pt', truncation=True, 
                             max_length=512, padding=True)
            
            # Obtener salida
            outputs = model(**inputs)
            
            # Usar [CLS] token o promedio de tokens
            # [CLS] es el primer token especial que representa todo el texto
            cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze()
            
            embeddings.append(cls_embedding.cpu().numpy())
    
    return {
        'embeddings': embeddings,
        'model_name': model_name,
        'embedding_dim': embeddings[0].shape[0] if embeddings else 0
    }


def cosine_similarity_vectors(vec1, vec2):
    """
    Calcula similitud de coseno entre dos vectores
    
    Args:
        vec1 (array): Primer vector
        vec2 (array): Segundo vector
        
    Returns:
        float: Similitud de coseno [0, 1]
    """
    
    import numpy as np
    
    # Normalizar vectores
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    vec1_norm = vec1 / norm1
    vec2_norm = vec2 / norm2
    
    # Producto punto
    similarity = np.dot(vec1_norm, vec2_norm)
    
    # Asegurar que esté en [0, 1]
    return float(max(0.0, min(1.0, similarity)))


def bert_similarity(text1, text2, model_name='bert-base-uncased'):
    """
    Calcula similitud BERT entre dos textos
    
    Args:
        text1 (str): Primer texto
        text2 (str): Segundo texto
        model_name (str): Nombre del modelo BERT
        
    Returns:
        dict: Diccionario con:
            - similarity: Similitud BERT [0, 1]
            - embedding1_sample: Muestra del primer embedding (primeras 10 dimensiones)
            - embedding2_sample: Muestra del segundo embedding (primeras 10 dimensiones)
            - model_name: Modelo usado
    """
    
    if not TRANSFORMERS_AVAILABLE:
        raise ImportError("transformers y torch no están instalados")
    
    result = get_bert_embeddings([text1, text2], model_name)
    
    embedding1 = result['embeddings'][0]
    embedding2 = result['embeddings'][1]
    
    similarity = cosine_similarity_vectors(embedding1, embedding2)
    
    return {
        'similarity': similarity,
        'embedding1_sample': embedding1[:10].tolist(),
        'embedding2_sample': embedding2[:10].tolist(),
        'embedding1_dimension': len(embedding1),
        'embedding2_dimension': len(embedding2),
        'model_name': model_name,
        'distance': 1.0 - similarity
    }


def bert_similarity_detailed(text1, text2, model_name='bert-base-uncased'):
    """
    Calcula similitud BERT con explicación paso a paso
    
    Args:
        text1 (str): Primer texto
        text2 (str): Segundo texto
        model_name (str): Nombre del modelo BERT
        
    Returns:
        dict: Diccionario con detalles del cálculo
    """
    
    if not TRANSFORMERS_AVAILABLE:
        raise ImportError("transformers y torch no están instalados")
    
    result = get_bert_embeddings([text1, text2], model_name)
    
    embedding1 = result['embeddings'][0]
    embedding2 = result['embeddings'][1]
    
    import numpy as np
    
    # Paso a paso
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    
    embedding1_norm = embedding1 / norm1
    embedding2_norm = embedding2 / norm2
    
    dot_product = np.dot(embedding1_norm, embedding2_norm)
    similarity = float(max(0.0, min(1.0, dot_product)))
    
    return {
        'texto1': text1[:100] + '...' if len(text1) > 100 else text1,
        'texto2': text2[:100] + '...' if len(text2) > 100 else text2,
        'paso_1_modelo': model_name,
        'paso_2_tokenizacion': 'WordPiece (automático)',
        'paso_3_embedding_dimension': len(embedding1),
        'paso_4_embedding_texto1_norma': round(norm1, 4),
        'paso_4_embedding_texto2_norma': round(norm2, 4),
        'paso_5_normalizacion_embedding1': embedding1_norm[:5].tolist(),
        'paso_5_normalizacion_embedding2': embedding2_norm[:5].tolist(),
        'paso_6_producto_punto': round(dot_product, 4),
        'paso_7_formula': 'cos(u, v) = (u · v) / (||u|| × ||v||)',
        'resultado_similitud_bert': round(similarity, 4),
        'resultado_distancia_bert': round(1.0 - similarity, 4)
    }