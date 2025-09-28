import os
from extractores.ieee_extractor import download_ieee
from extractores.sciencedirect_extractor import download_sciencedirect
from procesamiento.unifyBibtext import unify_bibtex_main  # renombrar tu función principal a unify_bibtex_main


def main():
    # 1. Descargar archivos automáticamente
    print("Descargando archivos de IEEE...")
    download_ieee(output_folder=os.path.join("downloads", "IEE"))

    print("Descargando archivos de ScienceDirect...")
    download_sciencedirect(output_folder=os.path.join("downloads", "science"))

    # (Si tienes extractores para SAGE, agregar aquí)

    # 2. Unificar y filtrar los archivos descargados
    print("Unificando y filtrando archivos...")
    unify_bibtex_main()  # Aquí se ejecuta todo el proceso de parseo, duplicados y guardado

    print("Proceso completado. Archivos unificados y duplicados guardados en 'output/'.")


if __name__ == "__main__":
    main()
