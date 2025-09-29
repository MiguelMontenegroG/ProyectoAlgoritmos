import bibtexparser

ruta = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output/unified_cleaned.bib"

arreglo=[]


def extraerDatosArchivo():
    with open(ruta, "r", encoding="utf-8") as bibfile:
        bib_database = bibtexparser.load(bibfile)

    # La lista de entradas se encuentra en bib_database.entries
    for entry in bib_database.entries:
        titulo = entry.get('title', '').strip()
        anio = entry.get('year', '').strip()
        arreglo.append({"titulo": titulo, "año": anio})

def ordenarArreglo():
    arregloOrdenado = sorted(arreglo, key=lambda x: (x["año"], x["titulo"].lower()))
    for elemento in arregloOrdenado:
        print(elemento)

if __name__ == "__main__":
    extraerDatosArchivo()
    ordenarArreglo()