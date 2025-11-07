import bibtexparser
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# === CONFIGURACIÓN ===
ARCHIVO_BIB = r'C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\seguimiento2Punto1.bib'
CARPETA_SALIDA = r'C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\procesamiento\Seguimiento2\Punto1'
UMBRAL_SIMILITUD = 0.35

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# === 1️⃣ Cargar títulos ===
def cargar_titulos(path):
    with open(path, encoding="utf-8") as f:
        bib_db = bibtexparser.load(f)
    titulos = [entry.get("title", "").strip() for entry in bib_db.entries if entry.get("title")]
    return titulos

# === 2️⃣ Calcular similitudes ===
def calcular_similitudes(titulos):
    vectorizer = TfidfVectorizer(stop_words="english")
    matriz_tfidf = vectorizer.fit_transform(titulos)
    return cosine_similarity(matriz_tfidf)

# === 3️⃣ Construir grafo dirigido ===
def construir_grafo(titulos, matriz, umbral=0.35):
    G = nx.DiGraph()
    G.add_nodes_from(range(1, len(titulos)+1))  # nodos numerados

    for i in range(len(titulos)):
        for j in range(len(titulos)):
            if i != j and matriz[i, j] >= umbral:
                G.add_edge(i+1, j+1, weight=matriz[i, j])
    return G

# === 4️⃣ Guardar descripción del grafo ===
def guardar_relaciones(G, titulos, carpeta):
    salida_txt = os.path.join(carpeta, "relaciones_grafo.txt")
    with open(salida_txt, "w", encoding="utf-8") as f:
        for nodo in G.nodes():
            titulo_origen = titulos[nodo-1]
            f.write(f"🔹 [{nodo}] {titulo_origen}\n")
            conexiones = list(G.successors(nodo))
            if not conexiones:
                f.write("   ⚪ Sin conexiones\n")
            else:
                for destino in conexiones:
                    peso = G[nodo][destino]['weight']
                    titulo_destino = titulos[destino-1]
                    f.write(f"   ➜ [{destino}] {titulo_destino} (peso={peso:.3f})\n")
            f.write("\n")
    print(f"📝 Relaciones guardadas en: {salida_txt}")

# === 5️⃣ Mostrar y guardar grafo visual ===
def mostrar_y_guardar_grafo(G):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, k=0.6, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=1000, alpha=0.9)
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15, edge_color="gray", width=1.2)
    nx.draw_networkx_labels(G, pos, labels={n: n for n in G.nodes()}, font_size=10, font_color="black")

    edge_labels = {e: f"{G.edges[e]['weight']:.2f}" for e in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    plt.title("Grafo dirigido de similitudes entre títulos (nodos numerados)", fontsize=13)
    plt.axis("off")
    plt.tight_layout()

    salida = os.path.join(CARPETA_SALIDA, "grafo_General.png")
    plt.savefig(salida, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"✅ Grafo guardado como {salida}")


# === 4️⃣ Calcular caminos mínimos con Floyd–Warshall ===
def calcular_caminos_minimos(G):
    # Convertir el grafo a matriz de adyacencia (usando pesos)
    dist = dict(nx.floyd_warshall(G, weight='weight'))
    salida = os.path.join(CARPETA_SALIDA, "caminos_minimos.txt")

    with open(salida, "w", encoding="utf-8") as f:
        f.write("Caminos mínimos entre artículos (según pesos de similitud):\n\n")
        for i in dist:
            for j in dist[i]:
                if i != j:
                    f.write(f"{i} → {j}: distancia mínima = {dist[i][j]:.4f}\n")
    print(f"✅ Caminos mínimos guardados en {salida}")


# === MÉTODO OPCIONAL: Imprimir matriz de similitud ===
def imprimir_matriz_similitud(titulos, matriz):
    import numpy as np
    np.set_printoptions(precision=3, suppress=True)

    print("\n📊 MATRIZ DE SIMILITUD ENTRE TÍTULOS:\n")

    # Encabezados numerados
    encabezado = "     " + "  ".join([f"{i + 1:>4}" for i in range(len(titulos))])
    print(encabezado)
    print("     " + "----" * len(titulos))

    # Filas con valores
    for i, fila in enumerate(matriz):
        fila_texto = "  ".join([f"{v:>4.2f}" for v in fila])
        print(f"{i + 1:>3} | {fila_texto}")

    print("\n🔹 Donde los valores cercanos a 1 indican mayor similitud.\n")

def ejecutarGrafoDirigido():
    titulos = cargar_titulos(ARCHIVO_BIB)
    matriz = calcular_similitudes(titulos)
    G = construir_grafo(titulos, matriz, umbral=UMBRAL_SIMILITUD)

    print(f"🔢 Se procesaron {len(titulos)} artículos.")
    guardar_relaciones(G, titulos, CARPETA_SALIDA)
    mostrar_y_guardar_grafo(G)

    print("Se muestran los caminos minimos")
    calcular_caminos_minimos(G)

    componentes = list(nx.strongly_connected_components(G))
    print(f"Se encontraron {len(componentes)} componentes fuertemente conexas.")
    for i, comp in enumerate(componentes, 1):
        print(f"Componente {i}: {sorted(comp)}")

    print("A continuacion se muestra la matriz de similitud ")
    imprimir_matriz_similitud(titulos, matriz)


# === 6️⃣ Ejecutar todo ===
if __name__ == "__main__":
    ejecutarGrafoDirigido()



