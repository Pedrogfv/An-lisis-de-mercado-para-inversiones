import pandas as pd
from datetime import datetime
import re

# def describir_df(df, campos_excluir=None, campos_incluir=None)
# def tipo_datos(df, lista_campos=None)
# def stats_campos(dataframe, lista_campos)
# def max_min_campos(dataframe, lista_campos)
# def lista_campos(df, lista_campos=None)
# def valores_unicos(df, lista_campos)
# def duplicados(df, campos_excluir=None, campos_incluir=None)
# def registros_al_azar(df, cantidad_registros)
# def convertir_a_datetime(valor)



##################################################
def describir_df(df, campos_excluir=None, campos_incluir=None):
 
    # Aplicar filtros de exclusión o inclusión
    if campos_excluir:
        df = df.drop(columns=campos_excluir)
    elif campos_incluir:
        df = df[campos_incluir]
    else:
        df 
   
    # Calcular cantidad total de registros
    cantidad_total_registros = len(df)
    print("Cantidad Registros: ", cantidad_total_registros)
    print('Cantidad Campos: ', len(df.columns))
    
    # Mostrar lista de campos
    print("Campos:\n", df.columns) 
    
    # Contar valores nulos y no nulos en cada columna
    conteo_nulos = df.isnull().sum()
    conteo_no_nulos = df.notnull().sum()
    
    # Calcular porcentaje de nulos y no nulos
    porcentaje_nulos = ((conteo_nulos / cantidad_total_registros) * 100).round(2)
    porcentaje_no_nulos = ((conteo_no_nulos / cantidad_total_registros) * 100).round(2)

    # Obtener una lista de todos los tipos de datos presentes en cada columna
    tipos_de_datos_por_columna = [df[column].apply(type).unique() for column in df.columns]

    # Crear un DataFrame con los resultados
    resultados = pd.DataFrame({
        'Campo': df.columns,
        'Tipo de Dato': tipos_de_datos_por_columna,
        'Valores Nulos': conteo_nulos.values,
        '% Nulos': porcentaje_nulos.values,
        'Valores No Nulos': conteo_no_nulos.values,
        '% No Nulos': porcentaje_no_nulos.values,
        'Valores Únicos': df.nunique().values,
        '% Únicos': ((df.nunique() / cantidad_total_registros) * 100).round(2).values
    })

    return resultados
##################################################

##################################################
def tipo_datos(df, lista_campos=None):
    """
    Esta función toma un DataFrame y una lista opcional de campos como entrada
    y muestra el tipo de datos para cada campo. Si no se proporciona una lista de campos,
    analiza todos los campos del DataFrame.
    Si un campo tiene más de un tipo de datos, los muestra por separado.
    """
    if lista_campos is None:
        lista_campos = df.columns

    tipos_por_campo = {}

    for campo in lista_campos:
        tipos_diferentes = df[campo].apply(type).value_counts()
        tipos_por_campo[campo] = ', '.join([f"{tipo} ({cantidad})" for tipo, cantidad in tipos_diferentes.items()])

    resultados = pd.DataFrame(list(tipos_por_campo.items()), columns=['Campo', 'Tipo de Dato'])

    return resultados
##################################################

##################################################
def stats_campos(dataframe, lista_campos):
    """
    Esta función toma un DataFrame y una lista de campos como entrada
    y devuelve estadísticas para esos campos en un DataFrame.
    """
    stats = dataframe[lista_campos].describe().round(2)
  
    return stats
##################################################

##################################################
def max_min_campos(dataframe, lista_campos):
    """
    Esta función toma un DataFrame y una lista de campos como entrada
    y devuelve los valores máximos y mínimos para esos campos.
    """
    maximos_minimos = dataframe[lista_campos].describe().transpose()[['min', 'max']]
    
    return maximos_minimos
##################################################

##################################################
def valores_unicos(df, lista_campos=None):
    """
    Esta función toma un DataFrame y una lista de campos como entrada
    y devuelve un diccionario con los valores únicos para cada campo.
    Si no se proporciona una lista de campos, se toman todos los campos.
    """
    if lista_campos is None:
        lista_campos = df.columns.tolist()

    valores_unicos_por_campo = {}
    
    for campo in lista_campos:
        valores_unicos_por_campo[campo] = df[campo].unique()
    
    return valores_unicos_por_campo
##################################################

##################################################
def buscar_valor(df, valores=None, campos=None):
    # Se cuentan los registros que contienen algún campo con el valor o valores
    if valores is not None:
        if not isinstance(valores, list):
            valores = [valores]

        for valor in valores:
            valor_cantidad = df[df.eq(valor).any(axis=1)]
            print(f"Cantidad de registros con '{valor}': {len(valor_cantidad)}\n")
    # else:
    #    print(f"Cantidad de registros con valor nulo: {df[campos].isnull().any(axis=1).sum()}\n")

    resultados = {}

    if campos is None:
        campos = df.columns

    for campo in campos:
        if campo in df.columns:
            if valores is not None:
                for valor in valores:
                    count = (df[campo] == valor).sum()
                    if count != 0:
                        resultados[(campo, valor)] = count
            else:
                count = df[campo].isnull().sum()
                if count != 0:
                    resultados[(campo, 'Nulo')] = count
    
    print(f"Total de apariciones en el dataframe:\n{resultados}\n")
##################################################

##################################################
def buscar_moda(df, campos):
    """
    Busca la moda para cada campo en el DataFrame.

    Parameters:
    - df: DataFrame
    - campos: str o lista de str
        Campo o campos para los cuales se buscará la moda.

    Returns:
    - moda_resultados: dict
        Un diccionario donde las claves son los campos y los valores son las modas correspondientes.
    """
    moda_resultados = {}

    if isinstance(campos, str):
        campos = [campos]

    for campo in campos:
        moda = df[campo].mode().iloc[0]
        moda_resultados[campo] = moda

    return moda_resultados
##################################################

##################################################
def imputar_valores(df, valores_a_reemplazar, valor_a_imputar=None, campos=None):
    """
    Imputa valores en el DataFrame para los campos especificados o en todo el DataFrame si no se proporcionan campos.

    Parameters:
    - df: DataFrame
    - valores_a_reemplazar: cualquier, lista o diccionario
        El valor o valores que se buscarán para reemplazar en el DataFrame.
    - valor_a_imputar: cualquier, opcional
        El valor con el cual se imputarán los valores encontrados. Si no se proporciona, se utilizará None.
    - campos: str o lista de str, opcional
        Campo o campos en los que se imputarán los valores. Si no se proporcionan, se imputarán en todo el DataFrame.

    Returns:
    - df_imputado: DataFrame
        El DataFrame con los valores imputados.
    """    

    if campos is None:
        campos = df.columns.tolist()
    elif isinstance(campos, str):
        campos = [campos]

    for campo in campos:
        df[campo] = df[campo].replace({val: valor_a_imputar for val in valores_a_reemplazar})

    return df

##################################################

##################################################

def duplicados(df, campos_excluir=None, campos_incluir=None):
    """
    Encuentra y devuelve los duplicados en un DataFrame basándose en todas las filas y campos,
    con opciones para excluir o incluir campos específicos, y agrega la frecuencia de la combinación de valores duplicados.

    Parameters:
    - df: DataFrame de pandas
    - campos_excluir: Lista de campos a excluir de la búsqueda de duplicados (opcional)
    - campos_incluir: Lista de campos para incluir en la búsqueda de duplicados (opcional)

    Returns:
    - DataFrame con los registros duplicados, ordenados por todas las columnas, y con la frecuencia agregada
    """

    # Aplicar filtros de exclusión o inclusión
    if campos_excluir:
        df_filtrado = df.drop(columns=campos_excluir)
    elif campos_incluir:
        df_filtrado = df[campos_incluir]
    else:
        df_filtrado = df.copy()

    # Identificar y contar duplicados       
    # duplicados = df_filtrado[df_filtrado.duplicated()].sort_values(by=campo_orden)


    # Identificar y contar duplicados
    duplicados = df_filtrado[df_filtrado.duplicated(keep=False)]  # Mantener todas las instancias duplicadas


    # Ordenar por todas las columnas
    duplicados = duplicados.sort_values(by=list(duplicados.columns))

    print("Cantidad de registros duplicados: ", len(duplicados))

    return duplicados
##################################################

##################################################
def mostrar_registros(df, valor, campos=None):
    """
    Muestra los registros que contienen un valor específico (incluido None) en los campos indicados.

    Parameters:
    - df: DataFrame
        El DataFrame en el que buscar.
    - valor: cualquier
        El valor que se desea buscar, incluido None.
    - campos: str o lista de str, opcional
        El campo o campos en los que buscar el valor. Si no se proporcionan, se buscará en todo el DataFrame.

    Returns:
    DataFrame
        Los registros filtrados que cumplen con la condición.
    """
    if campos is None:
        # Si no se proporcionan campos, buscar en todo el DataFrame
        registros_filtrados = df[df.apply(lambda row: valor in row.values, axis=1)]
    else:
        if isinstance(campos, str):
            campos = [campos]

        # Filtrar y mostrar los registros que cumplen con la condición en los campos especificados
        registros_filtrados = df[df[campos].eq(valor).any(axis=1)]
    
    return registros_filtrados
##################################################

##################################################
def registros_al_azar(df, cantidad_registros):
    """
    Esta función toma un DataFrame y la cantidad de registros a mostrar como entrada,
    y devuelve esos registros seleccionados al azar con una semilla basada en la hora actual.
    """
    semilla = int(datetime.now().timestamp())  # Generar una semilla basada en la hora actual
    registros_al_azar = df.sample(n=cantidad_registros, random_state=semilla)
    return registros_al_azar
##################################################

##################################################
# Define una función para convertir un valor str a datetime.time
def convertir_a_datetime(valor):
    try:
        datetime_obj = pd.to_datetime(valor)
        if datetime_obj is not None:
            return datetime_obj.time()
        else:
            return valor
    except (ValueError, TypeError):
        return valor
##################################################
    
##################################################
# Función para extraer el año o devolver nulo si no se puede extraer
def extraer_año(texto):
    try:
        año = int(re.search(r'(\d{4})', texto).group(1))
        return año
    except (AttributeError, TypeError):
        return None
##################################################

##################################################
def crear_rango(df_total, campo_calculado, max_valor, salto_bins):
    # Crea una nueva columna llamada 'rango_'+campo_calculado utilizando pd.cut
    bins = [i * salto_bins for i in range(int(max_valor/salto_bins) + 1)]
    labels = [f'{i}-{i+salto_bins}' for i in range(0, max_valor, salto_bins)]

    df_total['rango'] = pd.cut(df_total[campo_calculado], bins=bins, labels=labels, right=False)

    # Agrupa por el rango de campo_calculado y cuenta la cantidad de usuarios en cada grupo
    agrupado_por_rango = df_total.groupby('rango')[campo_calculado].count().reset_index()

    # Renombrar la columna a 'cantidad'
    agrupado_por_rango = agrupado_por_rango.rename(columns={campo_calculado: 'cantidad'})

    # Calcula el porcentaje en relación con el total de usuarios
    agrupado_por_rango['porcentaje'] = (agrupado_por_rango['cantidad'] / len(df_total)) * 100

    print(f"Rango {campo_calculado} hasta {max_valor}\n")
    return agrupado_por_rango