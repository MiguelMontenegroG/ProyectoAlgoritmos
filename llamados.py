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
    while True:
        print("\n" + "=" * 60)
        print("📚 MENÚ PRINCIPAL - Análisis de Artículos".center(60))
        print("=" * 60)
        print("1️⃣  Utilizar 100 artículos aleatorios del fichero unificado")
        print("    ➤ Se generará un nuevo fichero simplificado con la muestra seleccionada.\n")
        print("2️⃣  Utilizar los artículos ya cargados en el fichero simplificado")
        print("    ➤ Se procesarán los datos existentes sin generar una nueva muestra.\n")
        print("0️⃣  Salir del programa\n")
        print("-" * 60)

        opcion = input("👉 Ingrese el número de la opción que desea ejecutar (0, 1 o 2): ").strip()

        if opcion == "1":
            print("\n🔄 Ejecutando analizador con muestra aleatoria...")
            mainAnalizador()

        elif opcion == "2":
            print("\n📊 Ejecutando requerimiento con datos existentes...")
            mainRequerimiento5()

        elif opcion == "0":
            print("\n👋 Saliendo del programa... ¡Hasta luego!")
            break

        else:
            print("\n⚠️  Opción inválida. Por favor ingrese un número del 0 al 2.")

def ejecutarGrafoDirigidoLLamado():
    ejecutarGrafoDirigido()

def mostrar_menu():
    while True:
        print("\n" + "=" * 70)
        print("📌 MENÚ PRINCIPAL - PROYECTO ANÁLISIS DE ARTÍCULOS".center(70))
        print("=" * 70)

        print("1️⃣  Descargar y unificar archivos")
        print("    ➤ Descarga los conjuntos de datos y genera el fichero unificado.\n")

        print("2️⃣  Mostrar los algoritmos matemáticos")
        print("    ➤ Abre un entorno Jupyter con explicaciones y ejecuciones.\n")

        print("3️⃣  Palabras asociadas a la categoría 'Generative AI in Education'")
        print("    ➤ Analiza la frecuencia y relación de conceptos dentro de la categoría.\n")

        print("4️⃣  Dendogramas de los algoritmos de clustering")
        print("    ➤ Visualiza los dendrogramas de los tres métodos de agrupamiento.\n")

        print("5️⃣  Mapas de calor, nube de palabras y línea temporal")
        print("    ➤ Genera visualizaciones avanzadas del análisis textual.\n")

        print("6️⃣  Seguimiento 1 - Punto 1")
        print("    ➤ Ejecuta el análisis correspondiente al seguimiento 1 punto 1.\n")

        print("7️⃣  Seguimiento 1 - Punto 3")
        print("    ➤ Ejecuta el análisis correspondiente al seguimiento 1 punto 3.\n")

        print("8️⃣  Seguimiento 2 - Punto 1")
        print("    ➤ Ejecuta el algoritmo relacionado al seguimiento 2 punto 1.\n")

        print("9️⃣  Seguimiento 2 - Punto 2")
        print("    ➤ Ejecuta el algoritmo relacionado al seguimiento 2 punto 2.\n")

        print("0️⃣  Salir del programa\n")
        print("-" * 70)

        opcion = input("👉 Ingrese el número de la opción que desea ejecutar: ").strip()

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

        elif opcion == "6":
            seguimiento1Punto1()

        elif opcion == "7":
            seguimiento1Punto3Llamado()

        elif opcion == "8":
            ejecutarGrafoDirigidoLLamado()

        elif opcion == "9":
            ejecutraSegue2Punto2()

        elif opcion == "0":
            print("\n👋 Saliendo del programa... ¡Hasta pronto!")
            break

        else:
            print("\n⚠️  Opción inválida. Por favor ingrese un número del 0 al 9.")

if __name__ == "__main__":
    mostrar_menu()
