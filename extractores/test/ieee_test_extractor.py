import os
import time
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

# Configurar carpeta de descargas
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "downloads/IEE")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Configurar Chrome
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(DOWNLOAD_FOLDER),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

def scrape_IEE():
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    LOGIN_URL = "https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText=Computational%20thinking"

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(LOGIN_URL)
    time.sleep(6)

    # ------------------ LOGIN ------------------
    try:
        google_login_button = driver.find_element(By.ID, "btn-google")
        google_login_button.click()
        time.sleep(6)

        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                break

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.RETURN)
        time.sleep(6)

        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(15)

        driver.switch_to.window(main_window)

    except Exception as e:
        print("❌ Error durante el login:", e)

    # ------------------ ACEPTAR COOKIES ------------------
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.osano-cm-accept-all"))
        )
        button.click()
        print("✅ Cookies aceptadas")
    except:
        print("⚠️ Botón de cookies no encontrado (quizás ya aceptado).")

    # ------------------ SELECCIONAR 100 ------------------
    try:
        itemsPerPage = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "dropdownPerPageLabel"))
        )
        itemsPerPage.click()
        option_100 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '100')]"))
        )
        option_100.click()
        print("✅ Seleccionaste 100 elementos por página.")
        time.sleep(5)
    except Exception as e:
        print("❌ Error al seleccionar 100:", e)

    # ------------------ SOLO PRIMERA PÁGINA ------------------
    try:
        print("📄 Procesando página 1...")

        # Seleccionar todos los resultados
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "results-actions-selectall-checkbox"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(3)

        # Botón Export
        export = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Export')]"))
        )
        export.click()
        time.sleep(3)

        # Pestaña Citations
        citations_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Citations')]"))
        )
        citations_tab.click()
        time.sleep(2)

        # BibTeX
        bibtex_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='download-bibtex']/input"))
        )
        if not bibtex_radio.is_selected():
            bibtex_radio.click()
        time.sleep(2)

        # Citation + Abstract
        add_abstract = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Citation and Abstract')]/input"))
        )
        if not add_abstract.is_selected():
            add_abstract.click()
        time.sleep(2)

        # Botón Download dentro del modal
        try:
            download_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'modal-dialog')]//button[contains(text(), 'Download')]")
                )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
            time.sleep(1)
            download_button.click()
            print("✅ Botón Download clickeado")
            time.sleep(10)
        except Exception as e:
            print("❌ Error clickeando Download:", e)
            input("👉 Revisa manualmente en Chrome y presiona ENTER para continuar...")

    except Exception as e:
        print("❌ Error en la primera página:", e)

    driver.quit()

if __name__ == "__main__":
    scrape_IEE()
