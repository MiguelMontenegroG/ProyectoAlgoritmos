# ================================
# Requerimiento 4 - Agrupamiento jerárquico de abstracts
# ================================

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk

# Descargar recursos de NLTK (solo la primera vez)
nltk.download('stopwords')

# ========= 1. Extraer abstracts del archivo .bib ==========
def extraer_abstracts(archivo_bib):
    with open(archivo_bib, 'r', encoding='utf-8') as f:
        contenido = f.read()
    patrones = re.findall(r'abstract\s*=\s*[{"](.*?)[}"],?', contenido, flags=re.DOTALL | re.IGNORECASE)
    abstracts = [re.sub(r'\s+', ' ', a.strip()) for a in patrones]
    return abstracts


# ========= 2. Preprocesamiento del texto ==========
def limpiar_texto(texto):
    stop_words = set(stopwords.words('english'))  # o 'spanish' si tus abstracts están en español
    stemmer = SnowballStemmer('english')

    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúñü ]', ' ', texto)
    palabras = [stemmer.stem(p) for p in texto.split() if p not in stop_words]
    return ' '.join(palabras)


# ========= 3. Calcular similitud ==========
def calcular_similitud(abstracts):
    vectorizador = TfidfVectorizer()
    matriz_tfidf = vectorizador.fit_transform(abstracts)
    matriz_similitud = cosine_similarity(matriz_tfidf)
    return matriz_similitud


# ========= 4. Aplicar tres métodos de clustering jerárquico ==========
def clustering_jerarquico(similitud, metodo):
    distancia = 1 - similitud  # Convertimos similitud en distancia
    Z = linkage(distancia, method=metodo)
    return Z


# ========= 5. Representar dendrograma ==========
def mostrar_dendrograma(Z, abstracts, metodo):
    plt.figure(figsize=(10, 6))
    dendrogram(Z, labels=[f"Abs {i+1}" for i in range(len(abstracts))], leaf_rotation=90)
    plt.title(f"Dendrograma - Método {metodo}")
    plt.tight_layout()
    plt.show()


# ========= 6. Ejecución principal ==========
if __name__ == "__main__":
    ruta_bib = "articulos.bib"  # cambia por la ruta de tu archivo .bib
    abstracts = extraer_abstracts(ruta_bib)

    print(f"Se encontraron {len(abstracts)} abstracts.\n")

    # Preprocesamiento
    abstracts_limpios = [limpiar_texto(a) for a in abstracts]

    # Calcular matriz de similitud
    similitud = calcular_similitud(abstracts_limpios)

    # Métodos de clustering jerárquico a comparar
    metodos = ['single', 'complete', 'average']

    for metodo in metodos:
        Z = clustering_jerarquico(similitud, metodo)
        mostrar_dendrograma(Z, abstracts, metodo)

        # (Opcional) Generar grupos automáticos
        grupos = fcluster(Z, t=3, criterion='maxclust')
        print(f"\nAgrupamiento con método '{metodo}':")
        for i, g in enumerate(grupos, 1):
            print(f"  Abstract {i} → Grupo {g}")
