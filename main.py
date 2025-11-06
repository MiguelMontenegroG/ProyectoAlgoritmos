import os
from extractores.ieee_extractor import scrape_IEE
from procesamiento.Requerimiento4.clutsteringDatos import mainRequerimiento4
from procesamiento.Requerimiento3.FrecuenciaPalabra import mainEjecutableRequerimiento3
from extractores.sciencedirect_extractor import science_test_debug
from procesamiento.Requerimiento5.requerimiento5Ejecutable import mainRequerimiento5
from extractores.analizador import mainAnalizador
from procesamiento.unifyBibtext import unificar  # renombrar tu función principal a unify_bibtex_main
from procesamiento.install_dependencies import install_packages
from procesamiento.Requerimiento2.instalarJupyter import mainJupyter

def ejecutar_descarga_y_unificacion():
    # 1. Descargar archivos automáticamente
    print("Descargando archivos de IEEE...")
    scrape_IEE()

    print("Descargando archivos de ScienceDirect...")
    science_test_debug()  # Descomentar si quieres activar

    # 2. Unificar y filtrar los archivos descargados
    print("Unificando y filtrando archivos...")
    unificar()  # Aquí se ejecuta todo el proceso de parseo, duplicados y guardado

    print("Proceso completado. Archivos unificados y duplicados guardados en 'output/'.")


def jupyterNotebook():
    mainJupyter()


def contarCantidadPalabrasCategoria():
    mainEjecutableRequerimiento3()


def clusterizarDatos():
    mainRequerimiento4()


def requerimiento5():
    print("Seleccione 1 si desea utilizar 100 articulos al azar del fichero unificado. Estos se cargaran al bib simplificado")
    print("Seleccione 2 si desea utilizar los articulos que ya estan cargados en el fichero simplificado")
    opcion = input("Ingrese el número de la opción que desea ejecutar: ").strip()

    if opcion == "1":
        mainAnalizador()
    elif opcion =="2":
        mainRequerimiento5()
    elif opcion=="0":
        print("Saliendo del programa...")
    else:
        print("Opción inválida. Por favor ingrese un número del 0 al 2.")

def mostrar_menu():
    install_packages()
    while True:
        print("\n--- Menú Principal ---")
        print("1. Descargar y unificar archivos")
        print("2. Funcionalidad 2")
        print("3. Mostrar palabras asociadas a la categoria. Concepts of Generative AI in Education")
        print("4. Mostrar los dendogramas ligados a los tres algoritmos de agrupamiento de clustering")
        print("5. Funcionalidad 5")
        print("0. Salir")

        opcion = input("Ingrese el número de la opción que desea ejecutar: ").strip()

        if opcion == "1":
            ejecutar_descarga_y_unificacion()
        elif opcion == "2":
            jupyterNotebook()
        elif opcion == "3":
            contarCantidadPalabrasCategoria()
        elif opcion == "4":
            clusterizarDatos()
        elif opcion == "5":
            requerimiento5()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor ingrese un número del 0 al 5.")


if __name__ == "__main__":
    mostrar_menu()
