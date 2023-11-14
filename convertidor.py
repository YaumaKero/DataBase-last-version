import os
import json
import csv

#directorio
directorio_json = 'C:/Users/jaume/Documents/VISUAL CODES/PAE/PAE-basedatos/publicos'

#FUNCIO QUE ES FARA PER A CADA ARXIU DE LA CARPETA
def convertir_json_a_csv(archivo_json):
    archivo_csv = os.path.splitext(archivo_json)[0] + '.csv'
    # Abrir el archivo JSON y el archivo CSV de salida
    with open(os.path.join(directorio_json, archivo_json), 'r') as archivo_entrada, open(archivo_csv, 'w', newline='') as archivo_salida:
        # Cargar el contenido del archivo JSON
        datos_json = json.load(archivo_entrada)
        
        # Crear un objeto CSV writer
        escritor_csv = csv.writer(archivo_salida)
        
        # Escribir las cabeceras (nombres de las columnas) en el archivo CSV
        # Si los datos JSON son una lista de diccionarios, puedes usar la primera
        # entrada para generar las cabeceras.
        if isinstance(datos_json, list) and len(datos_json) > 0:
            cabeceras = datos_json[0].keys()
            escritor_csv.writerow(cabeceras)
            
        # Escribir los datos en el archivo CSV
        if isinstance(datos_json, list):
            for fila in datos_json:
                escritor_csv.writerow(fila.values())
        elif isinstance(datos_json, dict):
            escritor_csv.writerow(datos_json.keys())
            escritor_csv.writerow(datos_json.values())
        
    print(f"Se ha convertido el archivo JSON '{archivo_json}' en el archivo CSV '{archivo_csv}'.")

print("Se han convertido los archivos JSON en archivos CSV.")
