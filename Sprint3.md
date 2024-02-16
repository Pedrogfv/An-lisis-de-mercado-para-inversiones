# Indice 
1. Contexto
2. Dashboard
3. KPIs
4. Informe del análisis
5. Modelo de Machine Learning
6. Archivos de Engineering en el repositorio
7. Video del proyecto
<br/>

# Contexto
En esta última etapa, se completa el armado del dashboard, junto con el análisis de los datos trabajados. En este se incluyen los KPIs desarrollados para el análisis. Además contamos con un producto de ML implementado para suplir al análisis.
<br/>

# Dashboard 📊
Se completó el armado Dashboard. Trabajando los datos transformados y cargados por los ingenieros de datos, logramos graficar la data para generar una opción adecuada para el inversionista. Tomando en cuenta los criterios preestablecidos como estados con mayor crecimiento, restaurantes con servicios necesarios y categorías con mayor ratings, entre otros. Utilizamos el modelo de predicción proporcionado por nuestro científico de datos para verificar la oportunidad de crecimiento que tienen los restaurantes. Y logramos definir una oportunidad de negocio para el cliente.

![Gráficos](<Imagen de WhatsApp 2024-02-16 a las 13.05.21_e39958aa.jpg>)

![Gráficos](<Imagen de WhatsApp 2024-02-16 a las 13.05.21_937f9f32.jpg>)

![Gráficos](<Imagen de WhatsApp 2024-02-16 a las 13.05.21_8c84cef6.jpg>)
<br/>

Link del Dashboard: https://lookerstudio.google.com/reporting/eb8206df-b0d8-4223-b7c6-01beb5699bf8/page/p_pi0bcisied

# Informe de análisis 📝
Conclusiones:

- La gráfica de crecimiento de reseñas nos muestra un alza importante en los años 2017 al 2019 donde de repente encontramos una caída del 2020 al 2021.
- Dentro de ésta misma gráfica los dos con mayor crecimiento son Florida y New York.
- Siendo NewYork con el mayor crecimiento de restaurantes en el 2019 de entre todos los estados.
- Con nuestra lista ratings podemos notar como el restaurante de subway goza del mayor rating promedio dentro de los restaurantes.
- Si filtramos toda esta información, estado con mayor crecimiento de restaurantes (New York), año con mayor crecimiento en reseñas (2019), obtendremos una lista con los 10 restaurantes con menor review en ese año en ese estado.
- Elegimos un restaurante que podría funcionar y surge el nombre de WOK CHI - STIR FRY CHIKEN.
<br/>

# Modelo de Machine Learning 👩‍💻
Para esta etapa finalmente se escogió entrenar un modelo de Machine Learning de categoría supervisado, para realizar una regresión, cuyo parámetro a predecir es el rating, el cual es un resultado de la suma de la calificación del usuario y del análisis de sentimiento que se le hizo al comentario hecho por el mismo. Algunos de los Features usados para este fin son: cantidad de reseñas, estado donde esta ubicado el restaurante, categoría y 20 atributos mas del tipo booleano tales como, opción comer en el sitio, opción para llevar, postres, café entre otros. La tecnología o herramienta que se escogió para realizar dicho entrenamiento fue Workbench de VERTEX AI.  
Para realizar el entrenamiento se usaron los siguientes algoritmos de la librería scikit-learn: Ridge, Lasso, ElasticNet, RandomForestRegressor, DecisionTreeRegressor y GradientBoostingRegressor, también se usaron los algoritmos XGBRegressor y LGBMRegressor.  
Después, según el desempeño que tuvo cada algoritmo teniendo en cuenta el “mean absolute error” o MAE tanto en el train como en el test, se escogió el algoritmo XGBRegressor ya qué tuvo el menor MAE y se podía apreciar que no hubo sobreajuste.  
Luego, ya entrenado el modelo, se hicieron predicciones manualmente y también de todo el dataset de entrenamiento para poder analizar los restaurantes con bajas valoraciones y comentarios negativos. También se determino qué factores son los más importantes a la hora de predecir el rating de cada restaurante.

![Top 20 Features](<Imagen de WhatsApp 2024-02-16 a las 12.28.26_48c87cd6.jpg>)
<br/>

# Archivos de Engineering en el repositorio 📂
Los archivos y directorios utilizados en el ETL son los siguientes:

. Carpeta 'Cloud Functions'. Subcarpetas con funciones implementadas en Google Cloud Functions para automatización de ETL en la nube. Subcarpetas 'etl_reviews'  y 'etl_metadata', cada una con archivos 'main.py' y 'requirements.txt' de cada Cloud Function.

. Archivos correspondientes a ETL realizado en forma local:
* '1.1_ETL_metadata.ipynb'
* '1.2_ETL_reviews.ipynb'
* '2_EDA_restaurants.ipynb'
* '3_ETL_restaurants_final.ipynb'
* 'Scraping PBI USA.ipynb'

. Archivo 'my_functions.py'. Contiene funciones auxiliares utilizadas en el ETL local.

. Carpeta Data Auxiliar. Contiene archivos auxiliares procesador en forma local que fueron utilizados tanto para ETL local como en la nube.

# Web Scraping 🌐
Se realizó un Web Scraping de datos macroeconómicos para una posible ampliación del análisis. Los datos extraídos son los siguientes:  
PBI y PBI per cápita de cada estado de Estados Unidos, fuente: https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_GDP  
Población de cada estado de Estados Unidos, fuente: https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_population

