import pandas as pd
import os
import json
import csv
import convertidor

# mainprivadas_v1-------------------------------------
# Crea el csv
# ordena por año
# Pone un ID
# Combina 2 lineas de misma compañia y sector
# passa a  minusculas para poner todos los auto en automobilistica


# Nombre de la carpeta JSON de entrada y CSV de salida
directorio_json = 'C:/Users/Carlota/OneDrive/Escritorio/pae/carpeta_json'
archivos_json = [archivo for archivo in os.listdir(directorio_json) if archivo.endswith('.json')]

# Lista para almacenar DataFrames de los archivos CSV
dataframes = []

# Itera a través de los archivos JSON y los convierte a CSV
for archivo_json in archivos_json:
    convertidor.convertir_json_a_csv(directorio_json, archivo_json)

# Directorio que contiene los archivos CSV
directorio_csv = 'C:/Users/Carlota/OneDrive/Escritorio/pae'

# Itera a través de los archivos en el directorio
for archivo in os.listdir(directorio_csv):
    if archivo.endswith('.csv'):  # Asegúrate de que sean archivos CSV
        ruta_completa = os.path.join(directorio_csv, archivo)
        df = pd.read_csv(ruta_completa)
        dataframes.append(df)
        print(f"Metido en la database: '{archivo}'.")


# Combina los DataFrames utilizando la función concat
df_combined = pd.concat(dataframes, ignore_index=True)

# Ordenar por año de transaccion
df_combined = df_combined.sort_values(by=["Año"], ascending=False)

# Pone IDs
#df_combined = df_combined.drop(columns=["ID"])
df_combined["ID"] = range(1, len(df_combined) + 1)
# Poner la columna ID al principio
cols = df_combined.columns.tolist()
cols = cols[-1:] + cols[:-1]
df_combined = df_combined[cols]

#Si dos lineas con compañia,sector y pais son iguales con valores faltantes, los rellena con los valores de las lineas iguales
df_combined["porcent. adq."] = df_combined.groupby(["Compañia", "Sector", "Año"])["porcent. adq."].transform(lambda x: x.fillna(x.mean()))
df_combined["Precio"] = df_combined.groupby(["Compañia", "Sector", "Año"])["Precio"].transform(lambda x: x.fillna(x.mean()))
df_combined["EV"] = df_combined.groupby(["Compañia", "Sector", "Año"])["EV"].transform(lambda x: x.fillna(x.mean()))
df_combined["Ebitda"] = df_combined.groupby(["Compañia", "Sector", "Año"])["Ebitda"].transform(lambda x: x.fillna(x.mean()))

#lineas que tengan todos los valores nulos las elimina
df_combined = df_combined.dropna(how='all')

#Las lineas que sean iguales las elimina
df_combined = df_combined.drop_duplicates(subset=["Compañia","Sector","Año","Comprador","porcent. adq.","Precio","EV","Ebitda"])

# Guarda el DataFrame combinado en un nuevo archivo CSV
df_combined.to_csv("BasedatosPrivados.csv", index=False)

dbcsv = 'C:/Users/Carlota/OneDrive/Escritorio/pae/BasedatosPrivados.csv'

# Cargar el archivo CSV en un DataFrame
data = pd.read_csv(dbcsv)

data['Sector'] = data['Sector'].str.lower()
# Reemplazar los valores en la columna 'Sector'
#data['Sector'] = data['Sector'].replace(['auto parts', 'auto manufacturers'], 'automobilistica')
data.loc[data['Sector'].str.contains('auto'), 'Sector'] = 'Automobilistica'

# Guardar el DataFrame modificado en un nuevo archivo CSV
data.to_csv('BasedatosPrivados.csv', index=False)

# Imprime el DataFrame combinado
print("JUNTADO")


# mainprivadas_v2-------------------------------------
#afegirem que junti les diferents maneres d'esscriure un nom

