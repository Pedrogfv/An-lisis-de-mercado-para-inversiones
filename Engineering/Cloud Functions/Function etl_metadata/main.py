import functions_framework
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
import io
import re

# Autenticar el cliente de BigQuery
bq_client = bigquery.Client()

##########################
@functions_framework.cloud_event
def etl_reviews(cloud_event):  
  # Obtener información del evento
  data = cloud_event.data
  bucket_name = data['bucket']
  file_name = data['name']



  # Extraer el nombre del estado desde la ruta del archivo
  estado_match = re.search(r"review-(.*)/", file_name)
  if estado_match:
    nombre_carpeta = estado_match.group(1)
  else:
    print("No se pudo extraer el nombre del estado.")
    return

    

  # Inicializar el cliente de Storage
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(file_name)


  # Verificar si el objeto es un archivo JSON
  if blob.name.endswith(".json"):
    # Descargar el archivo JSON como objeto de bytes
    blob_data = blob.download_as_string()
    # Leer datos JSON desde el objeto de bytes
    df = pd.read_json(io.BytesIO(blob_data), lines=True)

    # Eliminar las columnas especificadas
    df = df.drop(columns = ['pics', 'resp'])

    # Modificar columnas a tipo string
    df['name'] = df['name'].astype('string')
    df['text'] = df['text'].astype('string')
    df['gmap_id'] = df['gmap_id'].astype('string') 

    # Nombre del archivo en el bucket
    nombre_archivo = 'id_restaurants.txt'
    bucket_metadata = 'etl_metadata_sitios'

    # Descargar el contenido del archivo como una cadena
    blob_metadata = storage_client.bucket(bucket_metadata).blob(nombre_archivo)
    contenido_archivo = blob_metadata.download_as_string().decode('utf-8')

    # Dividir la cadena en una lista de valores
    valores = contenido_archivo.split('\n')

    # Convertir la lista de valores a un conjunto para eliminar duplicados
    valores_set = set(valores)

    # Filtrar df para incluir solo los registros cuyos valores de 'gmap_id' estén en valores_set
    df = df[df['gmap_id'].isin(valores_set)]

    '''
    # Nombre del archivo en el bucket
    nombre_archivo = 'id_restaurants.txt'
    bucket_metadata = 'etl_metadata_sitios'

    # Descargar el contenido del archivo como una cadena
    blob_metadata = storage_client.bucket(bucket_metadata).blob(nombre_archivo)
    contenido_archivo = blob_metadata.download_as_string().decode('utf-8')

    # Dividir la cadena en una lista de valores
    valores = contenido_archivo.split(',')

    # Crear un DataFrame con los valores del archivo
    df_ids = pd.DataFrame({'gmap_id': valores})
    df_ids['gmap_id'] = df_ids['gmap_id'].astype('string') 

    # Filtrar df para incluir solo los registros cuyos valores de 'gmap_id' estén en df_ids
    df = df[df['gmap_id'].isin(df_ids['gmap_id'])]
    '''
    
    # Eliminar duplicados
    df.drop_duplicates(keep='first', inplace=True)

    # Convertir la columna 'datetime' a tipo datetime
    df['datetime'] = pd.to_datetime(df['time'], unit='ms').dt.date 
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Crear columnas 'year' y 'month'
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month

    # Eliminar las columnas especificadas
    df = df.drop(columns = ['time', 'datetime'])

    # Crear la columna 'state_name' con valores vacíos
    df['state_name'] = ''
    df['state_name'] = df['state_name'].astype('string')
    
    # Agregar la columna 'state_name'
    df['state_name'] = str(nombre_carpeta).replace('review_', '')

    # Reemplazar guiones bajos por espacios vacíos
    df['state_name'] = df['state_name'].str.replace('_', ' ')

    # Especificar el ID del dataset y el nombre de la tabla en BigQuery
    dataset_id = 'restaurants'
    table_id = 'reviews_restaurants'
    
    # Crear la tabla si no existe
    table_ref = bq_client.dataset(dataset_id).table(table_id)
    table = bigquery.Table(table_ref)
    table = bq_client.create_table(table, exists_ok=True)
    
    # Cargar el DataFrame en BigQuery
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND  # Modificado para concatenar
    job = bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
    
    print(f"Datos concatenados y cargados en BigQuery: {dataset_id}.{table_id}")
##########################