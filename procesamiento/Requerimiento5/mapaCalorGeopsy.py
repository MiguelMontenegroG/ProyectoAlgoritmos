import os
import bibtexparser
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
import pycountry
import time

# 🔹 Configuración de rutas
INPUT_BIB = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'unified_with_metadata.bib')
OUTPUT_IMG_HEATMAP = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'imagenes', 'mapa_calorGeopsy.png')

# Crear directorio de imágenes si no existe
os.makedirs(os.path.dirname(OUTPUT_IMG_HEATMAP), exist_ok=True)

# ---------------- FUNCIONES ----------------

def es_pais_valido(nombre):
    """Verifica si el nombre corresponde a un país válido."""
    try:
        return pycountry.countries.lookup(nombre).name
    except LookupError:
        return None

def obtener_pais_geopy(nombre_institucion):
    """Intenta inferir el país usando Geopy a partir de la institución."""
    geolocator = Nominatim(user_agent="geo_bibtex")
    try:
        location = geolocator.geocode(nombre_institucion, timeout=10)
        if location and location.address:
            for country in pycountry.countries:
                if country.name in location.address:
                    return country.name
    except Exception:
        return None
    return None

def cargar_affiliations_mejorado(bib_path):
    """Extrae el primer valor de affiliation_country e intenta resolver país si es institución."""
    with open(bib_path, encoding="utf-8") as bibfile:
        bib_db = bibtexparser.load(bibfile)

    paises = []
    sin_pais = []

    for i, entry in enumerate(bib_db.entries):
        valor = None
        if "affiliation_country" in entry and entry["affiliation_country"].strip():
            primer_valor = entry["affiliation_country"].split(",")[0].strip()
            pais_valido = es_pais_valido(primer_valor)
            if pais_valido:
                valor = pais_valido
            else:
                # Intentar inferir país desde la institución
                pais_inferido = obtener_pais_geopy(primer_valor)
                if pais_inferido:
                    valor = pais_inferido

        if valor:
            paises.append(valor)
        else:
            sin_pais.append(f"Artículo {i+1}")

        # Evitar saturar Geopy
        time.sleep(1)

    return paises, sin_pais

def generar_mapa_calor(paises):
    df = pd.DataFrame({"country": paises})
    df_counts = df.groupby("country").size().reset_index(name='count')

    fig = px.choropleth(
        df_counts,
        locations="country",
        locationmode="country names",
        color="count",
        color_continuous_scale="Viridis",
        title="Mapa de calor de artículos por país"
    )
    try:
        fig.write_image(OUTPUT_IMG_HEATMAP, scale=2)
        print(f"✅ Mapa de calor guardado en: {OUTPUT_IMG_HEATMAP}")
    except Exception as e:
        print(f"❌ Error al guardar mapa de calor: {e}")
        print("💡 Intenta instalar kaleido: pip install kaleido")

def mainCalorGeopsy():
    if not os.path.exists(INPUT_BIB):
        print(f"❌ No se encontró el archivo {INPUT_BIB}")
        return

    paises, sin_pais = cargar_affiliations_mejorado(INPUT_BIB)
    if paises:
        generar_mapa_calor(paises)
    if sin_pais:
        print("\n⚠️ Artículos sin país detectado:")
        for articulo in sin_pais:
            print(articulo)

if __name__ == "__main__":
    mainCalorGeopsy()



