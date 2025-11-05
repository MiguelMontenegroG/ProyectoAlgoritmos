# extractor_iee_playwright.py
"""
Extractor + downloader para IEEE via CRAI (Playwright).

Características principales:
- Abre la URL del CRAI para IEEE Xplore
- Intenta iniciar sesión vía Google SSO si aparece el botón
- Navega resultados, extrae keywords y afiliaciones (heurística country)
- Exporta BibTeX usando el modal de Export y guarda .bib en DOWNLOAD_FOLDER
- Inserta keywords y country en cada entrada del .bib descargado (si no existen)
- Reescribe el .bib asegurando exactamente dos saltos de línea entre entradas
- Ejecuta con navegador visible (headless=False) para facilitar debugging
"""

import os
import re
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout, Error as PlaywrightError

load_dotenv()

# ============ CONFIG =============
# Ruta fija donde quieres almacenar los archivos descargados
DOWNLOAD_FOLDER = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\downloads\IEE"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Login/starting URL (CRA I proxy)
LOGIN_URL = "https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText=Computational%20thinking"

# Timeout defaults (segundos)
SHORT_T = 5
MED_T = 15
LONG_T = 30

# ============ UTILITIES =============
def ensure_two_newlines_between_entries(bib_text: str) -> str:
    """Asegura que entre entradas haya exactamente dos saltos de línea."""
    parts = re.split(r'(?=@[a-zA-Z]+\{)', bib_text)
    parts = [p.strip("\n") for p in parts if p.strip() != ""]
    joined = "\n\n".join(parts)
    if not joined.endswith("\n"):
        joined += "\n"
    return joined

def safe_text(t: str) -> str:
    if not t:
        return ""
    return " ".join(t.split()).strip()

def heuristic_extract_country_from_affiliation(aff_text: str) -> str:
    """Heurística simple para extraer país desde la afiliación."""
    if not aff_text:
        return ""
    aff_text = aff_text.strip()
    parts = [p.strip() for p in re.split(r'[,;|-]', aff_text) if p.strip()]
    candidates = []
    if len(parts) >= 1:
        candidates.append(parts[-1])
    if len(parts) >= 2:
        candidates.append(parts[-2] + ", " + parts[-1])
    for c in candidates:
        if re.search(r"\d", c):
            continue
        if len(c) < 2:
            continue
        if re.search(r"[@<>/\\]", c):
            continue
        return c
    return ""

# ============ SELECTORS / HELPERS ============
COOKIE_SELECTORS = [
    "button.osano-cm-accept-all",
    "button#onetrust-accept-btn-handler",
    "button[aria-label='Aceptar cookies']",
    "button[aria-label='Accept cookies']",
    "button.cookie-accept",
]

MODAL_CLOSE_XPATHS = [
    "//div[contains(@class, 'modal-dialog')]//i[contains(@class,'fa-times')]",
    "//div[contains(@class, 'modal-dialog')]//button[contains(@class, 'close')]",
    "//div[contains(@class, 'modal')]//button[@aria-label='Close']",
    "//button[contains(@class, 'btn-close')]",
    "//button[contains(text(),'Close')]",
    "//button[contains(text(),'Cerrar')]"
]

NEXT_SELECTORS = [
    "a.stats-Pagination_arrow_next",
    "button.stats-Pagination_arrow_next",
    "a[aria-label='Next page']",
    "button[aria-label='Next page']",
    "//a[contains(@class,'next') or contains(text(),'Next') or contains(text(),'Siguiente')]"
]

SELECT_ALL_CHECKBOX_CANDIDATES = [
    ".results-actions-selectall-checkbox",
    "input#selectAll",
    "input[aria-label='Select all']",
]

EXPORT_BUTTON_XPATHS = [
    "//button[contains(text(), 'Export')]",
    "//button[contains(., 'Export')]",
    "//button[contains(text(), 'Export Results')]",
]

CITATIONS_TAB_XPATHS = [
    "//a[contains(text(), 'Citations')]",
    "//a[contains(., 'Citations')]",
    "//button[contains(text(), 'Citations')]"
]

BIBTEX_RADIO_XPATHS = [
    "//label[@for='download-bibtex']/input",
    "//input[@id='download-bibtex']",
    "//label[contains(., 'BibTeX')]/input"
]

CITATION_ABSTRACT_INDEX_XPATH = [
    "//label[contains(., 'Citation and Abstract and Index Terms')]/input",
    "//label[contains(., 'Citation + Abstract + Index Terms')]/input",
    "//label[contains(., 'Citation and Abstract')]/input"
]

DOWNLOAD_BUTTON_XPATHS = [
    "//div[contains(@class, 'modal-dialog')]//button[contains(text(), 'Download')]",
    "//button[contains(text(),'Download')]",
    "//button[contains(., 'Download')]"
]

ARTICLE_LINK_SELECTORS = [
    "a.doc-title-link",
    "a.result-item-title-link",
    "a[href*='/document/']",
    "h2.title a",
    ".List-results-items a[href*='/document/']",
    "//a[contains(@href,'/document/') and (contains(@class,'title') or contains(.,'Document') or contains(.,'Details'))]"
]

ARTICLE_KEYWORDS_SELECTORS = [
    "div.stats-keywords-list",
    "div#keywords-section",
    "//div[contains(@class,'keywords') or contains(.,'Index Terms') or contains(.,'Keywords')]",
]

AFFILIATION_SELECTORS = [
    "div.authors-info",
    "div.author-affiliations",
    "//div[contains(@class,'affiliation') or contains(@class,'authors')]"
]

# ============ SCRAPING / DOWNLOAD =============
def scrape_IEE_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Visible as requested
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("➡️ Abriendo URL de IEE (vía CRAI)...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        try:
            page.wait_for_load_state("networkidle", timeout=LONG_T * 1000)
        except PlaywrightTimeout:
            print("⚠️ Timeout esperando carga completa (continuando de todos modos).")

        # ---------- LOGIN (Google SSO si aparece) ----------
        try:
            if page.query_selector("#btn-google"):
                print("🔐 Botón Google SSO detectado, procediendo a iniciar sesión automáticamente...")
                page.click("#btn-google")
                time.sleep(2)
                # Switch to popup
                if len(context.pages) > 1:
                    popup = context.pages[-1]
                else:
                    popup = context.wait_for_event("page", timeout=10000)
                popup.wait_for_load_state("domcontentloaded", timeout=LONG_T * 1000)
                # Fill email
                if popup.query_selector("#identifierId"):
                    popup.fill("#identifierId", EMAIL or "")
                    popup.keyboard.press("Enter")
                    time.sleep(2)
                # Fill password (varias posibilidades)
                pwd_selectors = ["input[name='Passwd']", "input[type='password']"]
                time.sleep(3)
                for sel in pwd_selectors:
                    try:
                        if popup.query_selector(sel):
                            popup.fill(sel, PASSWORD or "")
                            popup.keyboard.press("Enter")
                            break
                    except PlaywrightError:
                        continue
                time.sleep(6)
                page.bring_to_front()
                try:
                    page.wait_for_load_state("networkidle", timeout=LONG_T * 1000)
                except PlaywrightTimeout:
                    pass
                print("✅ Intento de login completado (comprueba manualmente si hace falta).")
            else:
                print("⚠️ No se detectó botón Google; asumiendo sesión ya iniciada o login manual.")
        except Exception as e:
            print("❌ Error durante el login automático:", e)

        time.sleep(1)

        # ---------- Función para cerrar cookies/modales ----------
        def close_modals_and_cookies(local_page):
            # Cookies
            for sel in COOKIE_SELECTORS:
                try:
                    if local_page.query_selector(sel):
                        local_page.click(sel)
                        print("✅ Cookies aceptadas (selector):", sel)
                        time.sleep(0.8)
                        break
                except Exception:
                    continue
            # Cerrar modales por X / botones
            for xp in MODAL_CLOSE_XPATHS:
                try:
                    nodes = local_page.query_selector_all("xpath=" + xp) if xp.startswith("//") else local_page.query_selector_all(xp)
                    if nodes:
                        for n in nodes:
                            try:
                                n.click()
                                print("✅ Modal cerrado (xpath/selector):", xp)
                                time.sleep(0.6)
                            except Exception:
                                continue
                except Exception:
                    continue
            # Fallback ESC
            try:
                local_page.keyboard.press("Escape")
                time.sleep(0.4)
                return True
            except Exception:
                return False

        close_modals_and_cookies(page)

        # ---------- Intentar seleccionar 100 por página ----------
        try:
            if page.query_selector("#dropdownPerPageLabel"):
                page.click("#dropdownPerPageLabel")
                time.sleep(0.6)
                # seleccionar 100 si existe
                if page.query_selector("//button[contains(text(), '100')]"):
                    page.click("//button[contains(text(), '100')]")
                else:
                    try:
                        page.locator("text=100").first.click()
                    except Exception:
                        pass
                print("✅ Intento: seleccionar 100 items por página (si aplica).")
                try:
                    page.wait_for_load_state("networkidle", timeout=LONG_T * 1000)
                except PlaywrightTimeout:
                    pass
                time.sleep(1)
            else:
                print("⚠️ Control de resultados por página no encontrado (posible valor por defecto).")
        except Exception as e:
            print("❌ Error al intentar seleccionar 100:", e)

        # ---------- Iterar páginas y procesar ----------
        page_number = 1
        max_retries = 3
        processed_pages = 0

        while True:
            print(f"\n📄 Procesando página {page_number} ...")
            try:
                page.wait_for_load_state("networkidle", timeout=LONG_T * 1000)
            except PlaywrightTimeout:
                print("⚠️ Timeout esperando recursos de la página.")

            close_modals_and_cookies(page)

            # Seleccionar todo (checkbox) si es posible
            checkbox_clicked = False
            for sel in SELECT_ALL_CHECKBOX_CANDIDATES:
                try:
                    if page.query_selector(sel):
                        page.click(sel)
                        checkbox_clicked = True
                        time.sleep(0.6)
                        break
                except Exception:
                    continue
            if not checkbox_clicked:
                try:
                    if page.query_selector(".results-actions-selectall-checkbox"):
                        page.click(".results-actions-selectall-checkbox")
                        checkbox_clicked = True
                except Exception:
                    pass

            # Recopilar links a detalle de artículos en la página
            article_links = []
            for sel in ARTICLE_LINK_SELECTORS:
                try:
                    if sel.startswith("//"):
                        els = page.query_selector_all("xpath=" + sel)
                    else:
                        els = page.query_selector_all(sel)
                    for el in els:
                        try:
                            href = el.get_attribute("href")
                            if href and "/document/" in href:
                                article_links.append(href)
                        except Exception:
                            continue
                except Exception:
                    continue

            # Deduplicar manteniendo orden
            seen = set()
            article_links_ordered = []
            for l in article_links:
                if l not in seen:
                    seen.add(l)
                    article_links_ordered.append(l)

            # ---------- Extraer metadata por artículo (keywords, country) abriendo cada detalle ----------
            metadata_per_article = []
            for href in article_links_ordered:
                try:
                    detail = context.new_page()
                    detail.goto(href, wait_until="domcontentloaded", timeout=LONG_T * 1000)
                    try:
                        detail.wait_for_load_state("networkidle", timeout=10000)
                    except PlaywrightTimeout:
                        pass
                    close_modals_and_cookies(detail)

                    # Keywords
                    keywords = ""
                    for ksel in ARTICLE_KEYWORDS_SELECTORS:
                        try:
                            if ksel.startswith("//"):
                                nodes = detail.query_selector_all("xpath=" + ksel)
                            else:
                                nodes = detail.query_selector_all(ksel)
                            if nodes:
                                texts = []
                                for n in nodes:
                                    txt = safe_text(n.inner_text() or "")
                                    if txt:
                                        texts.append(txt)
                                if texts:
                                    keywords = "; ".join(texts)
                                    break
                        except Exception:
                            continue

                    if not keywords:
                        try:
                            nodes = detail.query_selector_all("xpath=//*[contains(., 'Index Terms') or contains(., 'Keywords')]/following-sibling::*[1]")
                            if nodes:
                                kw_texts = [safe_text(n.inner_text() or "") for n in nodes]
                                keywords = "; ".join([t for t in kw_texts if t])
                        except Exception:
                            pass

                    # Affiliations -> heurístico país
                    country = ""
                    try:
                        aff_texts = []
                        for a_sel in AFFILIATION_SELECTORS:
                            try:
                                if a_sel.startswith("//"):
                                    anodes = detail.query_selector_all("xpath=" + a_sel)
                                else:
                                    anodes = detail.query_selector_all(a_sel)
                                for n in anodes:
                                    t = safe_text(n.inner_text() or "")
                                    if t:
                                        aff_texts.append(t)
                            except Exception:
                                continue
                        if aff_texts:
                            country = heuristic_extract_country_from_affiliation(aff_texts[0])
                    except Exception:
                        country = ""

                    metadata_per_article.append({"keywords": keywords, "country": country})
                    time.sleep(0.4)
                    detail.close()
                except Exception as e:
                    print("⚠️ Error al abrir detalle de artículo:", href, e)
                    metadata_per_article.append({"keywords": "", "country": ""})

            # ---------- Intentar abrir modal Export y descargar BibTeX de la página ----------
            success_download = False
            retry = 0
            bib_filename = os.path.join(DOWNLOAD_FOLDER, f"iee_page_{page_number}.bib")

            while retry < max_retries and not success_download:
                try:
                    exported = False
                    # intentar distintos selectores para Export
                    for xp in EXPORT_BUTTON_XPATHS:
                        try:
                            if xp.startswith("//"):
                                node = page.query_selector("xpath=" + xp)
                            else:
                                node = page.query_selector(xp)
                            if node:
                                # intentar click robusto
                                try:
                                    node.click()
                                except Exception:
                                    try:
                                        node.evaluate("e => e.click()")
                                    except Exception:
                                        pass
                                exported = True
                                break
                        except Exception:
                            continue

                    if not exported:
                        try:
                            page.locator("button", has_text="Export").first.click(timeout=5000)
                            exported = True
                        except Exception:
                            pass

                    if not exported:
                        print("⚠️ No se encontró botón Export en esta página.")
                        break

                    # Esperar y seleccionar pestaña Citations si aparece
                    time.sleep(0.8)
                    for xp in CITATIONS_TAB_XPATHS:
                        try:
                            if xp.startswith("//"):
                                node = page.query_selector("xpath=" + xp)
                            else:
                                node = page.query_selector(xp)
                            if node:
                                try:
                                    node.click()
                                except Exception:
                                    try:
                                        node.evaluate("e => e.click()")
                                    except Exception:
                                        pass
                                time.sleep(0.6)
                                break
                        except Exception:
                            continue

                    # Seleccionar BibTeX
                    for xp in BIBTEX_RADIO_XPATHS:
                        try:
                            el = page.query_selector("xpath=" + xp) if xp.startswith("//") else page.query_selector(xp)
                            if el:
                                try:
                                    el.click()
                                except Exception:
                                    try:
                                        el.evaluate("e => e.checked = true")
                                    except Exception:
                                        pass
                                time.sleep(0.3)
                                break
                        except Exception:
                            continue

                    # Seleccionar Citation + Abstract + Index Terms si hay opción
                    for xp in CITATION_ABSTRACT_INDEX_XPATH:
                        try:
                            el = page.query_selector("xpath=" + xp) if xp.startswith("//") else page.query_selector(xp)
                            if el:
                                try:
                                    el.click()
                                except Exception:
                                    try:
                                        el.evaluate("e => e.click()")
                                    except Exception:
                                        pass
                                time.sleep(0.3)
                                break
                        except Exception:
                            continue

                    # Buscar botón Download en modal
                    download_btn = None
                    for xp in DOWNLOAD_BUTTON_XPATHS:
                        try:
                            if xp.startswith("//"):
                                if page.query_selector("xpath=" + xp):
                                    download_btn = "xpath=" + xp
                                    break
                            else:
                                if page.query_selector(xp):
                                    download_btn = xp
                                    break
                        except Exception:
                            continue

                    if not download_btn:
                        try:
                            # fallback: cualquier button con texto Download
                            page.locator("button", has_text="Download").first
                            download_btn = 'button:has-text("Download")'
                        except Exception:
                            pass

                    if not download_btn:
                        print("⚠️ No se encontró botón de descarga en el modal.")
                        break

                    # Ejecutar descarga con expect_download
                    with page.expect_download(timeout=LONG_T * 1000) as download_info:
                        try:
                            if download_btn.startswith("xpath="):
                                page.click(download_btn)
                            else:
                                page.click(download_btn)
                        except Exception:
                            # intentar evaluar click
                            try:
                                page.evaluate('(sel)=>document.querySelector(sel).click()', download_btn)
                            except Exception:
                                pass
                    download = download_info.value
                    download.save_as(bib_filename)
                    print(f"✅ Descargado BibTeX: {bib_filename}")
                    success_download = True

                except PlaywrightTimeout as e:
                    retry += 1
                    print(f"⚠️ Timeout descarga intento {retry}/{max_retries}: {e}")
                    close_modals_and_cookies(page)
                    time.sleep(2)
                except Exception as e:
                    retry += 1
                    print(f"⚠️ Error en export/descarga (intento {retry}/{max_retries}): {e}")
                    close_modals_and_cookies(page)
                    time.sleep(2)

            # ---------- Post-process: insertar keywords y country en el .bib descargado ----------
            if success_download:
                try:
                    with open(bib_filename, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except Exception as e:
                    print("⚠️ No se pudo leer el archivo descargado:", e)
                    content = ""

                if content:
                    bib_entries = re.split(r'(?=@(?:article|inproceedings|book)\{)', content, flags=re.IGNORECASE)
                    bib_entries = [b for b in bib_entries if b.strip() != ""]

                    modified_entries = []
                    for idx, entry in enumerate(bib_entries):
                        meta = metadata_per_article[idx] if idx < len(metadata_per_article) else {"keywords": "", "country": ""}
                        kws = safe_text(meta.get("keywords", "") or "")
                        country = safe_text(meta.get("country", "") or "")
                        entry_has_keywords = re.search(r'\bkeywords\s*=', entry, flags=re.IGNORECASE)
                        entry_has_country = re.search(r'\bcountry\s*=', entry, flags=re.IGNORECASE)
                        insertion = ""
                        if kws and not entry_has_keywords:
                            insertion += f"  keywords = {{{kws}}},\n"
                        if country and not entry_has_country:
                            insertion += f"  country = {{{country}}},\n"
                        if insertion:
                            entry = re.sub(r'\}\s*$', insertion + "}\n", entry, flags=re.MULTILINE)
                        else:
                            if not entry.endswith("\n"):
                                entry += "\n"
                        modified_entries.append(entry.strip("\n"))

                    new_content = "\n\n".join(modified_entries) + "\n"
                    new_content = ensure_two_newlines_between_entries(new_content)
                    with open(bib_filename, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print("✅ Post-procesado: keywords/country insertados cuando fue posible.")
                else:
                    print("⚠️ Contenido Bib vacío; se omitió post-procesado.")
            else:
                print(f"❌ No se pudo descargar la bibtex de la página {page_number}.")

            processed_pages += 1

            # ---------- Intentar ir a siguiente página ----------
            has_next = False
            for sel in NEXT_SELECTORS:
                try:
                    nxt = page.query_selector("xpath=" + sel) if sel.startswith("//") else page.query_selector(sel)
                    if not nxt:
                        continue
                    disabled_attr = nxt.get_attribute("disabled") or ""
                    class_attr = (nxt.get_attribute("class") or "").lower()
                    if "disabled" in class_attr or disabled_attr.lower() == "true":
                        has_next = False
                        continue
                    # intentar click en siguiente
                    try:
                        nxt.scroll_into_view_if_needed()
                        time.sleep(0.4)
                        nxt.click()
                        page_number += 1
                        try:
                            page.wait_for_load_state("networkidle", timeout=LONG_T * 1000)
                        except PlaywrightTimeout:
                            pass
                        time.sleep(0.8)
                        has_next = True
                    except Exception as e:
                        print("⚠️ Error haciendo click en siguiente:", e)
                        has_next = False
                    break
                except Exception:
                    continue

            if not has_next:
                print("🏁 No hay más páginas. Finalizando.")
                break

        # Cierre
        try:
            context.close()
            browser.close()
        except Exception:
            pass

        print(f"📊 Proceso terminado. Páginas procesadas: {processed_pages}")

def mainEjecutable():
    scrape_IEE_playwright()

if __name__ == "__main__":
    mainEjecutable()

