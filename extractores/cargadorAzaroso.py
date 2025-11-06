import bibtexparser
import random

def extraer_articulos_aleatorios(input_bib, output_bib, cantidad=100):
    """
    Extrae una cantidad específica de artículos al azar desde un archivo .bib
    y los guarda en un nuevo archivo .bib.

    :param input_bib: Ruta al archivo .bib de entrada
    :param output_bib: Ruta al archivo .bib de salida
    :param cantidad: Número de artículos a extraer
    """
    # Cargar archivo .bib
    with open(input_bib, 'r', encoding='utf-8') as bib_file:
        bib_database = bibtexparser.load(bib_file)

    total_articulos = len(bib_database.entries)
    if cantidad > total_articulos:
        print(f"Advertencia: Solo hay {total_articulos} artículos disponibles.")
        cantidad = total_articulos

    # Seleccionar al azar
    articulos_seleccionados = random.sample(bib_database.entries, cantidad)

    # Crear nueva base de datos .bib
    nueva_base = bibtexparser.bibdatabase.BibDatabase()
    nueva_base.entries = articulos_seleccionados

    # Guardar archivo .bib
    with open(output_bib, 'w', encoding='utf-8') as bib_file:
        bibtexparser.dump(nueva_base, bib_file)

    print(f"{cantidad} artículos aleatorios guardados en: {output_bib}")

def mainAzaroso():
    input_bib = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unified_cleaned.bib"         # Cambia a tu archivo .bib
    output_bib = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unifed_reducido.bib" # Archivo de salida

    extraer_articulos_aleatorios(input_bib, output_bib, cantidad=100)

if __name__ == "__main__":
    mainAzaroso()
