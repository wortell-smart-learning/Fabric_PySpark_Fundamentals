# Synapse Analytics notebook source

# METADATA ********************

# META {
# META   "synapse": {
# META     "lakehouse": {
# META       "default_lakehouse": "c95d7b56-9a7f-4b7c-baf4-ea0bdaacbbf7",
# META       "default_lakehouse_name": "PySparkLakehouse",
# META       "default_lakehouse_workspace_id": "e8b3335a-5e83-466c-bd0d-748c45da7cc9",
# META       "known_lakehouses": [
# META         {
# META           "id": "c95d7b56-9a7f-4b7c-baf4-ea0bdaacbbf7"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Let's make some plots of the movie dataset

# MARKDOWN ********************

#  For which movies / tv series do critics and normal users differ in their opinion?

# MARKDOWN ********************

#  1) Acquire a PySpark session, import plotly.express as px, read in the movies dataset and make sure you use the right settings

# CELL ********************

from pyspark.sql import SparkSession
import seaborn as sns

import plotly.express as px

# some nicer plotly setting
import plotly.io as pio
pio.templates.default = 'plotly_white'

spark = SparkSession.builder.appName('04_Plotting_Data').getOrCreate()
df = spark.read.csv('Files/csvsources/most_voted_titles_enriched.csv', inferSchema=True, header=True, multiLine=True)

display(
    df.limit(3)
)

# MARKDOWN ********************

#  2) Create a subset of your data by only selecting movies and assign it to variable `df_movies`

# CELL ********************

df_movies = df.filter('titleType == "movie"')

# MARKDOWN ********************

#  3) Use a `groupBy` and `count` to count the number of movies per `startYear`. Assign the result to a variable called `df_startyear_count`

# CELL ********************

df_startyear_count = df_movies.groupBy('startYear').count()

# CELL ********************

display(
    df_startyear_count
)

# MARKDOWN ********************

#  4) Create a nice bar plot with plotly.express and find out which year has the most movies in this dataset

# CELL ********************

px.bar(
    title='Movies per year',
    data_frame=df_startyear_count.toPandas(),
    x='startYear',
    y='count'
)

# MARKDOWN ********************

#  5) Create a scatter plot of `metascore` on the x-axis and `averageRating` on the y-axis
#  (metascore is what critics think of the movies, average rating is what users or ordinary viewers think)

# CELL ********************

px.scatter(
    title='metascore (critics) vs average rating (viewers)',
    data_frame=df_movies.toPandas(),
    x='metascore',
    y='averageRating',
    width=1000, # I want to have a square visualization, so the correlation is more clearly visible
    height=1000
)

# MARKDOWN ********************

#  6) Create the same plot as in 5) but add `hover_data=['primaryTitle']` to find out which title is represented by a dot.<br>Find examples of outliers where the critics think it's a bad movie and the users find it a good movie.

# CELL ********************

px.scatter(
    title='metascore (critics) vs average rating (viewers)',
    data_frame=df_movies.toPandas(),
    x='metascore',
    y='averageRating',
    width=1000, # I want to have a square visualization, so the correlation is more clearly visible
    height=1000,
    hover_data=['primaryTitle'],
    labels={'metascore': 'Critics'' ratings', 'averageRating': 'ordinary viewers'' ratings'}
)

# MARKDOWN ********************

#  7) Use the same plot as in 6) and now give the scatters the color based on column `color`.

# CELL ********************

px.scatter(
    title='metascore (critics) vs average rating (viewers)',
    data_frame=df_movies.toPandas(),
    color='color',
    x='metascore',
    y='averageRating',
    width=1000, # I want to have a square visualization, so the correlation is more clearly visible
    height=1000,
    hover_data=['primaryTitle'],
    labels={'metascore': 'Critics'' ratings', 'averageRating': 'ordinary viewers'' ratings'}
)

# MARKDOWN ********************

#  8) You can play with the chart above and turn off scatters by clicking on the legend. Try removing color named 'Color' from the legend. You can also zoom etc.

# MARKDOWN ********************

#  9) Now for the ultimate chart: filter your dataframe so that you only have countries `Germany` and `USA` and use the same code as in 7) and also use argument `facet_col` with column `country` and see what happens

# CELL ********************

px.scatter(
    title='metascore (critics) vs average rating (viewers)',
    data_frame=df_movies.filter(df_movies.country.isin(['Germany', 'USA'])).toPandas(),
    color='color',
    x='metascore',
    y='averageRating',
    facet_col='country',
    width=2000,
    height=1000,
    hover_data=['primaryTitle'],
    labels={'metascore': 'Critics'' ratings', 'averageRating': 'ordinary viewers'' ratings'}
)

# MARKDOWN ********************

#  10) Create a bar plot of the rating of the top 5 highest rated black and white movies

# CELL ********************

px.bar(
    title='Top 5 highest rated B&W movies',
    data_frame=df_movies.filter('color == "Black and White"').sort('averageRating', ascending=False).limit(5).toPandas(),
    x='primaryTitle',
    y='averageRating'
)

# CELL ********************

