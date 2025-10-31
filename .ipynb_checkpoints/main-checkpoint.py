import os
from extractores.ieee_extractor import scrape_IEE
from extractores.sage_extractor import scrape_sage
from extractores.sciencedirect_extractor import science_test_debug
from procesamiento.unifyBibtext import unificar  # renombrar tu función principal a unify_bibtex_main


def main():
    # 1. Descargar archivos automáticamente
    print("Descargando archivos de IEEE...")
    scrape_IEE()

    print("Descargando archivos de ScienceDirect...")
    #science_test_debug()

    # (Si tienes extractores para SAGE, agregar aquí)

    scrape_sage()

    # 2. Unificar y filtrar los archivos descargados
    print("Unificando y filtrando archivos...")
    unificar()  # Aquí se ejecuta todo el proceso de parseo, duplicados y guardado

    print("Proceso completado. Archivos unificados y duplicados guardados en 'output/'.")


if __name__ == "__main__":
    main()
