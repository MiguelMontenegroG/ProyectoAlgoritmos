import os
import re
import bibtexparser

# Directorios con archivos .bib
# Buscar primero en downloads (si existe) y luego en output (para archivos ya descargados)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
downloads_dir = os.path.join(base_dir, 'downloads')
output_dir = os.path.join(base_dir, 'output')

# Carpetas de entrada (primero downloads, luego output para archivos ya procesados)
folder_paths = [
    os.path.join(downloads_dir, 'IEE'),
    os.path.join(downloads_dir, 'science_test_debug'),
    os.path.join(downloads_dir, 'sage'),
    # También buscar archivos .bib directamente en output (para archivos ya descargados)
    output_dir
]

# Carpeta de salida
output_folder = output_dir
os.makedirs(output_folder, exist_ok=True)

output_cleaned = os.path.join(output_folder, "unified_cleaned.bib")
output_duplicates = os.path.join(output_folder, "duplicates.bib")

required_fields = {
    "article": ["title", "author", "journal", "year", "doi", "abstract", "ENTRYTYPE", "ID"],
    "inproceedings": ["title", "author", "booktitle", "year", "doi", "abstract", "ENTRYTYPE", "ID"],
    "book": ["title", "author", "publisher", "year", "isbn", "abstract", "ENTRYTYPE", "ID"],
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
    files_processed = []
    
    for folder in folder_paths:
        if not os.path.exists(folder):
            print(f"⚠️ La carpeta {folder} no existe, omitiendo...")
            continue
        
        # Si es el directorio output, solo buscar archivos que NO sean los de salida
        # para evitar procesar archivos ya unificados
        if folder == output_folder:
            skip_files = {'unified_cleaned.bib', 'duplicates.bib', 'unified_with_metadata.bib', 
                         'unifed_reducido.bib', 'requerimiento4.bib', 'requerimiento5.bib',
                         'seguimiento2Punto1.bib'}
        else:
            skip_files = set()
        
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".bib") and file not in skip_files:
                    file_path = os.path.join(root, file)
                    try:
                        entries = parse_bib_file(file_path)
                        all_entries.extend(entries)
                        files_processed.append(file_path)
                        print(f"✅ Procesado: {file} ({len(entries)} entradas)")
                    except Exception as e:
                        print(f"⚠️ Error procesando {file}: {e}")
                        continue
    
    if files_processed:
        print(f"\n📁 Archivos procesados: {len(files_processed)}")
        for f in files_processed:
            print(f"   - {os.path.basename(f)}")
    else:
        print("⚠️ No se encontraron archivos .bib para procesar.")
        print("💡 Asegúrese de que haya archivos .bib en:")
        print("   - downloads/IEE/")
        print("   - downloads/science_test_debug/")
        print("   - downloads/sage/")
        print("   - output/ (archivos no unificados)")
    
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
    """Limpia las entradas manteniendo solo los campos requeridos"""
    cleaned = []
    for entry in entries:
        etype = entry.get("ENTRYTYPE", "").lower()
        # Para tipos desconocidos, mantener campos básicos + abstract si existe
        default_fields = ["title", "author", "year", "abstract", "ENTRYTYPE", "ID"]
        fields = required_fields.get(etype, default_fields)
        
        # Siempre incluir campos básicos
        cleaned_entry = {
            "ENTRYTYPE": etype,
            "ID": entry.get("ID", ""),
        }
        
        # Agregar campos requeridos si existen en la entrada
        for field in fields:
            if field in entry and field not in ["ENTRYTYPE", "ID"]:
                cleaned_entry[field] = entry[field]
        
        # Si tiene abstract, asegurarse de incluirlo (importante para análisis de similitud)
        if "abstract" in entry:
            cleaned_entry["abstract"] = entry["abstract"]
        
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
    """Función principal de unificación que busca archivos BibTeX en múltiples ubicaciones"""
    print("=" * 80)
    print("🔄 PROCESO DE UNIFICACIÓN DE ARCHIVOS BIBTEX")
    print("=" * 80)
    print(f"📁 Buscando archivos en:")
    for folder in folder_paths:
        exists = "✅" if os.path.exists(folder) else "❌"
        print(f"   {exists} {folder}")
    print("=" * 80)
    
    all_entries = load_bibtex_files(folder_paths)
    print(f"\n📊 Total de entradas cargadas: {len(all_entries)}")

    if len(all_entries) == 0:
        print("\n⚠️ ADVERTENCIA: No se encontraron archivos .bib nuevos para procesar")
        
        # Verificar si ya existe un archivo unificado
        if os.path.exists(output_cleaned):
            file_size = os.path.getsize(output_cleaned)
            print(f"\nℹ️ INFORMACIÓN: Ya existe un archivo unificado:")
            print(f"   - {os.path.basename(output_cleaned)} ({file_size:,} bytes)")
            print(f"   - Ubicación: {output_cleaned}")
            print(f"\n💡 Si desea re-unificar archivos existentes:")
            print(f"   1. Asegúrese de tener archivos .bib en downloads/ o output/")
            print(f"   2. Los archivos deben tener extensión .bib y formato BibTeX válido")
            print(f"   3. Los archivos no deben estar en la lista de archivos ya unificados")
            return
        else:
            print("💡 Para usar esta funcionalidad:")
            print("   1. Asegúrese de tener archivos .bib en alguna de estas ubicaciones:")
            print("      - downloads/IEE/")
            print("      - downloads/science_test_debug/")
            print("      - downloads/sage/")
            print("      - output/ (archivos no unificados)")
            print("   2. O suba archivos .bib manualmente al directorio output/")
            print("   3. Los archivos deben tener extensión .bib y formato BibTeX válido")
            return

    print(f"\n🔄 Procesando {len(all_entries)} entradas...")
    unique_entries, duplicate_entries = detect_duplicates(all_entries)
    print(f"✅ Entradas únicas: {len(unique_entries)}")
    print(f"📋 Duplicados encontrados: {len(duplicate_entries)}")
    
    cleaned_entries = clean_entries(unique_entries)
    cleaned_duplicates = clean_entries(duplicate_entries)

    # Ordenar por año y título
    cleaned_entries.sort(key=lambda x: (x.get("year", ""), x.get("title", "").lower()))

    print(f"\n💾 Guardando archivos unificados...")
    save_bibtex_file(cleaned_entries, output_cleaned)
    save_bibtex_file(cleaned_duplicates, output_duplicates)
    
    print("\n" + "=" * 80)
    print("✅ PROCESO DE UNIFICACIÓN COMPLETADO")
    print("=" * 80)
    print(f"📁 Archivos generados:")
    if cleaned_entries:
        print(f"   - {os.path.basename(output_cleaned)} ({len(cleaned_entries)} entradas)")
    if cleaned_duplicates:
        print(f"   - {os.path.basename(output_duplicates)} ({len(cleaned_duplicates)} duplicados)")
    print("=" * 80)

if __name__ == "__main__":
    unificar()
