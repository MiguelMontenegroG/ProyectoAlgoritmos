# science_extractor.py
"""
Extractor y downloader para archivos .bib de ScienceDirect (vía CRAI Referencistas).

Características:
- Accede automáticamente a ScienceDirect usando el proxy CRAI institucional
- Descarga artículos en formato BibTeX (.bib)
- Lee los .bib desde downloads/science
- Extrae/normaliza `keywords` y `country` para cada entrada
- Reescribe los archivos .bib con la información enriquecida
- Asegura exactamente dos saltos de línea entre entradas
"""

import os
import re
import time
import logging
from typing import List, Optional
import bibtexparser
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Intentar usar pycountry para detección/normalización de países (opcional)
try:
    import pycountry
    _PYCOUNTRY_AVAILABLE = True
except Exception:
    _PYCOUNTRY_AVAILABLE = False


# ============================
# CONFIGURACIÓN GENERAL
# ============================
LOGIN_URL = "https://www-sciencedirect-com.crai.referencistas.com/search?qs=computational%20thinking"
DOWNLOAD_FOLDER = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\downloads\science"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ============================
# UTILIDADES
# ============================
def ensure_two_newlines_between_entries(bib_text: str) -> str:
    """Asegura exactamente dos saltos de línea entre cada entrada @...{... }."""
    parts = re.split(r'(?=@[a-zA-Z]+\{)', bib_text)
    parts = [p.strip("\n") for p in parts if p.strip() != ""]
    joined = "\n\n".join(parts)
    if not joined.endswith("\n"):
        joined += "\n"
    return joined


def safe_text(s: Optional[str]) -> str:
    return " ".join(s.split()).strip() if s else ""


def find_country_by_name(text: str) -> Optional[str]:
    """Busca un país dentro de un texto usando pycountry."""
    if not _PYCOUNTRY_AVAILABLE or not text:
        return None
    txt = text.lower()
    for country in pycountry.countries:
        if country.name and country.name.lower() in txt:
            return country.name
        if getattr(country, "official_name", None) and country.official_name.lower() in txt:
            return country.name
    return None


def heuristic_extract_country_from_affiliation(aff_text: str) -> str:
    """Heurística simple para intentar extraer un país de la afiliación."""
    if not aff_text:
        return ""
    parts = [p.strip() for p in re.split(r'[,;|-]', aff_text) if p.strip()]
    for i in range(1, min(3, len(parts) + 1)):
        candidate = ", ".join(parts[-i:])
        if len(candidate) < 2 or re.search(r'\d|[@<>/\\|]', candidate):
            continue
        if re.search(r'\b(dept|univ|faculty|school|lab)\b', candidate, flags=re.IGNORECASE):
            continue
        if _PYCOUNTRY_AVAILABLE:
            normalized = find_country_by_name(candidate)
            if normalized:
                return normalized
        return candidate
    return ""


def normalize_keywords_field(value: str) -> str:
    """Normaliza y limpia las palabras clave."""
    if not value:
        return ""
    tokens = re.split(r'[;|\n,]+', value)
    tokens = [t.strip() for t in tokens if t.strip()]
    seen, out = set(), []
    for t in tokens:
        low = t.lower()
        if low not in seen:
            seen.add(low)
            out.append(t)
    return ", ".join(out)


# ============================
# EXTRACCIÓN DE CAMPOS
# ============================
def extract_keywords_from_entry(entry: dict) -> str:
    """Extrae las palabras clave de diferentes campos o del abstract."""
    possible = []
    for key in ["keywords", "KW", "indexterms", "index_terms", "indextermsraw", "keywords_raw", "note"]:
        if key in entry and entry[key].strip():
            possible.append(entry[key].strip())
    if not possible and "abstract" in entry and entry["abstract"]:
        m = re.search(r'(?i)keywords?:\s*(.+)', entry["abstract"])
        if m:
            possible.append(m.group(1).strip())
    for k in possible:
        norm = normalize_keywords_field(k)
        if norm:
            return norm
    return ""


def extract_country_from_entry(entry: dict) -> str:
    """Intenta deducir el país de varios campos posibles."""
    candidate_fields = ["country", "affiliation", "affiliations", "address", "note", "institution", "publisher", "location"]
    if "country" in entry and entry["country"].strip():
        return entry["country"].strip()

    combined = [entry[f].strip() for f in candidate_fields if f in entry and entry[f].strip()]

    if not combined and "author" in entry and entry["author"].strip():
        m = re.findall(r'\(([^)]+)\)', entry["author"])
        if m:
            combined.extend(m)

    text = " ".join(combined)
    if _PYCOUNTRY_AVAILABLE and text:
        byname = find_country_by_name(text)
        if byname:
            return byname

    for part in combined:
        candidate = heuristic_extract_country_from_affiliation(part)
        if candidate:
            return candidate

    return ""


def clean_and_enrich_entries(entries: List[dict]) -> List[dict]:
    """Normaliza texto, extrae keywords y país."""
    cleaned = []
    for entry in entries:
        try:
            cleaned_entry = dict(entry)
            for k, v in list(cleaned_entry.items()):
                if isinstance(v, str):
                    cleaned_entry[k] = safe_text(v)

            kws = extract_keywords_from_entry(cleaned_entry)
            if kws:
                cleaned_entry["keywords"] = kws

            country = extract_country_from_entry(cleaned_entry)
            if country:
                cleaned_entry["country"] = country

            cleaned.append(cleaned_entry)
        except Exception as e:
            logging.warning(f"Error procesando entrada: {e}")
    return cleaned


# ============================
# DESCARGA AUTOMÁTICA DESDE CRAI
# ============================
def download_sciencedirect_articles_via_crai(max_results: int = 5):
    """Accede al portal CRAI de ScienceDirect y descarga artículos en formato BibTeX."""
    logging.info(f"Conectando a ScienceDirect vía CRAI: {LOGIN_URL}")

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Muestra navegador
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            page.goto(LOGIN_URL, timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(4)

            logging.info("Página de resultados cargada correctamente.")

            # Intentar abrir menú de exportación general
            try:
                page.locator("button:has-text('Export')").first.click(timeout=5000)
                page.locator("text=BibTeX").click()
                with page.expect_download(timeout=30000) as download_info:
                    pass
                download = download_info.value
                download_path = os.path.join(DOWNLOAD_FOLDER, download.suggested_filename)
                download.save_as(download_path)
                logging.info(f"Archivo .bib descargado: {download_path}")
            except Exception as e:
                logging.warning(f"No se pudo exportar automáticamente: {e}")

        except Exception as e:
            logging.error(f"Error al acceder o descargar desde ScienceDirect CRAI: {e}")
        finally:
            context.close()
            browser.close()

    logging.info("Descarga completada.")


# ============================
# PROCESAMIENTO LOCAL DE BIBS
# ============================
def process_bib_files_in_folder(folder_path: str):
    """Carga, limpia y reescribe los archivos .bib del directorio."""
    for file in os.listdir(folder_path):
        if file.endswith(".bib"):
            full_path = os.path.join(folder_path, file)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    bib_db = bibtexparser.load(f)
                entries = bib_db.entries
                cleaned_entries = clean_and_enrich_entries(entries)
                bib_db.entries = cleaned_entries
                bib_str = bibtexparser.dumps(bib_db)
                bib_str = ensure_two_newlines_between_entries(bib_str)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(bib_str)
                logging.info(f"Procesado y actualizado: {full_path}")
            except Exception as e:
                logging.warning(f"No se pudo procesar {file}: {e}")


# ============================
# FUNCIÓN PRINCIPAL
# ============================
def mainEjecutable():
    logging.info("Iniciando descarga y procesamiento de ScienceDirect...")
    download_sciencedirect_articles_via_crai(max_results=5)
    process_bib_files_in_folder(DOWNLOAD_FOLDER)
    logging.info("Proceso finalizado correctamente.")


# ============================
# EJECUTABLE
# ============================
if __name__ == "__main__":
    mainEjecutable()
