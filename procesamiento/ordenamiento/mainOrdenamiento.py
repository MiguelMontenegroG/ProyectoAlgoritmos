import time

import bibtexparser
from TimSort import ordenarPorTim

from CombSort import comb_sort
from radixSort import radixSort
from selectionSort import selection_sort

ruta = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\downloads/IEE/IEEE Xplore Citation BibTeX Download 2025.9.28.19.26.33.bib"

arreglo=[]


def extraerDatosArchivo():
    with open(ruta, "r", encoding="utf-8") as bibfile:
        bib_database = bibtexparser.load(bibfile)

    # La lista de entradas se encuentra en bib_database.entries
    for entry in bib_database.entries:
        # var=entry.get("title", "")+';'+entry.get("year", "")
        var = entry.get("year", "")
        arreglo.append(var)

        #for elemento in arreglo:

         #   print(elemento)

def imprimirTiempoEjecucionYArregllo(inicio,fin,arreglo):
    print(f"Tiempo de ejecución: {fin - inicio:.6f} segundos")
    for elemento in arreglo:
        print(elemento)


def mainOrdenamiento():
    opcion = input("Elige la opcion 1 para el TimSort"+"/n la opcion 2 para el combsort"+
                   "/n la opcion 3 para el selectionSort")
    extraerDatosArchivo()

    match opcion:
        case "1":
                inicio = time.perf_counter()
                ordenarPorTim(arreglo)
                fin=time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio,fin,arreglo)
        case "2":
                inicio = time.perf_counter()
                comb_sort(arreglo)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case "3":
                inicio = time.perf_counter()
                selection_sort(arreglo)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case "12":
                inicio = time.perf_counter()
                radixSort(arreglo)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case _:
            print("Opción no válida")


if __name__ == "__main__":
    mainOrdenamiento()
