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
from sklearn.decomposition import TruncatedSVD

# ========= 1. Extraer abstracts del archivo .bib ==========
def extraer_abstracts(archivo_bib):
    with open(archivo_bib, 'r', encoding='utf-8') as f:
        contenido = f.read()
    patrones = re.findall(r'abstract\s*=\s*[{"](.*?)[}"],?', contenido, flags=re.DOTALL | re.IGNORECASE)
    abstracts = [re.sub(r'\s+', ' ', a.strip()) for a in patrones]
    return abstracts


# ========= 3. Calcular similitud ==========
def calcular_similitud(abstracts):
    vectorizador = TfidfVectorizer(max_features=1000)
    matriz_tfidf = vectorizador.fit_transform(abstracts)

    # Reducir dimensionalidad
    svd = TruncatedSVD(n_components=100)
    matriz_reducida = svd.fit_transform(matriz_tfidf)

    matriz_similitud = cosine_similarity(matriz_reducida)
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

def mainRequerimiento4():
    ruta_bib = r'C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\requerimiento4.bib'  # cambia por la ruta de tu archivo .bib
    abstracts = extraer_abstracts(ruta_bib)

    print(f"Se encontraron {len(abstracts)} abstracts.\n")

    # Preprocesamiento
    # abstracts_limpios = [limpiar_texto(a) for a in abstracts]

    # Calcular matriz de similitud
    similitud = calcular_similitud(abstracts)

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


# ========= 6. Ejecución principal ==========
if __name__ == "__main__":
    mainRequerimiento4()
