from extractores.ieee_extractor import scrape_IEE
from procesamiento.Requerimiento4.clutsteringDatos import mainRequerimiento4
from procesamiento.Requerimiento3.FrecuenciaPalabra import mainEjecutableRequerimiento3
from extractores.sciencedirect_extractor import science_test_debug
from procesamiento.Requerimiento5.requerimiento5Ejecutable import mainRequerimiento5
from extractores.analizador import mainAnalizador
from procesamiento.unifyBibtext import unificar  # renombrar tu función principal a unify_bibtex_main
from instalarJupyter import mainJupyter
from procesamiento.Seguimiento1.Punto1Seguimiento.mainSeguimiento1 import mainSeguimiento1
from procesamiento.Seguimiento1.punto3Seguimiento.mainSeguimientoPunto3 import seguimiento1Punto3
from procesamiento.Seguimiento2.Punto1.grafoDirigido import ejecutarGrafoDirigido
from procesamiento.Seguimiento2.punto2.ejecutar import ejecutarEjecutar



def ejecutar_descarga_y_unificacion():
    # Preguntar cuántos descargar
    try:
        num_ieee = int(input("¿Cuántas páginas descargar de IEEE? (0 para todas): ").strip())
        if num_ieee < 0:
            num_ieee = 0
    except ValueError:
        num_ieee = 0

    try:
        num_science = int(input("¿Cuántas páginas descargar de ScienceDirect? (0 para todas): ").strip())
        if num_science < 0:
            num_science = 0
    except ValueError:
        num_science = 0

    # 1. Descargar archivos automáticamente
    print("Descargando archivos de IEEE...")
    scrape_IEE(max_pages=num_ieee if num_ieee > 0 else None)

    # Pequeña pausa para asegurar que Chrome se cierre completamente
    import time
    time.sleep(5)

    print("Descargando archivos de ScienceDirect...")
    try:
        science_test_debug(max_pages=num_science if num_science > 0 else None)  # Descomentar si quieres activar
    except Exception as e:
        print(f"❌ Error al descargar de ScienceDirect: {e}")
        print("💡 Posible solución: Actualizar ChromeDriver o verificar que Chrome esté actualizado")

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

def seguimiento1Punto1():
    mainSeguimiento1()

def seguimiento1Punto3Llamado():
    seguimiento1Punto3()

def ejecutraSegue2Punto2():
    ejecutarEjecutar()


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

def ejecutarGrafoDirigidoLLamado():
    ejecutarGrafoDirigido()

def mostrar_menu():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Descargar y unificar archivos")
        print("2. Mostrar los algoritmos matematicos")
        print("3. Mostrar palabras asociadas a la categoria. Concepts of Generative AI in Education")
        print("4. Mostrar los dendogramas ligados a los tres algoritmos de agrupamiento de clustering")
        print("5. Mapas de calor, nube de palabras y linea temporal")
        print("6. Seguimiento 1 punto 1")
        print("7. Seguimiento 1 punto 3")
        print("8. Seguimiento 2 punto 1")
        print("9. Seguimeinto 2 punto 2")
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
        elif opcion=="6":
            seguimiento1Punto1()
        elif opcion=="7":
            seguimiento1Punto3Llamado()
        elif opcion=="8":
            ejecutarGrafoDirigidoLLamado()
        elif opcion=="9":
            ejecutraSegue2Punto2()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor ingrese un número del 0 al 5.")


if __name__ == "__main__":
    mostrar_menu()
