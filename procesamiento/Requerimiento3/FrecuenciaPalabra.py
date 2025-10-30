import re
from collections import Counter

def extraer_abstracts(archivo_bib):
    """
    Extrae los abstracts de un archivo .bib y los devuelve como lista de strings.
    """
    with open(archivo_bib, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Encuentra los campos 'abstract = {...}' o 'abstract = "..."'
    patrones = re.findall(r'abstract\s*=\s*[{"](.*?)[}"],', contenido, flags=re.DOTALL | re.IGNORECASE)

    # Limpieza de saltos de línea o espacios innecesarios
    abstracts = [re.sub(r'\s+', ' ', a.strip()) for a in patrones]
    return abstracts


def contar_palabras(abstracts, palabras):
    """
    Cuenta cuántas veces aparecen ciertas palabras dentro de los abstracts.
    """
    contador = Counter()
    for abstract in abstracts:
        texto = abstract.lower()
        for palabra in palabras:
            ocurrencias = len(re.findall(rf'\b{re.escape(palabra.lower())}\b', texto))
            contador[palabra] += ocurrencias
    return contador


if __name__ == "__main__":
    ruta = r'C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unified_cleaned.bib'  # Cambia por la ruta de tu archivo .bib
    palabras_objetivo = ["Generative models","Prompting", "Machine learning", "Multimodality", "Fine-tuning", "Training data","Algorithmic bias",
                         "Explainability","Transparency","Ethics","Privacy","Personalization","Human-AI interaction","AI literacy","Co-creation"]  # Palabras que te interesan

    abstracts = extraer_abstracts(ruta)
    print(f"Se encontraron {len(abstracts)} abstracts.")

    frecuencias = contar_palabras(abstracts, palabras_objetivo)
    print("\nFrecuencia de palabras:")
    for palabra, freq in frecuencias.most_common():
        print(f"{palabra}: {freq}")
