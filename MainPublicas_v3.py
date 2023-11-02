import pandas as pd
import os
import json
import csv
import convertidor


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
    convertidor.convertir_json_a_csv(archivo_json)

# Directorio que contiene los archivos CSV
directorio = 'C:/Users/jaume/Documents/VISUAL CODES/PAE'
rutacsv = 'C:/Users/jaume/Documents/VISUAL CODES/PAE/PAE-basedatos/CSVs'

# Itera a través de los archivos en el directorio
for archivo in os.listdir(rutacsv):
    if archivo.endswith('.csv'):  # Asegúrate de que sean archivos CSV
        ruta_completa = os.path.join(rutacsv, archivo)
        df = pd.read_csv(ruta_completa)
        dataframes.append(df)

# Combina los DataFrames utilizando la función concat
df_combined = pd.concat(dataframes, ignore_index=True)

#Las lineas que sean iguales las elimina
df_combined = df_combined.drop_duplicates(subset=["symbol","name","country","sector","industry","ev","employees","stock price","# of shares","revenue","ebitda","profitability"])

#la columna revenue separala en 4 columnas, cada vez que encuentres un punto, coge los caracteres antresiores hasta encontrar un espacio
#elimina los "0" que esten solos
df_combined["revenue 2023"] = df_combined["revenue"].str.split(".").str[0]
df_combined["revenue 2022"] = df_combined["revenue"].str.split(".").str[1]
df_combined["revenue 2021"] = df_combined["revenue"].str.split(".").str[2]
df_combined["revenue 2020"] = df_combined["revenue"].str.split(".").str[3]
#elimina el primer caracter de revenue 2022 2021 y 2020
df_combined["revenue 2022"] = df_combined["revenue 2022"].str[1:]
df_combined["revenue 2021"] = df_combined["revenue 2021"].str[1:]
df_combined["revenue 2020"] = df_combined["revenue 2020"].str[1:]
#elimina la fecha de revenue 2023, 2022, 2021 y 2020
df_combined["revenue 2023"] = df_combined["revenue 2023"].str[10:]
df_combined["revenue 2022"] = df_combined["revenue 2022"].str[10:]
df_combined["revenue 2021"] = df_combined["revenue 2021"].str[10:]
df_combined["revenue 2020"] = df_combined["revenue 2020"].str[10:]
#elimina el primer caracter de revenue 2022 2021 y 2020
df_combined["revenue 2022"] = df_combined["revenue 2022"].str[1:]
df_combined["revenue 2021"] = df_combined["revenue 2021"].str[1:]
df_combined["revenue 2020"] = df_combined["revenue 2020"].str[1:]
#elimina los espacios en blanco de 2023 2022 2021 y 2020
df_combined["revenue 2023"] = df_combined["revenue 2023"].str.replace(" ","")
df_combined["revenue 2022"] = df_combined["revenue 2022"].str.replace(" ","")
df_combined["revenue 2021"] = df_combined["revenue 2021"].str.replace(" ","")
df_combined["revenue 2020"] = df_combined["revenue 2020"].str.replace(" ","")

#eliminamos la columna revenue inicial, y las columnas creadas anteriormente las ponemos entre la columna de # of shares y ebitda
df_combined = df_combined.drop(columns=["revenue"])
df_combined = df_combined[["symbol","name","country","sector","industry","ev","employees","stock price","# of shares","revenue 2023","revenue 2022","revenue 2021","revenue 2020","ebitda","profitability"]]

#igual que con la columna revenue, hacemos lo mismo con ebitda
df_combined["ebitda 2023"] = df_combined["ebitda"].str.split(".").str[0]
df_combined["ebitda 2022"] = df_combined["ebitda"].str.split(".").str[1]
df_combined["ebitda 2021"] = df_combined["ebitda"].str.split(".").str[2]
df_combined["ebitda 2020"] = df_combined["ebitda"].str.split(".").str[3]
df_combined["ebitda 2022"] = df_combined["ebitda 2022"].str[1:]
df_combined["ebitda 2021"] = df_combined["ebitda 2021"].str[1:]
df_combined["ebitda 2020"] = df_combined["ebitda 2020"].str[1:]
df_combined["ebitda 2023"] = df_combined["ebitda 2023"].str[10:]
df_combined["ebitda 2022"] = df_combined["ebitda 2022"].str[10:]
df_combined["ebitda 2021"] = df_combined["ebitda 2021"].str[10:]
df_combined["ebitda 2020"] = df_combined["ebitda 2020"].str[10:]
df_combined["ebitda 2022"] = df_combined["ebitda 2022"].str[1:]
df_combined["ebitda 2021"] = df_combined["ebitda 2021"].str[1:]
df_combined["ebitda 2020"] = df_combined["ebitda 2020"].str[1:]
df_combined["ebitda 2023"] = df_combined["ebitda 2023"].str.replace(" ","")
df_combined["ebitda 2022"] = df_combined["ebitda 2022"].str.replace(" ","")
df_combined["ebitda 2021"] = df_combined["ebitda 2021"].str.replace(" ","")
df_combined["ebitda 2020"] = df_combined["ebitda 2020"].str.replace(" ","")
df_combined = df_combined.drop(columns=["ebitda"])
df_combined = df_combined[["symbol","name","country","sector","industry","ev","employees","stock price","# of shares","revenue 2023","revenue 2022","revenue 2021","revenue 2020","ebitda 2023","ebitda 2022","ebitda 2021","ebitda 2020","profitability"]]

#en la clumna stockprice eliminamos "Date " y "Freq"
df_combined["stock price"] = df_combined["stock price"].str.replace("Date","") 
df_combined["stock price"] = df_combined["stock price"].str.replace("Freq: M","")

#igual que con la columna revenue hacemos lo mismo con stock price pero tambien quedate con 3 caracteres despues del punto

# Define una lista de fechas en el formato "año-mes-día"
fechas = [
    "columna vacia", "2023-09-30", "2023-08-30", "2023-07-30", "2023-06-30", "2023-05-30", "2023-04-30",
    "2023-03-30", "2023-02-28", "2023-01-30", "2022-12-30", "2022-11-30", "2022-10-30",
    "2022-09-30", "2022-08-30", "2022-07-30", "2022-06-30", "2022-05-30", "2022-04-30",
    "2022-03-30", "2022-02-28", "2022-01-30", "2021-12-30", "2021-11-30", "2021-10-30",
    "2021-09-30", "2021-08-30", "2021-07-30", "2021-06-30", "2021-05-30", "2021-04-30",
    "2021-03-30", "2021-02-28", "2021-01-30", "2020-12-30", "2020-11-30", "2020-10-30",
    "2020-09-30", "2020-08-30", "2020-07-30", "2020-06-30", "2020-05-30", "2020-04-30",
    "2020-03-30", "2020-02-28", "2020-01-30", "2019-12-30", "2019-11-30", "2019-10-30",
    "2019-09-30", "2019-08-30", "2019-07-30", "2019-06-30", "2019-05-30", "2019-04-30",
    "2019-03-30", "2019-02-28", "2019-01-30", "2018-12-30", "2018-11-30", "2018-10-30", 
]

# Itera a través de las fechas en sentido contrario y crea las columnas en df_combined
for i, fecha in reversed(list(enumerate(fechas))):
    #df_combined[f"stock price {fecha}"] = df_combined["stock price"].str.split("\n").str[-(i + 1)].str.split(" ").str[5]
    df_combined[f"stock price {fecha}"] = df_combined["stock price"].str.split("\n").str[-(i + 1)].str.split(" ").str[-1]
    #cambia los puntos por comas
    df_combined[f"stock price {fecha}"] = df_combined[f"stock price {fecha}"].str.replace(".",",")

#elimina la columna stock price inicial, y las columnas creadas anteriormente las ponemos entre la columna de emplyees y # of shares
df_combined = df_combined.drop(columns=["stock price"])
#elimina la columna de stock price columna vacia
df_combined = df_combined.drop(columns=["stock price columna vacia"])

#la columna profitability la dividimos en 4 columnas, separamos en cada 'kpi' y cogemos el valor que hay despues de 'kpi'
df_combined["profitability 2023"] = df_combined["profitability"].str.split("kpi").str[1].str.split(",").str[0]
#en la columna creada quitamos los ' y los : y los espacios en blanco
df_combined["profitability 2023"] = df_combined["profitability 2023"].str.replace("'","")
df_combined["profitability 2023"] = df_combined["profitability 2023"].str.replace(":","")
df_combined["profitability 2023"] = df_combined["profitability 2023"].str.replace(" ","")
df_combined["profitability 2023"] = df_combined["profitability 2023"].str.replace("{","")
df_combined["profitability 2023"] = df_combined["profitability 2023"].str.replace("}","")
df_combined["profitability 2023"] = df_combined["profitability 2023"].str.replace("]","")
df_combined["profitability 2023"] = df_combined["profitability 2023"].str.replace("[","")
df_combined["profitability 2023"] = df_combined["profitability 2023"].str.replace(" ","")
df_combined["profitability 2023"] = df_combined["profitability 2023"].str.replace(".",",")
df_combined["profitability 2022"] = df_combined["profitability"].str.split("kpi").str[2].str.split(",").str[0]
df_combined["profitability 2022"] = df_combined["profitability 2022"].str.replace("'","")
df_combined["profitability 2022"] = df_combined["profitability 2022"].str.replace(":","")
df_combined["profitability 2022"] = df_combined["profitability 2022"].str.replace(" ","")
df_combined["profitability 2022"] = df_combined["profitability 2022"].str.replace("{","")
df_combined["profitability 2022"] = df_combined["profitability 2022"].str.replace("}","")
df_combined["profitability 2022"] = df_combined["profitability 2022"].str.replace("]","")
df_combined["profitability 2022"] = df_combined["profitability 2022"].str.replace("[","")
df_combined["profitability 2022"] = df_combined["profitability 2022"].str.replace(" ","")
df_combined["profitability 2022"] = df_combined["profitability 2022"].str.replace(".",",")
df_combined["profitability 2021"] = df_combined["profitability"].str.split("kpi").str[3].str.split(",").str[0]
df_combined["profitability 2021"] = df_combined["profitability 2021"].str.replace("'","")
df_combined["profitability 2021"] = df_combined["profitability 2021"].str.replace(":","")
df_combined["profitability 2021"] = df_combined["profitability 2021"].str.replace(" ","")
df_combined["profitability 2021"] = df_combined["profitability 2021"].str.replace("{","")
df_combined["profitability 2021"] = df_combined["profitability 2021"].str.replace("}","")
df_combined["profitability 2021"] = df_combined["profitability 2021"].str.replace("]","")
df_combined["profitability 2021"] = df_combined["profitability 2021"].str.replace("[","")
df_combined["profitability 2021"] = df_combined["profitability 2021"].str.replace(" ","")
df_combined["profitability 2021"] = df_combined["profitability 2021"].str.replace(".",",")

#borra la columna profitability inicial
df_combined = df_combined.drop(columns=["profitability"])

#lineas que tengan todos los valores nulos las elimina
df_combined = df_combined.dropna(how='all')

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

# Pregunta si quieres filtrar
print("¿Quieres aplicar algun filtro? (s/n)")
respuesta = input()

# Si la respuesta es "si", pregunta qué ID quieres filtrar
if respuesta == "s":
    print("¿Qué ID quieres usar como referencia para el filtro?")
    ID_referencia = int(input())
    
    # Filtra el DataFrame para obtener el precio de referencia
    precio_referencia = df_combined[df_combined["ID"] == ID_referencia]["ev"].values[0]
    
    # Calcula el rango del 20% del precio de la acción
    rango_20_porciento = precio_referencia * 0.2
    
    # Filtra el DataFrame para mostrar las filas dentro del rango del 10% del precio de la acción
    df_filtrado = df_combined[(df_combined["ev"] >= precio_referencia - rango_20_porciento) &
                              (df_combined["ev"] <= precio_referencia + rango_20_porciento)]
    
    # Muestra el DataFrame filtrado
    #print(df_filtrado["symbol"].to_string(index=False) + "   " + df_filtrado["name"].to_string(index=False) + "   " + df_filtrado["ev"].to_string(index=False))
    print(df_filtrado["name"].to_string(index=False))

    print("FILTRADO")
else:
    print("NO FILTRADO")




