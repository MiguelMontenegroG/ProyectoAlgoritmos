import re
import os
from collections import Counter

import bibtexparser

ruta = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'output', 'unified_cleaned.bib')

arreglo=[]


def extraerDatosArchivo():
    with open(ruta, "r", encoding="utf-8") as bibfile:
        bib_database = bibtexparser.load(bibfile)

    contador_autores = Counter()

    for entry in bib_database.entries:
        autoresExtraidos= entry.get("author", "")
        autores = [a.strip() for a in re.split(r'\s+and\s+', autoresExtraidos) if a.strip()]
        contador_autores.update(autores)

    autores_ordenados = sorted(
        contador_autores.items(),
        key=lambda x: (-x[1], x[0].lower())
    )

    top15 = autores_ordenados[:15]

    for autor, apariciones in top15:
        print(f"{autor}: {apariciones}")

def seguimiento1Punto3():
    extraerDatosArchivo()

if __name__ == "__main__":
    seguimiento1Punto3()