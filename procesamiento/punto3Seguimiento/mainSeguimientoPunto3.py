import re
from collections import Counter

import bibtexparser

ruta = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\procesamiento/output/unified_cleaned.bib"

arreglo=[]


def extraerDatosArchivo():
    with open(ruta, "r", encoding="utf-8") as bibfile:
        bib_database = bibtexparser.load(bibfile)

    contador_autores = Counter()

    for entry in bib_database.entries:
        autores_raw = entry.get("author", "")
        # Separar respetando que BibTeX usa " and " (con espacios) como separador
        # Usamos regex para evitar problemas con mayúsculas/minúsculas o saltos de línea
        autores = [a.strip() for a in re.split(r'\s+and\s+', autores_raw) if a.strip()]
        contador_autores.update(autores)

    # Ordenar: primero por cantidad (descendente), luego por nombre (ascendente)
    autores_ordenados = sorted(
        contador_autores.items(),
        key=lambda x: (-x[1], x[0].lower())
    )

    # Tomar solo los primeros 15
    top15 = autores_ordenados[:15]

    for autor, apariciones in top15:
        print(f"{autor}: {apariciones}")

if __name__ == "__main__":
    extraerDatosArchivo()