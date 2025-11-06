import os
import bibtexparser
import pandas as pd
import plotly.express as px

# 🔹 Configuración de rutas
INPUT_BIB = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\unified_with_metadata.bib"
OUTPUT_IMG_HEATMAP = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\imagenes\mapa_calor.png"

# ---------------- FUNCIONES ----------------

def cargar_affiliations(bib_path):
    """Extrae el primer valor del campo affiliation_country de cada artículo."""
    with open(bib_path, encoding="utf-8") as bibfile:
        bib_db = bibtexparser.load(bibfile)

    paises = []
    sin_pais = []
    for i, entry in enumerate(bib_db.entries):
        if "affiliation_country" in entry and entry["affiliation_country"].strip():
            primer_valor = entry["affiliation_country"].split(",")[0].strip()
            paises.append(primer_valor)
        else:
            sin_pais.append(f"Artículo {i+1}")
    return paises, sin_pais

def generar_mapa_calor(paises):
    """Genera un mapa de calor mundial basado en los países."""
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
    fig.write_image(OUTPUT_IMG_HEATMAP, scale=2)
    fig.show()
    print(f"✅ Mapa de calor guardado en: {OUTPUT_IMG_HEATMAP}")

def imprimir_articulos_sin_pais(sin_pais):
    """Imprime los artículos que no tienen afiliación de país."""
    if not sin_pais:
        print("⚠️ No hay artículos sin país.")
        return
    print("\n⚠️ Artículos sin afiliación de país:")
    for articulo in sin_pais:
        print(articulo)

def mainCalorNormal():
    if not os.path.exists(INPUT_BIB):
        print(f"❌ No se encontró el archivo {INPUT_BIB}")
        return

    paises, sin_pais = cargar_affiliations(INPUT_BIB)
    if paises:
        generar_mapa_calor(paises)
    if sin_pais:
        imprimir_articulos_sin_pais(sin_pais)

if __name__ == "__main__":
    mainCalorNormal()

