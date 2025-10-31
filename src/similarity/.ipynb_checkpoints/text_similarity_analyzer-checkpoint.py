"""
Analizador integrado de similitud textual

Combina múltiples algoritmos de similitud textual:
- Clásicos: Levenshtein, Jaccard, Jaro-Winkler, Coseno-TF-IDF
- Con IA: BERT, Sentence-BERT
"""

from src.similarity.edit_distance import edit_distance
from src.similarity.jaccard_similarity import (
    jaccard_similarity, jaccard_similarity_detailed
)
from src.similarity.jaro_winkler import (
    jaro_winkler_similarity, jaro_winkler_detailed
)

# Importaciones condicionales para IA
try:
    from src.similarity.bert_similarity import bert_similarity, bert_similarity_detailed
    BERT_AVAILABLE = True
except:
    BERT_AVAILABLE = False

try:
    from src.similarity.sentence_bert_similarity import (
        sentence_bert_similarity, sentence_bert_similarity_detailed
    )
    SBERT_AVAILABLE = True
except:
    SBERT_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except:
    SKLEARN_AVAILABLE = False


class TextSimilarityAnalyzer:
    """
    Analizador completo de similitud textual
    """
    
    def __init__(self, text1, text2):
        """
        Inicializa el analizador
        
        Args:
            text1 (str): Primer texto
            text2 (str): Segundo texto
        """
        self.text1 = text1
        self.text2 = text2
        self.results = {}
        
    def compute_levenshtein(self):
        """Calcula distancia de Levenshtein"""
        distance = edit_distance(self.text1, self.text2)
        max_len = max(len(self.text1), len(self.text2))
        
        similarity = 1.0 - (distance / max_len) if max_len > 0 else 1.0
        
        self.results['levenshtein'] = {
            'distance': distance,
            'similarity': similarity,
            'max_length': max_len
        }
        
        return self.results['levenshtein']
    
    def compute_jaccard(self):
        """Calcula similitud Jaccard"""
        result = jaccard_similarity(self.text1, self.text2)
        self.results['jaccard'] = {
            'similarity': result['similarity'],
            'intersection_size': result['intersection_size'],
            'union_size': result['union_size']
        }
        return self.results['jaccard']
    
    def compute_jaro_winkler(self):
        """Calcula similitud Jaro-Winkler"""
        result = jaro_winkler_similarity(self.text1, self.text2)
        self.results['jaro_winkler'] = {
            'similarity': result['jaro_winkler'],
            'jaro': result['jaro']
        }
        return self.results['jaro_winkler']
    
    def compute_tfidf_cosine(self):
        """Calcula similitud Coseno con TF-IDF"""
        if not SKLEARN_AVAILABLE:
            return None
        
        try:
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([self.text1, self.text2])
            similarity = cosine_similarity(tfidf_matrix)[0][1]
            
            self.results['tfidf_cosine'] = {
                'similarity': float(similarity),
                'method': 'TF-IDF + Coseno'
            }
            return self.results['tfidf_cosine']
        except:
            return None
    
    def compute_bert(self, model_name='bert-base-uncased'):
        """Calcula similitud BERT"""
        if not BERT_AVAILABLE:
            return None
        
        try:
            result = bert_similarity(self.text1, self.text2, model_name)
            self.results['bert'] = {
                'similarity': result['similarity'],
                'model': model_name
            }
            return self.results['bert']
        except:
            return None
    
    def compute_sentence_bert(self, model_name='all-MiniLM-L6-v2'):
        """Calcula similitud Sentence-BERT"""
        if not SBERT_AVAILABLE:
            return None
        
        try:
            result = sentence_bert_similarity(self.text1, self.text2, model_name)
            self.results['sentence_bert'] = {
                'similarity': result['similarity'],
                'model': model_name
            }
            return self.results['sentence_bert']
        except:
            return None
    
    def compute_all(self):
        """
        Calcula todos los algoritmos disponibles
        
        Returns:
            dict: Resultados de todos los algoritmos
        """
        algorithms = [
            ('levenshtein', self.compute_levenshtein),
            ('jaccard', self.compute_jaccard),
            ('jaro_winkler', self.compute_jaro_winkler),
            ('tfidf_cosine', self.compute_tfidf_cosine),
            ('bert', self.compute_bert),
            ('sentence_bert', self.compute_sentence_bert)
        ]
        
        for name, method in algorithms:
            try:
                method()
            except Exception as e:
                print(f"Error computing {name}: {e}")
        
        return self.results
    
    def get_detailed_analysis(self, algorithm='all'):
        """
        Obtiene análisis detallado paso a paso
        
        Args:
            algorithm (str): Algoritmo a analizar ('all' para todos)
            
        Returns:
            dict: Análisis detallado
        """
        
        detailed = {}
        
        if algorithm == 'all' or algorithm == 'jaccard':
            detailed['jaccard'] = jaccard_similarity_detailed(self.text1, self.text2)
        
        if algorithm == 'all' or algorithm == 'jaro_winkler':
            detailed['jaro_winkler'] = jaro_winkler_detailed(self.text1, self.text2)
        
        if (algorithm == 'all' or algorithm == 'bert') and BERT_AVAILABLE:
            try:
                detailed['bert'] = bert_similarity_detailed(self.text1, self.text2)
            except:
                pass
        
        if (algorithm == 'all' or algorithm == 'sentence_bert') and SBERT_AVAILABLE:
            try:
                detailed['sentence_bert'] = sentence_bert_similarity_detailed(
                    self.text1, self.text2
                )
            except:
                pass
        
        return detailed
    
    def compare_all(self):
        """
        Realiza comparación visual de todos los algoritmos
        
        Returns:
            dict: Comparativa con ranking
        """
        
        self.compute_all()
        
        # Extraer similitudes (normalizar a [0, 1])
        similarities = {}
        
        if 'levenshtein' in self.results:
            similarities['Levenshtein (normalizado)'] = self.results['levenshtein']['similarity']
        
        if 'jaccard' in self.results:
            similarities['Jaccard'] = self.results['jaccard']['similarity']
        
        if 'jaro_winkler' in self.results:
            similarities['Jaro-Winkler'] = self.results['jaro_winkler']['similarity']
        
        if 'tfidf_cosine' in self.results:
            similarities['TF-IDF Coseno'] = self.results['tfidf_cosine']['similarity']
        
        if 'bert' in self.results:
            similarities['BERT'] = self.results['bert']['similarity']
        
        if 'sentence_bert' in self.results:
            similarities['Sentence-BERT'] = self.results['sentence_bert']['similarity']
        
        # Ordenar por similitud descendente
        sorted_similarities = sorted(
            similarities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'similarities': dict(sorted_similarities),
            'ranking': [name for name, _ in sorted_similarities],
            'values': [value for _, value in sorted_similarities]
        }


def analyze_abstracts(abstract1, abstract2, detailed=True):
    """
    Función de conveniencia para analizar dos abstracts
    
    Args:
        abstract1 (str): Primer abstract
        abstract2 (str): Segundo abstract
        detailed (bool): Si obtener análisis detallado
        
    Returns:
        dict: Resultados del análisis
    """
    
    analyzer = TextSimilarityAnalyzer(abstract1, abstract2)
    
    comparison = analyzer.compare_all()
    
    result = {
        'abstract1': abstract1[:200] + '...' if len(abstract1) > 200 else abstract1,
        'abstract2': abstract2[:200] + '...' if len(abstract2) > 200 else abstract2,
        'comparison': comparison
    }
    
    if detailed:
        result['detailed_analysis'] = analyzer.get_detailed_analysis()
    
    return result