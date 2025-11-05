import os
from extractores.ieee_extractor import  mainEjecutable
#from extractores.sage_extractor import scrape_sage
from extractores.sciencedirect_extractor import mainEjecutable
from procesamiento.unifyBibtext import unificar  # renombrar tu función principal a unify_bibtex_main


def main():
    # 1. Descargar archivos automáticamente
    print("Descargando archivos de IEEE...")
    mainEjecutable()

    print("Descargando archivos de ScienceDirect...")
    mainEjecutable()

    # (Si tienes extractores para SAGE, agregar aquí)

    #scrape_sage()

    # 2. Unificar y filtrar los archivos descargados
    print("Unificando y filtrando archivos...")
    unificar()  # Aquí se ejecuta todo el proceso de parseo, duplicados y guardado

    print("Proceso completado. Archivos unificados y duplicados guardados en 'output/'.")


if __name__ == "__main__":
    main()
