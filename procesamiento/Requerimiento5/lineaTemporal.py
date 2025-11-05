import os
import bibtexparser
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
INPUT_BIB = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unified_with_metadata.bib"


def cargar_articulos(bib_path):
    """Lee el archivo .bib y devuelve una lista de diccionarios con journal, year y title."""
    if not os.path.exists(bib_path):
        raise FileNotFoundError(f"No se encontró el archivo: {bib_path}")

    with open(bib_path, encoding="utf-8") as bibfile:
        bib_db = bibtexparser.load(bibfile)

    articulos = []
    for entry in bib_db.entries:
        if "journal" in entry and "year" in entry and "title" in entry:
            try:
                year = int(entry["year"])
                journal = entry["journal"]
                title = entry["title"]
                articulos.append({"year": year, "journal": journal, "title": title})
            except ValueError:
                # Ignorar años no válidos
                continue
    return articulos


def crear_linea_tiempo(articulos):
    """Genera un gráfico de línea del tiempo de publicaciones por journal."""
    if not articulos:
        print("No se encontraron artículos para graficar.")
        return

    # Obtener lista única de journals para el eje Y
    journals = sorted(list({art["journal"] for art in articulos}))
    journal_to_y = {journal: idx for idx, journal in enumerate(journals)}

    # Preparar datos para graficar
    x = [art["year"] for art in articulos]
    y = [journal_to_y[art["journal"]] for art in articulos]
    labels = [art["title"] for art in articulos]

    # Crear el gráfico
    plt.figure(figsize=(14, max(6, len(journals) * 0.5)))
    plt.scatter(x, y, color='skyblue', s=100, edgecolor='black')

    # Etiquetar cada punto con el título (opcional: solo mostrar algunos si son muchos)
    for i, txt in enumerate(labels):
        plt.text(x[i], y[i] + 0.1, txt, fontsize=8, rotation=30, ha='left', va='bottom')

    # Configurar eje Y
    plt.yticks(list(journal_to_y.values()), list(journal_to_y.keys()))
    plt.xlabel("Año")
    plt.ylabel("Revista")
    plt.title("Línea del tiempo de artículos por año y revista")
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


def main():
    articulos = cargar_articulos(INPUT_BIB)
    crear_linea_tiempo(articulos)


if __name__ == "__main__":
    main()
