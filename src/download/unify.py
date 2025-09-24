import pandas as pd
import os

def unify_datasets():
    raw_path = "data/raw"
    output_path = "data/processed/unificado.csv"
    duplicates_path = "data/duplicates/duplicados.csv"

    # Leer todos los CSV del directorio raw
    dataframes = []
    for file in os.listdir(raw_path):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(raw_path, file))
            dataframes.append(df)

    # Concatenar
    df_all = pd.concat(dataframes, ignore_index=True)

    # Eliminar duplicados por título (puedes ajustar clave única)
    df_dup = df_all[df_all.duplicated("title", keep=False)]
    df_clean = df_all.drop_duplicates("title", keep="first")

    # Guardar
    df_clean.to_csv(output_path, index=False)
    df_dup.to_csv(duplicates_path, index=False)

    print(f"✅ Datos unificados en {output_path}")
    print(f"⚠️ Duplicados guardados en {duplicates_path}")
