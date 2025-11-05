import requests
import bibtexparser
import time
import os
from tqdm import tqdm
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
from string import punctuation

# 🔹 Configuración de rutas
INPUT_BIB = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\prueba.bib"
OUTPUT_BIB = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unified_with_metadata.bib"

# 🔹 Configuración NLP
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

TOP_N = 8  # número de keywords generadas si Crossref no tiene

# ---------------- FUNCIONES ----------------

def limpiar_texto(texto):
    """Limpia texto eliminando símbolos, URLs, etc."""
    texto = re.sub(r"http\S+|doi\S+", "", texto)
    texto = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip().lower()
    return texto

def extraer_keywords_nlp(texto):
    """Extrae palabras clave automáticamente del abstract o título."""
    if not texto:
        return None
    texto = limpiar_texto(texto)
    palabras = nltk.word_tokenize(texto, language="spanish")
    stop_words = set(stopwords.words("spanish")) | set(stopwords.words("english"))
    palabras_filtradas = [
        p for p in palabras if p not in stop_words and len(p) > 3 and p not in punctuation
    ]
    if not palabras_filtradas:
        return None
    contador = Counter(palabras_filtradas)
    comunes = [w for w, _ in contador.most_common(TOP_N)]
    return ", ".join(comunes)

def get_metadata_from_crossref(doi):
    """Obtiene keywords (subject) y país desde Crossref."""
    url = f"https://api.crossref.org/works/{doi}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None, None
        data = r.json().get("message", {})

        # 🔹 Keywords desde Crossref
        subjects = data.get("subject", [])
        keywords = ", ".join(subjects) if subjects else None

        # 🔹 Países desde afiliación
        countries = []
        for author in data.get("author", []):
            for aff in author.get("affiliation", []):
                if "country" in aff:
                    countries.append(aff["country"])
                elif "name" in aff:
                    text = aff["name"]
                    if "," in text:
                        possible_country = text.split(",")[-1].strip()
                        if len(possible_country) > 2:
                            countries.append(possible_country)
        countries = list(set(countries))
        countries_str = ", ".join(countries) if countries else None

        return keywords, countries_str
    except Exception:
        return None, None

def load_bib_entries(path):
    with open(path, encoding="utf-8") as bibfile:
        bib_db = bibtexparser.load(bibfile)
    return bib_db.entries

def save_bib_entries(entries, path):
    bib_db = bibtexparser.bibdatabase.BibDatabase()
    bib_db.entries = entries
    with open(path, "w", encoding="utf-8") as bibfile:
        bibtexparser.dump(bib_db, bibfile)

# ---------------- PROCESO PRINCIPAL ----------------

def main():
    if not os.path.exists(INPUT_BIB):
        print(f"❌ No se encontró el archivo {INPUT_BIB}")
        return

    entries = load_bib_entries(INPUT_BIB)
    print(f"📚 Total artículos a procesar: {len(entries)}")

    for entry in tqdm(entries, desc="🔍 Extrayendo metadatos"):
        doi = entry.get("doi", "").strip()
        abstract = entry.get("abstract", "")
        keywords, countries = (None, None)

        if doi:
            keywords, countries = get_metadata_from_crossref(doi)
            time.sleep(1)  # evitar sobrecarga API

        # Si Crossref no tiene keywords, generar con NLP
        if not keywords:
            keywords = extraer_keywords_nlp(abstract)

        if keywords:
            entry["keywords"] = keywords
        if countries:
            entry["affiliation_country"] = countries

    save_bib_entries(entries, OUTPUT_BIB)
    print(f"\n✅ Archivo con metadatos y keywords guardado en:\n{OUTPUT_BIB}")

if __name__ == "__main__":
    main()

