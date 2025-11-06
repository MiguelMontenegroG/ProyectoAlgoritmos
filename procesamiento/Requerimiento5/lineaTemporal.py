import os
import bibtexparser
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
INPUT_BIB = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unified_with_metadata.bib"
OUTPUT_IMG = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\imagenes\lineaTemporal.png"

def cargar_articulos(bib_path):
    """Lee el archivo .bib y devuelve una lista de tuplas (journal, year)."""
    if not os.path.exists(bib_path):
        raise FileNotFoundError(f"No se encontró el archivo: {bib_path}")

    with open(bib_path, encoding="utf-8") as bibfile:
        bib_db = bibtexparser.load(bibfile)

    articulos = []
    for entry in bib_db.entries:
        if "journal" in entry and "year" in entry:
            try:
                year = int(entry["year"])
                journal = entry["journal"]
                articulos.append((journal, year))
            except ValueError:
                continue
    return articulos

def crear_linea_tiempo(articulos):
    """Crea y guarda la línea de tiempo con cuadrícula."""
    if not articulos:
        print("⚠️ No hay artículos para graficar.")
        return

    journals = [a[0] for a in articulos]
    years = [a[1] for a in articulos]

    journals_unicos = list(sorted(set(journals)))
    y_map = {journal: i for i, journal in enumerate(journals_unicos)}

    plt.figure(figsize=(14, max(6, len(journals_unicos)*0.5)))

    for i, (journal, year) in enumerate(articulos):
        plt.scatter(year, y_map[journal], s=100, color='skyblue')
        plt.text(year, y_map[journal]+0.1, str(i+1), fontsize=8, ha='center', va='bottom')

    plt.yticks(range(len(journals_unicos)), journals_unicos, fontsize=8)
    plt.xlabel("Año")
    plt.ylabel("Revistas")

    min_year = min(years)
    max_year = max(years)
    plt.xlim(min_year - 1, max_year + 1)

    # --- Activar cuadrícula ---
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    # Ajuste de márgenes
    plt.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.15)

    # Guardar imagen
    plt.savefig(OUTPUT_IMG, dpi=300)
    plt.show()
    print(f"✅ Línea de tiempo con cuadrícula guardada en: {OUTPUT_IMG}")

def mainLineaTemporal():
    articulos = cargar_articulos(INPUT_BIB)
    crear_linea_tiempo(articulos)

if __name__ == "__main__":
    mainLineaTemporal()

