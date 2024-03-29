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

# # Aggregating and summarizing data

# CELL ********************

from pyspark.sql import SparkSession
import pandas as pd
import plotly.express as px

spark = SparkSession.builder.appName('05_Aggregating_and_summarizing_data').getOrCreate()


# CELL ********************

df = spark.read.csv('Files/csvsources/most_voted_titles_enriched.csv', inferSchema=True, header=True)
df = df.filter(df['titleType'].isin(['tvSeries', 'movie']))

display(
  df.limit(3)
)

# MARKDOWN ********************

# You can do a simple count of values:

# CELL ********************

df.groupBy('endYear').count().limit(5).show()

# MARKDOWN ********************

#  If you want percentages you need to calculate the entire count first:

# CELL ********************

from pyspark.sql.functions import col, sum as _sum, round

# Calculate counts
df_count = df.groupBy('endYear').count()

# Calculate total count
total_count = df_count.select(_sum('count')).first()[0]

# # Normalize counts
df_normalized = df_count.withColumn('normalized_count', round(df_count['count'] / total_count, 4))

# df_normalized.limit(5).show()

df_normalized.sort('normalized_count', ascending=False).limit(5).show()

# MARKDOWN ********************

#  But one of the most powerful features of pySpark is the method `.groupby()`
#  This makes it possible to divide your data in groups and summarize it however you like.
#  With built-in functions such as .mean(), but you also create your own custom functions

# MARKDOWN ********************

#  Let's first group data by title type

# CELL ********************

df.groupby('titleType')

# MARKDOWN ********************

#  Okay, we grouped the data, we don't see anything. We still need to specify what to do with the groups. Let's calculate a `.mean()`.

# CELL ********************

display(
  df.groupby('titleType').mean()
)

# MARKDOWN ********************

#  Or just a `.count()` of the columns:

# CELL ********************

df.groupby('titleType').count().show()

# MARKDOWN ********************

#  Or check the mean rating per start year (for movies) and use pandas plotting

# CELL ********************

(df
    .filter('titleType == "movie"')
    .groupby('startYear')
    .mean('averageRating')
    .sort('startYear')
    .toPandas() # Watch out, converting to pandas here!
    .set_index('startYear')
    .plot()
)

# MARKDOWN ********************

#  But some years have much more movies than others. How does that effect the mean rating per start year. <br> Below is an example of method chaining: applying all sorts of functions after eachother.

# CELL ********************

from pyspark.sql import functions as sf

df_group_startyear = (df
    .filter('titleType == "movie"')
    .groupby('startYear')
    .agg(sf.mean('averageRating').alias('mean (avgRating)'), sf.count('averageRating').alias('count (avgRating)'))
)
df_group_startyear.limit(3).show()

# MARKDOWN ********************

#  And let's plot the result with plotly express

# CELL ********************

px.scatter(
    title='Average rating per start year', 
    data_frame=df_group_startyear.toPandas(), 
    x='startYear', 
    y='mean (avgRating)', 
    size='count (avgRating)', 
    size_max=25,
    height=400,
    width=700,
)

# MARKDOWN ********************

# There's a whole of functions you can apply to groups. These are just examples:
# - count()
# - mean()
# - min()
# - max()
# 
# 
# See more info here:  
# 
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.GroupedData.html#pyspark.sql.GroupedData

# MARKDOWN ********************

# Last thing: let's say you want to apply a custom aggregation to your groups. How do we do that?
# 
# In PySpark, you can achieve custom aggregation using the agg() function along with udf (User Defined Function). Here's how you can do it:
# 
# First, you need to define your custom function and convert it into a udf.

# CELL ********************

from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType # The return type of the function will be a double (floating point number)

def custom_mean_calculation(x):
    return (sum(x) / len(x)) * 10

custom_mean_calculation_udf = udf(custom_mean_calculation, DoubleType())

# MARKDOWN ********************

# Then, you can use this udf in your aggregation:

# CELL ********************

from pyspark.sql import functions as F

display(
    df
    .groupBy('startYear')
    .agg(
        custom_mean_calculation_udf(F.collect_list('averageRating'))
        .alias('groupMeanRating')
    )
)
