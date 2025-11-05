import os
import bibtexparser
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# --- CONFIGURACIÓN ---
INPUT_BIB = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unified_with_metadata.bib"
OUTPUT_IMG = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\imagenes\nubePalabras.png"

def cargar_palabras_clave(bib_path):
    """
    Lee el archivo .bib y devuelve una lista con todas las palabras clave de todos los artículos.
    Cada palabra será contada tantas veces como aparezca en los keywords.
    """
    if not os.path.exists(bib_path):
        raise FileNotFoundError(f"No se encontró el archivo: {bib_path}")

    with open(bib_path, encoding="utf-8") as bibfile:
        bib_db = bibtexparser.load(bibfile)

    todas_las_palabras = []
    for entry in bib_db.entries:
        if "keywords" in entry:
            # Separar por coma o punto y coma
            palabras = entry["keywords"].replace(";", ",").split(",")
            # Limpiar espacios y pasar a minúsculas
            palabras = [p.strip().lower() for p in palabras if p.strip()]
            # Agregar todas las palabras al contador (acumulativo)
            todas_las_palabras.extend(palabras)

    return todas_las_palabras

def generar_nube(palabras):
    """Genera una nube de palabras y muestra la cantidad de cada palabra."""
    if not palabras:
        print("⚠️ No se encontraron palabras clave para generar la nube.")
        return

    # Contar cuántas veces aparece cada palabra (contador acumulativo)
    frecuencias = Counter(palabras)

    # Imprimir la cantidad de cada palabra
    print("📊 Frecuencia de cada palabra:")
    for palabra, cantidad in frecuencias.most_common():
        print(f"{palabra}: {cantidad}")

    # Crear la nube de palabras usando las frecuencias exactas
    nube = WordCloud(
        width=1600,
        height=900,
        background_color="white",
        colormap="viridis",
        max_words=200
    ).generate_from_frequencies(frecuencias)

    # Mostrar y guardar
    plt.figure(figsize=(12, 8))
    plt.imshow(nube, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, dpi=300)
    plt.show()

    print(f"✅ Nube de palabras generada correctamente en: {OUTPUT_IMG}")
    print(f"📊 Total de palabras clave procesadas: {len(palabras)}")
    print(f"🔠 Palabras únicas: {len(frecuencias)}")

def main():
    print("📚 Generando nube de palabras (ponderada por frecuencia acumulada en keywords)...")
    palabras = cargar_palabras_clave(INPUT_BIB)
    generar_nube(palabras)

if __name__ == "__main__":
    main()
