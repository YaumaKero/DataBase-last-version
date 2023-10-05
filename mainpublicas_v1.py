import pandas as pd
import os
import json
import csv
import convertidor

# Nombre de la carpeta JSON de entrada y CSV de salida
directorio_json = 'C:/Users/jaume/Documents/VISUAL CODES/PAE/PAE-basedatos/publicos'
archivos_json = [archivo for archivo in os.listdir(directorio_json) if archivo.endswith('.json')]

# Lista para almacenar DataFrames de los archivos CSV
dataframes = []

# Itera a través de los archivos JSON y los convierte a CSV
for archivo_json in archivos_json:
    convertidor.convertir_json_a_csv(archivo_json)

# Directorio que contiene los archivos CSV
directorio = 'C:/Users/jaume/Documents/VISUAL CODES/PAE'

# Itera a través de los archivos en el directorio
for archivo in os.listdir(directorio):
    if archivo.endswith('.csv'):  # Asegúrate de que sean archivos CSV
        ruta_completa = os.path.join(directorio, archivo)
        df = pd.read_csv(ruta_completa)
        dataframes.append(df)

# Combina los DataFrames utilizando la función concat
df_combined = pd.concat(dataframes, ignore_index=True)

# Ordenar por numero trabajadores
df_combined = df_combined.sort_values(by=["Num. trabajadores"], ascending=False)

# Elimina la columna ID y crea una nueva con valores del 1 al N
df_combined["ID"] = range(1, len(df_combined) + 1)

# Poner la columna ID al principio
cols = df_combined.columns.tolist()
cols = cols[-1:] + cols[:-1]
df_combined = df_combined[cols]

# Guarda el DataFrame combinado en un nuevo archivo CSV
df_combined.to_csv("Basedatos.csv", index=False)

# Imprime el DataFrame combinado
print("JUNTADO")
