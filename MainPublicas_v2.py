import pandas as pd
import os
import json
import csv
import convertidor_v1


# Ruta de la carpeta donde se encuentran los archivos CSV
ruta_carpeta = 'C:/Users/jaume/Documents/VISUAL CODES/PAE'  

# Lista todos los archivos en la carpeta
archivos_en_carpeta = os.listdir(ruta_carpeta)

# Filtra los archivos para obtener solo los archivos CSV
archivos_csv = [archivo for archivo in archivos_en_carpeta if archivo.endswith('.csv')]

# Elimina los archivos CSV
for archivo_csv in archivos_csv:
    ruta_completa_csv = os.path.join(ruta_carpeta, archivo_csv)
    os.remove(ruta_completa_csv)



# Nombre de la carpeta JSON de entrada y CSV de salida
directorio_json = 'C:/Users/jaume/Documents/VISUAL CODES/PAE/PAE-basedatos/publicos'
archivos_json = [archivo for archivo in os.listdir(directorio_json) if archivo.endswith('.json')]

# Lista para almacenar DataFrames de los archivos CSV
dataframes = []

# Itera a través de los archivos JSON y los convierte a CSV
for archivo_json in archivos_json:
    convertidor_v1.convertir_json_a_csv(archivo_json)

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

#Si dos lineas con compañia,sector y pais son iguales con valores faltantes, los rellena con los valores de las lineas iguales
df_combined["Precio acción"] = df_combined.groupby(["Compañia", "Sector", "Pais"])["Precio acción"].transform(lambda x: x.fillna(x.mean()))
df_combined["Num. acciones"] = df_combined.groupby(["Compañia", "Sector", "Pais"])["Num. acciones"].transform(lambda x: x.fillna(x.mean()))
df_combined["Ventas"] = df_combined.groupby(["Compañia", "Sector", "Pais"])["Ventas"].transform(lambda x: x.fillna(x.mean()))
df_combined["EV"] = df_combined.groupby(["Compañia", "Sector", "Pais"])["EV"].transform(lambda x: x.fillna(x.mean()))
df_combined["Ebitda"] = df_combined.groupby(["Compañia", "Sector", "Pais"])["Ebitda"].transform(lambda x: x.fillna(x.mean()))
df_combined["Num. trabajadores"] = df_combined.groupby(["Compañia", "Sector", "Pais"])["Num. trabajadores"].transform(lambda x: x.fillna(x.mean()))

#Las lineas que sean iguales las elimina
df_combined = df_combined.drop_duplicates(subset=["Compañia","Sector","Precio acción","Num. acciones","Ventas","EV","Ebitda","Pais","Num. trabajadores"])

#lineas que tengan todos los valores nulos las elimina
df_combined = df_combined.dropna(how='all')


# Guarda el DataFrame combinado en un nuevo archivo CSV
df_combined.to_csv("Basedatos.csv", index=False)

# Imprime el DataFrame combinado
print("JUNTADO")
