# science_test_debug.py
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "downloads", "science_test_debug")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(DOWNLOAD_FOLDER),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
})


def save_debug_artifacts(driver, name_prefix="debug"):
    screenshot_path = os.path.join(DOWNLOAD_FOLDER, f"{name_prefix}_screenshot.png")
    html_path = os.path.join(DOWNLOAD_FOLDER, f"{name_prefix}_html_snippet.txt")
    try:
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        print(f"⚠️ No se pudo guardar screenshot: {e}")
    try:
        html = driver.page_source
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html[:20000])  # limitado a 20k chars
        print(f"✅ Guardado snippet de HTML en: {html_path}")
    except Exception as e:
        print(f"⚠️ No se pudo guardar snippet HTML: {e}")
    return screenshot_path, html_path


def remove_common_overlays(driver):
    scripts = [
        "document.querySelectorAll('.modal, .overlay, .modal-backdrop, .cookie-banner, [role=\"dialog\"]').forEach(e=>e.remove());",
        "document.querySelectorAll('[style*=\"z-index\"]').forEach(e=>{ if(window.getComputedStyle(e).zIndex && parseInt(window.getComputedStyle(e).zIndex) > 1000) e.style.display='none'; });",
    ]
    for s in scripts:
        try:
            driver.execute_script(s)
        except Exception:
            pass


def click_element_fallbacks(driver, elem, desc="element"):
    """Intenta varias formas de clicar un elemento WebElement."""
    try:
        elem.click()
        return True, "click()"
    except Exception as e1:
        try:
            ActionChains(driver).move_to_element(elem).click().perform()
            return True, "ActionChains click"
        except Exception as e2:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                driver.execute_script("arguments[0].click();", elem)
                return True, "JS click"
            except Exception as e3:
                return False, f"failed clicks: {e1} | {e2} | {e3}"


def get_current_page_number(driver):
    """Obtiene el número de la página actual"""
    try:
        current_page_elem = driver.find_element(By.CSS_SELECTOR,
                                                ".pagination-page.current, .page-number.current, [aria-current='page']")
        return int(current_page_elem.text)
    except:
        try:
            # Buscar input de página actual
            page_input = driver.find_element(By.CSS_SELECTOR, "input[type='number'], .pagination-input")
            return int(page_input.get_attribute("value"))
        except:
            return 1


def go_to_next_page(driver):
    """Intenta navegar a la siguiente página"""
    try:
        # Intentar diferentes selectores para el botón "Next"
        next_selectors = [
            # Selector específico que encontraste
            "span.anchor-text:contains('next'), span.anchor-text:contains('Next')",
            # Otros selectores comunes
            "button[aria-label*='Next']",
            "button[aria-label*='Siguiente']",
            ".pagination-next",
            ".next-page",
            "a[aria-label*='Next']",
            "a[aria-label*='Siguiente']",
            "//span[contains(@class, 'anchor-text') and contains(text(), 'next')]",
            "//span[contains(@class, 'anchor-text') and contains(text(), 'Next')]",
            "//button[contains(text(), 'Next')]",
            "//button[contains(text(), 'Siguiente')]",
            "//a[contains(text(), 'Next')]",
            "//a[contains(text(), 'Siguiente')]"
        ]

        for selector in next_selectors:
            try:
                if selector.startswith("//"):
                    next_btn = driver.find_element(By.XPATH, selector)
                else:
                    # Para selectores CSS que usan :contains (que no es soportado nativamente)
                    if ":contains" in selector:
                        # Convertir a XPath
                        parts = selector.split(":contains")
                        if len(parts) == 2:
                            css_selector = parts[0]
                            text_content = parts[1].strip("()\"'")
                            xpath_selector = f"//{css_selector.replace('.', '*[@class and ').replace('#', '*[@id and ')}[contains(text(), '{text_content}')]"
                            next_btn = driver.find_element(By.XPATH, xpath_selector)
                        else:
                            continue
                    else:
                        next_btn = driver.find_element(By.CSS_SELECTOR, selector)

                if next_btn.is_enabled() and next_btn.is_displayed():
                    print(f"🔍 Encontrado botón siguiente con selector: {selector}")
                    ok, how = click_element_fallbacks(driver, next_btn, "next_button")
                    if ok:
                        print(f"✅ Navegando a siguiente página usando: {selector}")
                        time.sleep(5)  # Esperar a que cargue la nueva página
                        return True
                    else:
                        print(f"❌ No se pudo hacer click en el botón con selector: {selector}")
            except Exception as e:
                print(f"⚠️ Selector falló {selector}: {e}")
                continue

        print("❌ No se pudo encontrar el botón de siguiente página")
        # Guardar debug para inspeccionar
        save_debug_artifacts(driver, "next_button_not_found")
        return False
    except Exception as e:
        print(f"❌ Error al intentar navegar a siguiente página: {e}")
        return False


def download_current_page(driver):
    """Descarga los artículos de la página actual"""
    try:
        # Eliminar overlays por si tapan el botón
        remove_common_overlays(driver)
        time.sleep(1)

        # --- Seleccionar la casilla de los 25 artículos (si existe) ---
        try:
            checkbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "select-all-results"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            driver.execute_script("arguments[0].click();", checkbox)
            print("✅ Checkbox de selección clickeado.")
        except Exception as e:
            print(f"⚠️ No encontré o no pude clicar checkbox: {e}")

        time.sleep(2)

        # --- Buscar Export: varios selectores posibles ---
        export_candidates = []
        try:
            spans = driver.find_elements(By.XPATH, "//span[contains(@class,'export-all-link-text')]")
            export_candidates.extend(spans)
        except:
            pass
        try:
            spans2 = driver.find_elements(By.XPATH, "//span[contains(text(),'Export')]")
            export_candidates.extend(spans2)
        except:
            pass
        try:
            anchors = driver.find_elements(By.XPATH, "//a[contains(@class,'export') or contains(@class,'Export')]")
            export_candidates.extend(anchors)
        except:
            pass

        print(f"ℹ️ Encontrados {len(export_candidates)} candidatos para 'Export'.")

        export_clicked = False
        for idx, cand in enumerate(export_candidates):
            desc = cand.tag_name + " / " + (cand.get_attribute("class") or "")[:120]
            ok, how = click_element_fallbacks(driver, cand, desc)
            print(f"  intento {idx + 1}: {desc} -> {ok} ({how})")
            time.sleep(1)
            try:
                bib = driver.find_elements(By.XPATH, "//span[contains(text(), 'Export citation to BibTeX')]")
                if bib:
                    export_clicked = True
                    print("✅ Menú Export abierto (se detectó la opción BibTeX).")
                    break
            except:
                pass

        if not export_clicked:
            print("❌ No logré abrir el menú Export automáticamente.")
            return False

        # --- Click en Export citation to BibTeX ---
        try:
            bib_span = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Export citation to BibTeX')]"))
            )
            ok, how = click_element_fallbacks(driver, bib_span, "bibtex_span")
            print(f"📥 Intento click BibTeX -> {ok} via {how}")
            if not ok:
                raise Exception("No pude clicar BibTeX")
            print("✅ Botón 'Export citation to BibTeX' clickeado")
            time.sleep(8)  # Esperar a que se complete la descarga
            return True
        except Exception as e:
            print(f"❌ Error al clicar BibTeX: {e}")
            return False

    except Exception as e:
        print(f"❌ Error en descarga de página actual: {e}")
        return False


def science_test_debug():
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    LOGIN_URL = "https://www-sciencedirect-com.crai.referencistas.com/search?qs=computational%20thinking"

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(LOGIN_URL)
    time.sleep(5)

    try:
        # --- LOGIN ---
        google_login_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "btn-google"))
        )
        google_login_button.click()
        time.sleep(4)

        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                break

        email_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)

        password_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)

        driver.switch_to.window(main_window)
        print("✅ Login completado, procediendo a descarga de todas las páginas.")

        # Asegurarse de que la página ha cargado bien
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
        time.sleep(3)

        # Descargar múltiples páginas
        max_pages = 10  # Límite para evitar bucles infinitos
        downloaded_pages = 0

        for page_num in range(max_pages):
            current_page = get_current_page_number(driver)
            print(f"\n📄 Procesando página {current_page}...")

            # Descargar la página actual
            if download_current_page(driver):
                downloaded_pages += 1
                print(f"✅ Página {current_page} descargada exitosamente")

                # Verificar archivos descargados
                files = os.listdir(DOWNLOAD_FOLDER)
                bib_files = [f for f in files if f.endswith('.bib') or 'bibtex' in f.lower()]
                print(f"📁 Archivos BibTeX en carpeta: {len(bib_files)}")
            else:
                print(f"❌ Falló la descarga de la página {current_page}")

            # Intentar ir a la siguiente página
            if not go_to_next_page(driver):
                print("🏁 No hay más páginas o no se pudo navegar a la siguiente.")
                break

            # Pequeña pausa entre páginas
            time.sleep(3)

        print(f"\n🎉 Proceso completado. Total de páginas descargadas: {downloaded_pages}")

        # Mostrar resumen final de archivos
        final_files = os.listdir(DOWNLOAD_FOLDER)
        bib_final = [f for f in final_files if f.endswith('.bib') or 'bibtex' in f.lower()]
        print(f"📊 Total de archivos BibTeX descargados: {len(bib_final)}")

    except Exception as e:
        print(f"❌ Error inesperado en test debug: {e}")
        sshot, html = save_debug_artifacts(driver, "unexpected_error")
        print(f"📌 Guardado screenshot: {sshot} y HTML snippet: {html}")
        input("🔎 Revisa manualmente en Chrome. Cuando termines, presiona ENTER para cerrar.")
    finally:
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    science_test_debug()