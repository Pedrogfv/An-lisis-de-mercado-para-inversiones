import functions_framework
import pandas as pd
import numpy as np
from google.cloud import storage
import io
import re
import ast
import os

# Autenticar el cliente de BigQuery
bq_client = bigquery.Client()


##########################
# Función para agregar comas entre categorías
def agregar_comas(cadena):    
    # Busca valores entre comillas.
    valores = re.findall(r"'(.*?)'", cadena)

    # Si hay solo un valor, retorna la cadena original.
    if len(valores) <= 1:
        return cadena

    # Une los valores con comas y espacios.
    cadena_con_comas = ", ".join(valores)

    # Retorna la cadena con las comas añadidas.
    return cadena_con_comas
##########################

@functions_framework.cloud_event
def etl_metadata(cloud_event):  
    data = cloud_event.data
    bucket_name = data['bucket']
    file_name = data['name']
    lock_file = 'processing.lock'  # Nombre del archivo de bloqueo

    # Verificar si el objeto es un archivo JSON
    if file_name.endswith(".json"):
        # Verificar si existe el archivo de bloqueo
        if os.path.exists(lock_file):
            print(f"Otro proceso ya está en curso. No se puede procesar {file_name}.")
            return

        # Crear el archivo de bloqueo
        open(lock_file, 'a').close()

        try:
            # Inicializar el cliente de Storage
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file_name)

            # Descargar el archivo JSON como objeto de bytes
            blob_data = blob.download_as_string()

            # Leer datos JSON desde el objeto de bytes
            df = pd.read_json(io.BytesIO(blob_data), lines=True)

            # Eliminar columnas innecesarias
            df = df.drop(columns=['avg_rating', 'num_of_reviews'])

            # Modificar columnas a tipo string
            df['name'] = df['name'].astype('string')
            df['address'] = df['address'].astype('string')
            df['gmap_id'] = df['gmap_id'].astype('string')
            df['description'] = df['description'].astype('string')
            df['category'] = df['category'].astype('string')
            df['price'] = df['price'].astype('string')
            df['hours'] = df['hours'].astype('string')
            df['MISC'] = df['MISC'].astype('string')        
            df['state'] = df['state'].astype('string')
            df['relative_results'] = df['relative_results'].astype('string')
            df['url'] = df['url'].astype('string')    

            # Filtramos los registros que contienen la categoría "restaurant":
            df = df[df['category'].str.contains("restaurant", case=False)].reset_index(drop=True)

            # Eliminamos los duplicados:
            df.drop_duplicates(inplace=True)

            # Se crea el campo 'categories' copiando la información de 'category'
            df['categories'] = df['category']
            df['categories'] = df['categories'].astype('string')

            # Eliminación de corchetes
            df['categories'] = df['categories'].str.replace("[", "").str.replace("]", "")

            # Se ejecuta función para agregar comas
            df['categories'] = df['categories'].apply(agregar_comas)

            # Se eliminan comillas
            df['categories'] = df['categories'].str.replace("'", "")
            df['categories'] = df['categories'].str.replace('"', '')

            # Exportar DataFrame a archivo Parquet
            blob_df = 'df.parquet'
            # Convertir DataFrame a Parquet y subirlo al bucket
            df.to_parquet(f'gs://{bucket_name}/{blob_df}', engine='pyarrow')

            # CARGAR 'df_metadata.parquet' SI YA EXISTE

            # Configurar el cliente de Storage
            storage_client = storage.Client()

            # Definir los nombres de los archivos parquet en el bucket
            archivo_parquet_df_metadata = "df_metadata.parquet"
        
            # Obtener el bucket
            bucket_name = data['bucket']
            bucket = storage_client.get_bucket(bucket_name)

            # Definir los nombres de los archivos parquet en el bucket
            archivo_parquet_df_metadata = "df_metadata_parcial.parquet"

            # Verificar si el archivo 'df_metadata.parquet' existe en el bucket
            if bucket.blob(archivo_parquet_df_metadata).exists():
                
                # Definir la ruta al archivo Parquet en el bucket
                ruta_archivo_parquet = f"gs://{bucket_name}/{archivo_parquet_df_metadata}"

                # Leer el archivo Parquet directamente en un DataFrame de Pandas
                df_metadata = pd.read_parquet(ruta_archivo_parquet)

                # Modificar columnas a tipo string
                df_metadata['name'] = df_metadata['name'].astype('string')
                df_metadata['address'] = df_metadata['address'].astype('string')
                df_metadata['gmap_id'] = df_metadata['gmap_id'].astype('string')
                df_metadata['description'] = df_metadata['description'].astype('string')
                df_metadata['category'] = df_metadata['category'].astype('string')            
                df_metadata['price'] = df_metadata['price'].astype('string')            
                df_metadata['hours'] = df_metadata['hours'].astype('string')
                df_metadata['MISC'] = df_metadata['MISC'].astype('string')
                df_metadata['state'] = df_metadata['state'].astype('string')
                df_metadata['relative_results'] = df_metadata['relative_results'].astype('string')
                df_metadata['url'] = df_metadata['url'].astype('string')
                df_metadata['categories'] = df_metadata['categories'].astype('string')

                # Modificar columnas a tipo string
                df['name'] = df['name'].astype('string')
                df['address'] = df['address'].astype('string')
                df['gmap_id'] = df['gmap_id'].astype('string')
                df['description'] = df['description'].astype('string')
                df['category'] = df['category'].astype('string')            
                df['price'] = df['price'].astype('string')            
                df['hours'] = df['hours'].astype('string')
                df['MISC'] = df['MISC'].astype('string')
                df['state'] = df['state'].astype('string')
                df['relative_results'] = df['relative_results'].astype('string')
                df['url'] = df['url'].astype('string')
                df['categories'] = df['categories'].astype('string')
                
                # Concatenar df con df_metadata
                df = pd.concat([df_metadata, df], ignore_index=True)
                
                # Eliminar duplicados basados en la columna 'gmap_id' y quedarse con el último registro
                df = df.drop_duplicates(subset='gmap_id', keep='last')
            
            # Exportar DataFrame a archivo Parquet
            blob_df_metadata = 'df_metadata_parcial.parquet'
            # Convertir DataFrame a Parquet y subirlo al bucket
            df.to_parquet(f'gs://{bucket_name}/{blob_df_metadata}', engine='pyarrow')
            

            # MISC EXPAND

            df['MISC'] = df['MISC'].astype('string')

            # Reemplazamos los valores nulos con un diccionario vacío:
            df['MISC'] = df['MISC'].fillna('{}')

            # Convertimos la columna de cadena a diccionario:
            df['MISC'] = df['MISC'].apply(ast.literal_eval)

            # Función para chequear nivel de anidación:
            def nested_level(d):
                """
                Función recursiva para calcular el nivel de anidación de un diccionario.
                """
                if not isinstance(d, dict):
                    return 0
                if not d:
                    return 1
                return 1 + max(nested_level(v) for v in d.values())

            # Calculamos el nivel de anidación para cada diccionario en la columna 'MISC':
            df['nested_level'] = df['MISC'].apply(nested_level)

            df_normalized = pd.json_normalize(df['MISC'])

            from collections import Counter
            lista = []
            for columna in df_normalized.columns:
                # Ejecutar función explode() para convertir las listas en filas duplicadas
                lista_completa = df_normalized[columna].explode().dropna()

                # Contar la frecuencia de cada elemento en la lista completa
                contador = Counter(lista_completa)

                # Obtener los elementos más comunes
                elementos_comunes = contador.most_common()

                # Le agregamos el nombre de la columna a la que pertenece el atributo:
                for atributo in elementos_comunes:
                    atributo = list(atributo)
                    atributo.append(columna)
                    lista.append(atributo)

            # Convertir la lista de tuplas en un DataFrame
            df_atributos = pd.DataFrame(lista, columns=['atributo', 'frecuencia', 'origen'])

            # Ordenar el DataFrame por la columna de frecuencia en orden descendente
            df_atributos = df_atributos.sort_values(by='frecuencia', ascending=False).reset_index(drop=True)

            first20 = df_atributos.head(20)

            # Iteramos sobre los atributos de first20:
            for index, fila in first20.iterrows():
                # Obtenemos el origen y el atributo de la fila actual:
                origen = fila['origen']
                atributo = fila['atributo']

                # Utiliza apply junto con una función lambda para buscar el valor en cada fila de la columna 'MISC'
                df[f"{origen}: {atributo}"] = df.apply(lambda row: atributo in str(row['MISC']), axis=1)

            # Eliminamos columnas auxiliares:
            for index, fila in first20.iterrows():
                atributo = fila['atributo']
                try:
                    del df[atributo]
                except KeyError:
                    pass

            # Eliminamos la columna "nested_level" creada anteriormente:
            del df['nested_level']

            # Obtener los nombres de las últimas 20 columnas
            ultimas_columnas = df.columns[-20:]

            # Crear un diccionario para mapear los nombres de las columnas originales a los nombres modificados
            nuevos_nombres = {nombre: nombre.replace(' ', '__').replace(':', '_').replace('-', '_') for nombre in ultimas_columnas}

            # Renombrar las columnas utilizando el diccionario de mapeo
            df.rename(columns=nuevos_nombres, inplace=True)


            # CATEGORIES EXPAND

            # Creamos la columna "categories_list":
            df["categories_list"] = df["categories"].str.replace("restaurant", "").str.replace("Restaurant", "").str.lower()

            # Le quitamos la palabra "Restaurant" a la columna "categories":
            df["categories"] = df["categories"].str.replace("restaurant", "").str.replace("Restaurant", "").str.lower()

            # Función para convertir texto en lista:
            def convert_to_list(text):
                return [category.strip() for category in text.split(",")]

            # Aplicamos la función a la columna 'categories_list':
            df["categories_list"] = df["categories_list"].apply(convert_to_list)

            # Función para dividir y asignar los primeros 3 elementos de una lista a columnas
            def split_and_assign(categories_list):
                # Obtener los primeros 3 elementos de la lista (o menos si la lista tiene menos de 3 elementos)
                category_1 = categories_list[0] if len(categories_list) > 0 else None
                category_2 = categories_list[1] if len(categories_list) > 1 else None
                category_3 = categories_list[2] if len(categories_list) > 2 else None
                return category_1, category_2, category_3

            # Aplicar la función a la columna 'categories_list'
            df[["category 1", "category 2", "category 3"]] = df["categories_list"].apply(split_and_assign).apply(pd.Series)

            # Eliminamos la columna 'categories_list':
            df.drop(columns=["categories_list"], inplace=True)

            # Dividimos las categorías por coma, quitamos espacios al inicio y al final y las convertimos en una lista de palabras:
            words = df['categories'].str.split(',').explode().str.strip()

            # Convertimos todas las palabras a minúsculas para que sean contadas correctamente:
            words = words.str.lower()

            # Calculamos la frecuencia de cada palabra:
            word_freq = words.value_counts().reset_index()

            # Renombramos las columnas:
            word_freq.columns = ['Palabras', 'Frecuencia']

            # Carga de archivo 'categories.csv'

            # Nombre del archivo CSV en el bucket
            archivo_csv = 'categories.csv'

            # Descargar el archivo CSV como un objeto de bytes
            blob_categories = bucket.blob(archivo_csv)
            contenido_csv = blob_categories.download_as_string()

            # Leer el contenido del archivo CSV en un DataFrame de pandas
            categories = pd.read_csv(io.BytesIO(contenido_csv), sep=';')

            # Corregimos y eliminamos columnas:
            categories["Palabras"] = categories["Palabras"].str.replace("'", "").str.replace(",", "").str.strip()       
            
            categories["Valor"] = categories["Valor"].fillna(1)
            categories["Valor"] = categories["Valor"].astype(int)

            categories["cat_1"] = categories["General Category"]
            categories["cat_2"] = categories["Unnamed: 3"]
            categories["cat_3"] = categories["Unnamed: 4"]
            del categories["General Category"]
            del categories["Unnamed: 3"]
            del categories["Unnamed: 4"]

            # Incluimos la categoría "Gas station" para las frases que contienen "gas " o "fuel":
            categories.loc[categories['Palabras'].str.contains('gas |fuel'), 'cat_1'] = 'Gas station'

            # Corregimos los errores:
            categories["cat_1"] = categories["cat_1"].str.replace("Arabe", "Arab").str.replace("Asiatica", "Asian").str.replace("Mediterranea", "Mediterranean").str.replace("Mediterraneannn", "Mediterranean").str.replace("Mediterraneann", "Mediterranean").str.replace("Chiken", "Chicken")
            categories["cat_2"] = categories["cat_2"].str.replace("Arabe", "Arab").str.replace("Asiatica", "Asian").str.replace("Mediterranea", "Mediterranean").str.replace("Mediterraneannn", "Mediterranean").str.replace("Mediterraneann", "Mediterranean").str.replace("Chiken", "Chicken")
            categories["cat_3"] = categories["cat_3"].str.replace("Arabe", "Arab").str.replace("Asiatica", "Asian").str.replace("Mediterranea", "Mediterranean").str.replace("Mediterraneannn", "Mediterranean").str.replace("Mediterraneann", "Mediterranean").str.replace("Chiken", "Chicken")

            # Limpíamos la columna "category 1":
            df["category 1"] = df["category 1"].replace('', None)

            # Hacemos el primer merge con "category 1", esta tomará la información para "cat_1", "cat_2":
            df = pd.merge(df, categories[["Palabras", "cat_1", "cat_2"]], left_on="category 1", right_on="Palabras", how="left")

            # Hacemos el segundo merge con "category 2", esta tomará la información para "cat_3":
            df = pd.merge(df, categories[["Palabras","cat_3"]], left_on="category 2", right_on="Palabras", how="left")

            # Eliminamos las columnas innecesarias:
            del df["category 1"]
            del df["category 2"]
            del df["category 3"]
            del df["Palabras_x"]
            del df["Palabras_y"]


            # CORRECCIONES FINALES

            # Reemplazar 'None' y '' (cadena) por NaN (valor nulo)
            df.replace('None', pd.NA, inplace=True)
            df.replace('', pd.NA, inplace=True)

            # Reemplazar 'W' por '$' dentro de cada cadena en la columna 'price'
            df['price'] = df['price'].str.replace('₩', '$')

            # Reemplazar los valores nulos por 'Sin Datos' en todo el DataFrame
            df.fillna('Sin Datos', inplace=True)


            # EXPORTAR A PARQUET

            # Configurar el cliente de Storage
            storage_client = storage.Client()
        
            # Obtener el bucket
            bucket_name = data['bucket']
            bucket = storage_client.get_bucket(bucket_name)

            # Exportar DataFrame a archivo Parquet
            blob_df_metadata_final = 'df_metadata_final.parquet'

            # Convertir DataFrame a Parquet y subirlo al bucket
            df.to_parquet(f'gs://{bucket_name}/{blob_df_metadata_final}', engine='pyarrow')
            
            
            # EXPORTAR A BIG QUERY 

            # Autenticar el cliente de BigQuery
            bq_client = bigquery.Client()

            # Definir el proyecto y el dataset
            project_id = 'proyecto-levels-hh'
            dataset_id = 'restaurants'
            table_id = 'metadata_restaurants'

            # Obtener una referencia a la tabla
            table_ref = bq_client.dataset(dataset_id).table(table_id)

            # Intentar eliminar la tabla si existe
            try:
                bq_client.delete_table(table_ref)
                print(f'Tabla {table_id} eliminada.')
            except Exception as e:
                print(f'Error al intentar eliminar la tabla {table_id}: {e}')

            # Crear la tabla
            table = bigquery.Table(table_ref)
            table = bq_client.create_table(table)

            # Cargar el DataFrame en BigQuery
            job_config = bigquery.LoadJobConfig()
            job = bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            job.result()

            print(f"Datos concatenados y cargados en BigQuery: {dataset_id}.{table_id}")        


            # GUARDAR gmap_id UNICOS
            
            # Configurar el cliente de Storage
            client_storage = storage.Client()
            
            # Configurar el cliente de BigQuery
            client_bq = bigquery.Client()

            # Obtener los datos de la columna gmap_id de la tabla
            query = f"""
                SELECT DISTINCT gmap_id
                FROM `{project_id}.{dataset_id}.{table_id}`
            """

            query_job = client_bq.query(query)
            resultados = query_job.result()

            # Crear una lista de los valores únicos de gmap_id
            id_restaurants = [row.gmap_id for row in resultados]

            # Convertir la lista a un string separado por comas
            id_restaurants_str = ','.join(id_restaurants)

            # Nombre del archivo en el bucket
            nombre_archivo = 'id_restaurants.txt'

            # Guardar la lista en un archivo en el bucket

            blob_ids = bucket.blob(nombre_archivo)
            blob_ids.upload_from_string(id_restaurants_str)

        except Exception as e:
            print(f"Error al procesar {file_name}: {str(e)}")

        finally:
            # Eliminar el archivo de bloqueo al finalizar
            if os.path.exists(lock_file):
                os.remove(lock_file)
                print(f"Bloqueo de archivo eliminado para {file_name}.")