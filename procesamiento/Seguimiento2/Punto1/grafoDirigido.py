import bibtexparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import re

# === 1. Leer archivo BibTeX ===
def leer_titulos_bib(ruta_bib):
    with open(ruta_bib, encoding="utf-8") as f:
        bib_db = bibtexparser.load(f)

    titulos = []
    for entry in bib_db.entries:
        # Algunos artículos tienen el campo 'title' o 'Title'
        titulo = entry.get("title") or entry.get("Title") or ""
        # Limpiar el título de caracteres LaTeX o corchetes
        titulo = re.sub(r"[{}]", "", titulo).strip()
        if titulo:
            titulos.append(titulo)
    return titulos

# === 2. Calcular matriz de similitud ===
def calcular_similitudes(titulos):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(titulos)
    similitudes = cosine_similarity(tfidf_matrix)
    return similitudes

# === 3. Construir grafo dirigido ===
def construir_grafo(titulos, matriz_similitud, umbral=0.3):
    grafo = {}
    G = nx.DiGraph()  # también construimos el grafo con NetworkX opcionalmente

    for i, titulo_i in enumerate(titulos):
        conexiones = []
        for j, titulo_j in enumerate(titulos):
            if i != j:
                peso = matriz_similitud[i][j]
                if peso >= umbral:  # solo enlaces con similitud significativa
                    conexiones.append((titulo_j, peso))
                    G.add_edge(titulo_i, titulo_j, weight=float(peso))
        grafo[titulo_i] = conexiones

    return grafo, G

# === 4. Guardar grafo en archivo o visualizar ===
def guardar_grafo(grafo, archivo_salida="grafo_similitud.txt"):
    with open(archivo_salida, "w", encoding="utf-8") as f:
        for nodo, conexiones in grafo.items():
            f.write(f"\n🔹 {nodo}\n")
            for destino, peso in conexiones:
                f.write(f"   ➜ {destino} (peso={peso:.3f})\n")

# === 5. Ejecución ===
if __name__ == "__main__":
    RUTA_BIB = "archivo_unificado.bib"  # tu archivo combinado de IEEE + ScienceDirect

    print("📘 Extrayendo títulos...")
    titulos = leer_titulos_bib(RUTA_BIB)
    print(f"✅ Se extrajeron {len(titulos)} títulos.")

    print("🧮 Calculando similitudes...")
    matriz = calcular_similitudes(titulos)

    print("🕸️ Construyendo grafo dirigido...")
    grafo, G = construir_grafo(titulos, matriz, umbral=0.35)  # puedes ajustar el umbral

    print("💾 Guardando grafo...")
    guardar_grafo(grafo, "grafo_titulos.txt")

    print("✅ Grafo creado y guardado correctamente.")
