import os
import re
import bibtexparser

INPUT_FILE = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unified_cleaned.bib"
OUTPUT_FILE = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unified_with_extra_info.bib"

def limpiar_texto_bibtex(texto):
    texto = texto.replace('\u0000', '')
    texto = texto.replace('\t', ' ')
    texto = re.sub(r'“|”', '"', texto)
    texto = re.sub(r"‘|’", "'", texto)
    return texto

def obtener_keywords(entry):
    """Detecta keywords sin importar cómo se llamen en el .bib"""
    posibles_campos = [
        "keywords", "keyword", "Keywords", "Keyword",
        "index_terms", "indexterms", "author_keywords",
        "keywords_plus", "terms", "Descriptors"
    ]

    for campo in posibles_campos:
        if campo in entry:
            raw = entry[campo].strip()
            # limpiar conectores comunes de IEEE o Elsevier
            raw = raw.replace("Index Terms—", "").replace("Index terms:", "")
            # reemplazar separadores distintos
            raw = raw.replace(";", ",").replace("|", ",")
            # eliminar dobles comas y espacios
            raw = re.sub(r",\s*,", ",", raw)
            return raw
    return ""

def extraer_info_bibtex(ruta_bib):
    with open(ruta_bib, encoding="utf-8") as f:
        contenido = limpiar_texto_bibtex(f.read())
        bib_data = bibtexparser.loads(contenido)

    info_actualizada = []
    for entry in bib_data.entries:
        titulo = entry.get('title', '').strip()
        abstract = entry.get('abstract', '').strip()
        keywords = obtener_keywords(entry)
        address = entry.get('address', '').strip() or entry.get('affiliation', '').strip()
        author_field = entry.get('author', '').split(" and ")[0] if 'author' in entry else ""

        # Extraer país del campo address o affiliation
        country = ""
        if address:
            match = re.search(r'\b([A-Z][a-z]+(?: [A-Z][a-z]+)*)$', address)
            if match:
                country = match.group(1)

        entry['first_author'] = author_field
        entry['country'] = country
        entry['keywords'] = keywords  # sobrescribe o añade unificado

        info_actualizada.append(entry)

    return info_actualizada

def guardar_bibtex(entries, output_path):
    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = entries
    with open(output_path, "w", encoding="utf-8") as f:
        bibtexparser.dump(db, f)
    print(f"✅ Archivo actualizado guardado en: {output_path}")

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print("❌ No se encontró el archivo unificado. Ejecuta primero el script de unificación.")
    else:
        print(f"📘 Procesando {INPUT_FILE}...")
        datos = extraer_info_bibtex(INPUT_FILE)
        guardar_bibtex(datos, OUTPUT_FILE)
