import bibtexparser

ruta = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\downloads/IEE/IEEE Xplore Citation BibTeX Download 2025.9.28.19.26.33.bib"

arreglo=[]


def extraerDatosArchivo():
    with open(ruta, "r", encoding="utf-8") as bibfile:
        bib_database = bibtexparser.load(bibfile)

    # La lista de entradas se encuentra en bib_database.entries
    for entry in bib_database.entries:
        titulo = entry.get('title', '').strip()
        anio = entry.get('year', '').strip()
        arreglo.append({
            'tipo': tipo,
            'titulo': titulo,
            'año': int(anio) if anio.isdigit() else 0  # Año como entero para ordenamiento
        })

if __name__ == "__main__":
    extraerDatosArchivo()