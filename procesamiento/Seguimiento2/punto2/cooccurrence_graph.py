"""
Módulo para construir grafos de coocurrencia de términos.
Establece relaciones entre términos que aparecen juntos en textos.
"""

import re
import networkx as nx
from collections import defaultdict, Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import string

# Descargar recursos de NLTK si es necesario
def _ensure_nltk_resources():
    """Descarga recursos necesarios de NLTK."""
    resources = [
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('corpora/stopwords', 'stopwords'),
        ('corpora/wordnet', 'wordnet'),
        ('corpora/averaged_perceptron_tagger', 'averaged_perceptron_tagger')
    ]
    
    for resource_path, resource_name in resources:
        try:
            nltk.data.find(resource_path)
        except (LookupError, Exception):
            try:
                nltk.download(resource_name, quiet=True)
            except Exception as e:
                print(f"Advertencia: No se pudo descargar {resource_name}: {e}")

# Asegurar que los recursos NLTK estén disponibles
_ensure_nltk_resources()


class CooccurrenceGraph:
    """Construye un grafo de coocurrencia de términos a partir de documentos."""
    
    def __init__(self, min_cooccurrence=1, language='english', use_lemmatization=True):
        """
        Inicializa el generador del grafo de coocurrencia.
        
        Args:
            min_cooccurrence (int): Mínimo número de coocurrencias para crear una arista
            language (str): Idioma para stopwords
            use_lemmatization (bool): Si usar lematización
        """
        self.graph = nx.Graph()
        self.min_cooccurrence = min_cooccurrence
        self.language = language
        self.use_lemmatization = use_lemmatization
        self.stop_words = set(stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer() if use_lemmatization else None
        self.cooccurrence_matrix = defaultdict(lambda: defaultdict(int))
        self.term_frequency = Counter()
        self.document_count = 0
        
    def preprocess_text(self, text):
        """
        Preprocesa un texto: lowercase, tokenización, eliminación de stopwords.
        
        Args:
            text (str): Texto a procesar
            
        Returns:
            list: Lista de tokens procesados
        """
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remover números
        text = re.sub(r'\d+', '', text)
        
        # Remover puntuación
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenizar
        tokens = word_tokenize(text)
        
        # Remover stopwords
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        # Lematizar si es necesario
        if self.use_lemmatization and self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return tokens
    
    def add_document(self, text):
        """
        Agrega un documento al grafo.
        
        Args:
            text (str): Texto del documento
        """
        tokens = self.preprocess_text(text)
        
        if not tokens:
            return
        
        self.document_count += 1
        
        # Contar frecuencia de términos
        for token in set(tokens):
            self.term_frequency[token] += 1
        
        # Registrar coocurrencias
        for i, token1 in enumerate(tokens):
            for token2 in tokens[i+1:]:
                if token1 != token2:
                    # Ordenar alfabéticamente para evitar duplicados
                    key1, key2 = (token1, token2) if token1 < token2 else (token2, token1)
                    self.cooccurrence_matrix[key1][key2] += 1
    
    def build_graph(self):
        """
        Construye el grafo a partir de la matriz de coocurrencia.
        """
        self.graph.clear()
        
        # Agregar nodos y aristas basadas en coocurrencia
        for term1, cooccurrences in self.cooccurrence_matrix.items():
            for term2, count in cooccurrences.items():
                if count >= self.min_cooccurrence:
                    # Agregar nodos si no existen
                    if term1 not in self.graph:
                        self.graph.add_node(term1, frequency=self.term_frequency[term1])
                    if term2 not in self.graph:
                        self.graph.add_node(term2, frequency=self.term_frequency[term2])
                    
                    # Agregar arista con peso igual a coocurrencia
                    self.graph.add_edge(term1, term2, weight=count)
        
        return self.graph
    
    def get_graph(self):
        """Retorna el grafo actual."""
        return self.graph
    
    def get_statistics(self):
        """
        Retorna estadísticas del grafo.
        
        Returns:
            dict: Estadísticas del grafo
        """
        if len(self.graph) == 0:
            return {
                'total_nodes': 0,
                'total_edges': 0,
                'total_documents': self.document_count,
                'density': 0
            }
        
        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'total_documents': self.document_count,
            'density': nx.density(self.graph),
            'average_degree': sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes()
        }


def build_cooccurrence_graph_from_abstracts(abstracts, min_cooccurrence=1):
    """
    Construye un grafo de coocurrencia a partir de una lista de abstracts.
    
    Args:
        abstracts (list): Lista de strings con los abstracts
        min_cooccurrence (int): Mínimo número de coocurrencias
        
    Returns:
        CooccurrenceGraph: Objeto con el grafo construido
    """
    cg = CooccurrenceGraph(min_cooccurrence=min_cooccurrence)
    
    for abstract in abstracts:
        if abstract and isinstance(abstract, str):
            cg.add_document(abstract)
    
    cg.build_graph()
    return cg