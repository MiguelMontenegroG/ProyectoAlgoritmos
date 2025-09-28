import os
import bibtexparser

# Configuración de carpetas
folder_paths = [
    "downloads/IEE",
    "downloads/science",
    "downloads/sage"
]

output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

output_cleaned = os.path.join(output_folder, "unified_cleaned.bib")
output_duplicates = os.path.join(output_folder, "duplicates.bib")

required_fields = {
    "article": ["title", "author", "journal", "year", "doi", "abstract"],
    "inproceedings": ["title", "author", "booktitle", "year", "doi", "abstract"],
    "book": ["title", "author", "publisher", "year", "isbn", "abstract"],
}

def load_bibtex_files(folders):
    entries = []
    for folder in folders:
        if not os.path.exists(folder):
            continue
        for file in os.listdir(folder):
            if file.endswith(".bib"):
                with open(os.path.join(folder, file), encoding="utf-8") as bibfile:
                    bib_database = bibtexparser.load(bibfile)
                    entries.extend(bib_database.entries)
    return entries

def get_identifier(entry):
    return entry.get("doi", entry.get("title", "")).strip().lower()

def detect_duplicates(entries):
    seen = {}
    duplicates = []
    for entry in entries:
        identifier = get_identifier(entry)
        if identifier in seen:
            duplicates.append(entry)
        else:
            seen[identifier] = entry
    return list(seen.values()), duplicates

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

def save_bibtex_file(entries, path):
    if entries:
        bib_db = bibtexparser.bibdatabase.BibDatabase()
        bib_db.entries = entries
        with open(path, "w", encoding="utf-8") as bibfile:
            bibtexparser.dump(bib_db, bibfile)
        print(f"Archivo guardado: {path}")

def unify_and_filter():
    all_entries = load_bibtex_files(folder_paths)
    unique, duplicates = detect_duplicates(all_entries)

    cleaned_unique = clean_entries(unique)
    cleaned_duplicates = clean_entries(duplicates)

    # Ordenar por año y luego título (opcional para seguimiento)
    cleaned_unique.sort(key=lambda x: (x.get("year", ""), x.get("title", "").lower()))

    save_bibtex_file(cleaned_unique, output_cleaned)
    save_bibtex_file(cleaned_duplicates, output_duplicates)

if __name__ == "__main__":
    unify_and_filter()
