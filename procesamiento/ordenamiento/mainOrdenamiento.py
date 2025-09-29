import random
import time

import bibtexparser
from TimSort import ordenarPorTim

from CombSort import comb_sort
from GnomeSort import gnome_sort
from radixSort import radixSort
from selectionSort import selection_sort
from BinaryInsertion import binary_insertion_sort
from BiotonicSort import bitonic_sort
from HeapSort import heap_sort
from QuickSort import quicksort_inplace
from bucketSort import bucket_sort
from pigeonHoleSort import pigeonhole_sort


ruta = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\downloads/IEE/IEEE Xplore Citation BibTeX Download 2025.9.28.19.26.33.bib"

arreglo=[]


def extraerDatosArchivo():
    with open(ruta, "r", encoding="utf-8") as bibfile:
        bib_database = bibtexparser.load(bibfile)

    # La lista de entradas se encuentra en bib_database.entries
    for entry in bib_database.entries:
        # var=entry.get("title", "")+';'+entry.get("year", "")
        var = int(entry.get("year", ""))
        arreglo.append(var)



def imprimirTiempoEjecucionYArregllo(inicio,fin,arreglo):
    print(f"Tiempo de ejecución: {fin - inicio:.6f} segundos")
    for elemento in arreglo:
        print(elemento)

def modificarIntPorDecimales(arreglo):
    for i in range(len(arreglo)):
        decimal=round(random.uniform(0, 1), 2)
        arreglo[i] = arreglo[i] + decimal


def mainOrdenamiento():
    opcion = input(
        "Elige una opción de ordenamiento:\n"
        " 1  - TimSort\n"
        " 2  - CombSort\n"
        " 3  - SelectionSort\n"
        " 4  - (Reservado para futuro método)\n"
        " 5  - Pigeonhole Sort\n"
        " 6  - Bucket Sort (con decimales)\n"
        " 7  - QuickSort\n"
        " 8  - HeapSort\n"
        " 9  - Bitonic Sort\n"
        " 10 - Gnome Sort\n"
        " 11 - Binary Insertion Sort\n"
        " 12 - Radix Sort\n"
        "Ingresa el número de tu elección: "
    )
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
        case "2":
                inicio = time.perf_counter()
                selection_sort(arreglo)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case "5":
                inicio = time.perf_counter()
                pigeonhole_sort(arreglo)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case "6":
                inicio = time.perf_counter()
                modificarIntPorDecimales(arreglo)
                bucket_sort(arreglo)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case "7":
                inicio = time.perf_counter()
                quicksort_inplace(arreglo,0,len(arreglo)-1)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case "8":
                inicio = time.perf_counter()
                heap_sort(arreglo)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case "9":
                inicio = time.perf_counter()
                arreglobasura = [2015, 2021, 2010, 2024, 2001, 2007, 2019, 2004, 2013, 2020, 2006, 2018, 2003, 2022, 2009,
                             2011,2002,2017,2023,2008,2016,2005, 2025,2014,2000,2012,2007,2021,]
                arreglo.extend(arreglobasura)
                bitonic_sort(arreglo)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case "10":
                inicio = time.perf_counter()
                gnome_sort(arreglo)
                fin = time.perf_counter()
                imprimirTiempoEjecucionYArregllo(inicio, fin, arreglo)
        case "11":
                inicio = time.perf_counter()
                binary_insertion_sort(arreglo)
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
