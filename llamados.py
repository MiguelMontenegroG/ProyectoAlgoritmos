# Importaciones con manejo de errores para módulos opcionales
# Estos módulos requieren Selenium y solo están disponibles con requirements-full.txt
try:
    from extractores.ieee_extractor import scrape_IEE
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️ Advertencia: Selenium no está disponible. La descarga de documentos no funcionará.")
    print("💡 Para habilitar: pip install -r requirements-full.txt")

try:
    from extractores.sciencedirect_extractor import science_test_debug
except ImportError:
    science_test_debug = None
    print("⚠️ Advertencia: science_test_debug no está disponible.")

# Importaciones principales (siempre disponibles)
from procesamiento.Requerimiento4.clutsteringDatos import mainRequerimiento4
from procesamiento.Requerimiento3.FrecuenciaPalabra import mainEjecutableRequerimiento3
from procesamiento.Requerimiento2.requerimiento2Ejecutable import mainRequerimiento2
from procesamiento.Requerimiento5.requerimiento5Ejecutable import mainRequerimiento5
from extractores.analizador import mainAnalizador
from procesamiento.unifyBibtext import unificar
from procesamiento.Seguimiento1.Punto1Seguimiento.mainSeguimiento1 import mainSeguimiento1
from procesamiento.Seguimiento1.punto3Seguimiento.mainSeguimientoPunto3 import seguimiento1Punto3
from procesamiento.Seguimiento2.Punto1.grafoDirigido import ejecutarGrafoDirigido
from procesamiento.Seguimiento2.punto2.ejecutar import ejecutarEjecutar

# Jupyter es opcional
try:
    from instalarJupyter import mainJupyter
    JUPYTER_AVAILABLE = True
except ImportError:
    JUPYTER_AVAILABLE = False
    print("⚠️ Advertencia: Jupyter no está disponible.")
    print("💡 Para habilitar: pip install -r requirements-full.txt")
    def mainJupyter():
        print("❌ Jupyter Notebook no está disponible. Instale las dependencias completas.")



def ejecutar_descarga_y_unificacion():
    # Verificar si Selenium está disponible
    if not SELENIUM_AVAILABLE:
        print("❌ ERROR: Selenium no está disponible.")
        print("=" * 70)
        print("La descarga de documentos requiere Selenium y ChromeDriver.")
        print("=" * 70)
        print("💡 Para habilitar esta funcionalidad:")
        print("   1. Instale las dependencias completas:")
        print("      pip install -r requirements-full.txt")
        print("   2. Asegúrese de tener Chrome/ChromeDriver instalado")
        print("   3. Vuelva a ejecutar esta opción")
        print("=" * 70)
        input("\n⏸️  Presione Enter para continuar...")
        return

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
    try:
        scrape_IEE(max_pages=num_ieee if num_ieee > 0 else None)
    except Exception as e:
        print(f"❌ Error al descargar de IEEE: {e}")
        print("💡 Verifique que Chrome/ChromeDriver estén instalados correctamente")
        input("\n⏸️  Presione Enter para continuar...")
        return

    # Pequeña pausa para asegurar que Chrome se cierre completamente
    import time
    time.sleep(5)

    print("Descargando archivos de ScienceDirect...")
    try:
        if science_test_debug:
            science_test_debug(max_pages=num_science if num_science > 0 else None)
        else:
            print("⚠️ ScienceDirect extractor no está disponible")
    except Exception as e:
        print(f"❌ Error al descargar de ScienceDirect: {e}")
        print("💡 Posible solución: Actualizar ChromeDriver o verificar que Chrome esté actualizado")

    # 2. Unificar y filtrar los archivos descargados
    print("Unificando y filtrando archivos...")
    unificar()  # Aquí se ejecuta todo el proceso de parseo, duplicados y guardado

    print("Proceso completado. Archivos unificados y duplicados guardados en 'output/'.")


def jupyterNotebook():
    """Menú para seleccionar entre Jupyter Notebook o Análisis de Similitud Textual"""
    while True:
        print("\n" + "=" * 60)
        print("📊 HERRAMIENTAS DE ANÁLISIS".center(60))
        print("=" * 60)
        print("1️⃣  Jupyter Notebook")
        print("    ➤ Entorno interactivo completo con explicaciones detalladas\n")
        print("2️⃣  Análisis de Similitud Textual (Script)")
        print("    ➤ Análisis rápido de 6 algoritmos con interfaz simplificada\n")
        print("0️⃣  Volver al menú principal\n")
        print("-" * 60)

        opcion = input("👉 Seleccione la herramienta de análisis (0-2): ").strip()

        if opcion == "1":
            if not JUPYTER_AVAILABLE:
                print("\n❌ ERROR: Jupyter Notebook no está disponible.")
                print("=" * 60)
                print("💡 Para habilitar Jupyter Notebook:")
                print("   1. Instale las dependencias completas:")
                print("      pip install -r requirements-full.txt")
                print("   2. Vuelva a ejecutar esta opción")
                print("=" * 60)
            else:
                print("\n🔬 Iniciando Jupyter Notebook...")
                print("💡 Si no se abre automáticamente, copie la URL que aparecerá abajo")
                mainJupyter()

        elif opcion == "2":
            print("\n🎯 Iniciando Análisis de Similitud Textual...")
            try:
                similitudTextual()
            except Exception as e:
                print(f"❌ Error al ejecutar el análisis: {e}")
                print("💡 Verifique que todas las dependencias estén instaladas")

        elif opcion == "0":
            print("\n⬅️  Volviendo al menú principal...")
            break

        else:
            print("\n⚠️  Opción inválida. Por favor ingrese 0, 1 o 2.")

        # Pausa después de cada acción
        if opcion in ["1", "2"]:
            input("\n⏸️  Presione Enter para continuar...")


def contarCantidadPalabrasCategoria():
    mainEjecutableRequerimiento3()


def clusterizarDatos():
    mainRequerimiento4()

def similitudTextual():
    mainRequerimiento2()

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

        print("2️⃣  Herramientas de análisis")
        print("    ➤ Jupyter Notebook o Análisis de Similitud Textual interactivo.\n")

        print("3️⃣  Palabras asociadas a la categoría 'Generative AI in Education'")
        print("    ➤ Analiza la frecuencia y relación de conceptos dentro de la categoría.\n")

        print("4️⃣  Análisis de similitud textual")
        print("    ➤ Compara abstracts usando 6 algoritmos de similitud (4 clásicos + 2 IA).\n")

        print("5️⃣  Dendogramas de los algoritmos de clustering")
        print("    ➤ Visualiza los dendrogramas de los tres métodos de agrupamiento.\n")

        print("6️⃣  Mapas de calor, nube de palabras y línea temporal")
        print("    ➤ Genera visualizaciones avanzadas del análisis textual.\n")

        print("7️⃣  Seguimiento 1 - Punto 1")
        print("    ➤ Ejecuta el análisis correspondiente al seguimiento 1 punto 1.\n")

        print("8️⃣  Seguimiento 1 - Punto 3")
        print("    ➤ Ejecuta el análisis correspondiente al seguimiento 1 punto 3.\n")

        print("9️⃣  Seguimiento 2 - Punto 1")
        print("    ➤ Ejecuta el algoritmo relacionado al seguimiento 2 punto 1.\n")

        print("10️⃣ Seguimiento 2 - Punto 2")
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
            similitudTextual()

        elif opcion == "5":
            clusterizarDatos()

        elif opcion == "6":
            requerimiento5()

        elif opcion == "7":
            seguimiento1Punto1()

        elif opcion == "8":
            seguimiento1Punto3Llamado()

        elif opcion == "9":
            ejecutarGrafoDirigidoLLamado()

        elif opcion == "10":
            ejecutraSegue2Punto2()

        elif opcion == "0":
            print("\n👋 Saliendo del programa... ¡Hasta pronto!")
            break

        else:
            print("\n⚠️  Opción inválida. Por favor ingrese un número del 0 al 10.")

if __name__ == "__main__":
    mostrar_menu()
