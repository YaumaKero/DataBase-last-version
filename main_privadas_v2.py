import pandas as pd
import os
import json
import csv
import convertidor

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

        # Reemplazar valores vacíos o nulos en la columna "Percent. acq." con "100%"
        df["Percent. acq."] = df["Percent. acq."].fillna("100%")

        # Convertir la columna "Year" a enteros
        df["Year"] = df["Year"].fillna(1)
        df["Year"] = df["Year"].astype(int)

        dataframes.append(df)
        print(f"Metido en la database: '{archivo}'.")


# Combina los DataFrames utilizando la función concat
df_combined = pd.concat(dataframes, ignore_index=True)

# Elimina las transacciones con "Year" previo a 2015
df_combined = df_combined[df_combined["Year"] >= 2015]

#lineas que tengan todos los valores nulos las elimina
df_combined = df_combined.dropna(how='all')

#Las lineas que sean iguales las elimina
df_combined = df_combined.drop_duplicates(subset=["Purchaser","Company","Price","Percent. acq.","Year"])

#Cuando hay dos lineas iguales pero en distintos años, coger el más reciente/eliminar el mas antiguo.
df_combined.sort_values("Year", ascending=False, inplace=True)
df_combined.drop_duplicates(subset=["Purchaser","Company","Price","Percent. acq."], keep='first', inplace=True)

# Si hay 2 líneas iguales pero tienen el apartado price distinto
price_difference_threshold = 0.2  # 20%

for _, group in df_combined.groupby(["Purchaser", "Company", "Percent. acq."]):
    if len(group) == 2:
        prices = group["Price"].values
        price_diff = abs(prices[0] - prices[1])
        price_avg = max(prices)

        if price_diff / price_avg <= price_difference_threshold:
            df_combined.drop(group.index, inplace=True)
            df_combined = pd.concat([df_combined, group.loc[group["Price"].idxmax()]], ignore_index=True)


# Pone IDs
#df_combined = df_combined.drop(columns=["ID"])
df_combined["ID"] = range(1, len(df_combined) + 1)
# Poner la columna ID al principio
cols = df_combined.columns.tolist()
cols = cols[-1:] + cols[:-1]
df_combined = df_combined[cols]

# Guarda el DataFrame combinado en un nuevo archivo CSV
df_combined.to_csv("BasedatosPrivados.csv", index=False)

dbcsv = 'C:/Users/Carlota/OneDrive/Escritorio/pae/BasedatosPrivados.csv'

# Cargar el archivo CSV en un DataFrame
data = pd.read_csv(dbcsv)

# Guardar el DataFrame modificado en un nuevo archivo CSV
data.to_csv('BasedatosPrivados.csv', index=False)

# Imprime el DataFrame combinado
print("JUNTADO")


# mainprivadas_v2-------------------------------------
#afegirem que junti les diferents maneres d'esscriure un nom
#hay que añadir el sector en algun momento
#s'ha de poder actualitzar
#posar només la transacció més recent?
#twitter valoracio de l'empresa adquirida
#dolares o euros






#POSIBILITATS:
#Irisbond, , Microsoft, 
#MG o MG Motor Europe o 
#Sabadell - Banco sabadell
#Relypsa - Relypsa, INC.
#PricewaterhouseCooper - PwC 
#Boehringer Ingelheim
