import os
import re
import bibtexparser

# Directorios con archivos .bib
folder_paths = [
    r"C:\Users\ANGEL\PycharmProjects\ProyectoAlgoritmos\downloads\IEE",
    r"C:\Users\ANGEL\PycharmProjects\ProyectoAlgoritmos\downloads\sage",
    r"C:\Users\ANGEL\PycharmProjects\ProyectoAlgoritmos\downloads\science"
]

# Carpeta de salida
output_folder = r"output"
os.makedirs(output_folder, exist_ok=True)

output_cleaned = os.path.join(output_folder, "unified_cleaned.bib")
output_duplicates = os.path.join(output_folder, "duplicates.bib")

required_fields = {
    "article": ["title", "author", "journal", "year", "doi", "abstract"],
    "inproceedings": ["title", "author", "booktitle", "year", "doi", "abstract"],
    "book": ["title", "author", "publisher", "year", "isbn", "abstract"],
}

# Regex para detectar entradas BibTeX
ENTRY_REGEX = re.compile(r"@(\w+)\s*{\s*([^,]+),(.+?)}\s*(?=@|\Z)", re.DOTALL)
FIELD_REGEX = re.compile(r"(\w+)\s*=\s*[{\"'](.+?)[}\"']", re.DOTALL)


def parse_bib_file(file_path):
    """Parsea un archivo .bib y devuelve una lista de diccionarios."""
    entries = []
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    for match in ENTRY_REGEX.finditer(content):
        entry_type, entry_id, body = match.groups()
        entry_type = entry_type.lower()
        entry = {"ENTRYTYPE": entry_type, "ID": entry_id}
        for field_match in FIELD_REGEX.finditer(body):
            key, value = field_match.groups()
            entry[key.strip().lower()] = value.strip()
        entries.append(entry)
    print(f"{os.path.basename(file_path)} -> {len(entries)} entradas parseadas")
    return entries


def load_bibtex_files(folder_paths):
    """Carga todos los archivos BibTeX de las carpetas (recursivo)."""
    all_entries = []
    for folder in folder_paths:
        if not os.path.exists(folder):
            print(f"⚠️ La carpeta {folder} no existe, omitiendo...")
            continue
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".bib"):
                    file_path = os.path.join(root, file)
                    all_entries.extend(parse_bib_file(file_path))
    return all_entries


def get_identifier(entry):
    """Extrae un identificador único basado en DOI o título."""
    return entry.get("doi", entry.get("title", "")).strip().lower()


def detect_duplicates(entries):
    seen = {}
    duplicates = []
    for entry in entries:
        identifier = get_identifier(entry)
        if identifier:
            if identifier in seen:
                duplicates.append(entry)
            else:
                seen[identifier] = entry
    unique_entries = list(seen.values())
    return unique_entries, duplicates


def clean_entries(entries):
    cleaned = []
    for entry in entries:
        etype = entry.get("ENTRYTYPE", "").lower()
        fields = required_fields.get(etype, ["title", "author", "year"])
        cleaned_entry = {k: entry[k] for k in fields if k in entry}
        cleaned_entry["ENTRYTYPE"] = etype
        cleaned_entry["ID"] = entry.get("ID", "")
        cleaned.append(cleaned_entry)
    return cleaned


def save_bibtex_file(entries, output_file):
    if entries:
        bib_db = bibtexparser.bibdatabase.BibDatabase()
        bib_db.entries = entries
        with open(output_file, "w", encoding="utf-8") as f:
            bibtexparser.dump(bib_db, f)
        print(f"Guardado en: {output_file}")
    else:
        print(f"No hay entradas para guardar en {output_file}")

def unificar():
    all_entries = load_bibtex_files(folder_paths)
    print(f"Total de entradas cargadas: {len(all_entries)}")

    unique_entries, duplicate_entries = detect_duplicates(all_entries)
    cleaned_entries = clean_entries(unique_entries)
    cleaned_duplicates = clean_entries(duplicate_entries)

    # Ordenar por año y título
    cleaned_entries.sort(key=lambda x: (x.get("year", ""), x.get("title", "").lower()))

    save_bibtex_file(cleaned_entries, output_cleaned)
    save_bibtex_file(cleaned_duplicates, output_duplicates)

if __name__ == "__main__":
    unificar()
