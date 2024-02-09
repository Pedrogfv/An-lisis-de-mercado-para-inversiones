# Índice

1. Contexto
2. Transformacion de datos
3. Dashboard 
4. Stack Tecnológico

# Contexto
Recordaremos aquí el alcance del proyecto: el mismo está acotado por rubro de negocio, geográfica y temporalmente. Se trabajó sobre restaurantes 
de los Estados Unidos con registros entre los años 2010 a 2021.
Nos ubicamos ahora en qué etapa del proyecto nos encontramos. Los datos ya se han pasado por los siguientes procesos:
almacenamiento de archivos fuente en Cloud Storage, definición y ejecución de un proceso de ETL automatizado realizado en Cloud Functions,
almacenamiento de las bases de datos resultante en Big Query.

# Transformación de datos 🔃✨
ETL (Extracción, Transformación y Carga):
En este segundo sprint, nuestros ingenieros de datos llevaron a cabo las siguientes transformaciones en el dataset de Google Maps:

Generalización de categorías:
Dataset: metadata de los restaurants, archivo "metadata_restaurants_v3.parquet".
Columna modificada: "categories", posee información sobre las categorías de cada restaurant.
Se crearon 28 categorías generales con el objetivo de encasillar las más de 2000 categorías específicas de los restaurantes. 
A cada categoría específica se le asignaron hasta 3 categorías generales.
Por cada registro en la columna "categories" detectamos las 2 primeras frases correspondientes a categorías específicas.
Como resultado de la transformaciones aplicadas, contamos con 3 nuevas columnas en el dataset de metadata:
"general 1": esta hace referencia a la primer categoría general de la primera categoría específica detectada.
"general 2": esta hace referencia a la segunda categoría general de la primera categoría específica detectada.
"general 3": esta hace referencia a la primera categoría general de la segunda categoría específica detectada.
Las categorías generales creadas son las siguientes:
Asian, Latin, American, Cafe/Breakfast, Sándwich, Sweets/Desserts, Asian, Arab, Fusion, African, European, Mediterranean, Seafood, BBQ/Grill, Pizza, Italian,
Kosher/Halal, Deli, Hamburguer, Chicken, Family/Homemade, Healthy/Organic,
Meat/Steak house, Mexican, Taco, Bar, Veggie/Plant based, Gas station.

Priorización de los aributos principales:
Dataset: metadata de los restaurants, archivo "metadata_restaurants_v4.parquet".
Columna modificada: "MISC", posee información sobre los atributos (comodidades, servicios, características, etc.) de cada restaurant.
Se tomaron únicamente los 20 atributos con mayor frecuencia (aparición) en la columna "MISC".
Con cada uno de ellos se hicieron 20 nuevas columnas tipo dummies que nos indican si cierto restaurant cuenta con ese atributo o no.
Las 20 nuevas columnas son:
'Service options: Delivery', 'Amenities: Good for kids', 'Service options: Takeout', 'Atmosphere: Casual', 'Accessibility: Wheelchair accessible entrance',
'Offerings: Comfort food', 'Popular for: Solo dining', 'Offerings: Quick bite', 'Popular for: Lunch', 'Service options: Dine-in', 'Popular for: Dinner', 
'Dining options: Dessert', 'Crowd: Groups', 'Dining options: Lunch', 'Offerings: Coffee', 'Payments: Debit cards', 'Offerings: Small plates', 'Dining options: Dinner',
'Offerings: Vegetarian options', 'Crowd: Tourists'.

  Se estás utilizando una combinación de servicios en la nube de Google (Cloud Storage, BigQuery y Cloud Data Fusion) para gestionar tus datos de manera eficiente
Carga de archivos en Cloud Storage (Buckets):

Los archivos originales del data set se cargan manualmente en Cloud Storage, que actúa como un sistema de almacenamiento en la nube altamente escalable y duradero.
Creación de Dataset y tablas en BigQuery:

Se genera manualmente el data set y las tablas con los esquemas vacíos en BigQuery, que es un servicio de almacenamiento y análisis de datos totalmente administrado.
ETL automatizado con Cloud Data Fusion:

Cloud Data Fusion se utiliza para la extracción, transformación y carga (ETL) de los datos.
Cuando se carga un nuevo archivo en el Bucket de Cloud Storage, se activa automáticamente un flujo de trabajo ETL en Cloud Data Fusion.
Este flujo de trabajo ETL utiliza el servicio Tiger automatizado para realizar las transformaciones necesarias en los datos según las especificaciones definidas.
Una vez que se completan las transformaciones, los datos se cargan automáticamente en las tablas correspondientes de BigQuery.
Este flujo de trabajo automatizado te permite gestionar eficientemente tus datos, desde la carga inicial hasta la transformación y almacenamiento en BigQuery para su análisis posterior. 
La automatización garantiza la consistencia y la eficiencia del proceso, permitiéndote centrarte en el análisis y la obtención de información valiosa a partir de tus datos.



![WhatsApp Image 2024-02-08 at 18 32 55](https://github.com/mariebraca21/Pf.google_yelp/assets/86693811/80283080-766d-4bcf-8a5a-54317f7d4afc)


![WhatsApp Image 2024-02-08 at 18 33 48](https://github.com/mariebraca21/Pf.google_yelp/assets/86693811/3070fb0d-e366-4cf9-883b-b4868a0037ec)

![WhatsApp Image 2024-02-08 at 18 35 06](https://github.com/mariebraca21/Pf.google_yelp/assets/86693811/5d62c4e1-99c1-4991-aa35-66843c763500)

![WhatsApp Image 2024-02-08 at 18 38 48](https://github.com/mariebraca21/Pf.google_yelp/assets/86693811/d74dfce6-d419-44d0-bc97-4d0295a13a33)

# Avances en Machine Learning 
Se consulto sobre las herramientas disponibles para Machine Learning en Google Cloud Platform, se decidió usar Vertex AI porque es la que tiene más información sobre su uso.
Se consulto sobre como manejar los datasets, construir y entrenar los modelos de machine learning de regresión, clasificación y series temporales.
Se consulto también como hacer los pipelines para MLOps, ajustar hiperparámetros y el uso SDK.
Se realizo una práctica en Vertex Workbench, para probar esta plataforma, donde se realizó el análisis de sentimiento.
Los principales atributos o “features” para el entrenamiento del algoritmo son: Rating, nombre del restaurante, nombre del estado, categoría, cantidad de reseñas
y análisis de sentimiento.


# Dashboard 👨🏽‍💼👩‍💼💻📊
La presente etapa tiene como objetivo desarrollar un dashboard interactivo que permita a los empresarios explorar los datos 
y extraer información relevante sobre los restaurantes.
![dashboard jpg](https://github.com/mariebraca21/Pf.google_yelp/assets/86693811/cd529f7c-2411-47f2-b212-96c2aaf633a9)
https://lookerstudio.google.com/reporting/31466819-180d-4c6e-9b35-8877b52cd085/page/p_ywrf6c8bed?s=glNNDEVpPkE



