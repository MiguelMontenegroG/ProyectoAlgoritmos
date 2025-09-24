# src/main.py
from similarity.edit_distance import edit_distance
from frequency.word_frequency import count_category_words
from download.unify import unify_datasets

def main():
    print("=== Proyecto Bibliometría ===")
    print("1. Unificar datos (Requerimiento 1)")
    print("2. Algoritmos de similitud (Requerimiento 2)")
    print("3. Frecuencia de palabras (Requerimiento 3)")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        unify_datasets()
    elif opcion == "2":
        texto1 = "Generative AI can be used in education..."
        texto2 = "Education benefits from generative artificial intelligence..."
        print("Distancia de edición:", edit_distance(texto1, texto2))
    elif opcion == "3":
        count_category_words("data/processed/articulos.csv")
    else:
        print("Opción inválida")

if __name__ == "__main__":
    main()
