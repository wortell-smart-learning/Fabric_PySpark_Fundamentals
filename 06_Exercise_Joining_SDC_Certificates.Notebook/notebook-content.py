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

# # Certificate mania

# MARKDOWN ********************

#  Try to answer the following question using a merge:<br><br>Which colleague has no certificates registered in the SDC database?

# MARKDOWN ********************

#  Hints:
# - use `df.join()`
# - use datafiles `sdc_certificaten.csv` and `sdc_personeel.csv`
# - for joining use the argument `on`, but consult the [docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.join.html) for examples on how to handle different column names on left / right sides.
# - you can use `df.distinct()` to get the unique values in a column

# CELL ********************

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('06 Exercise').getOrCreate()

df_cert = spark.read.csv('Files/csvsources/sdc_certificaten.csv', inferSchema=True, header=True, multiLine=True)
df_ppl = spark.read.csv('Files/csvsources/sdc_personeel.csv', inferSchema=True, header=True, multiLine=True)

# CELL ********************

display(df_cert)

# CELL ********************

display(df_ppl)

# MARKDOWN ********************

#  1) Looking at `sdc_personeel.csv`, how many colleagues do you have? 

# CELL ********************

df_ppl.count()

# MARKDOWN ********************

#  2) How many Barts en Jeroens do we have in our company?

# CELL ********************

display(
    df_ppl
    .where(
        df_ppl
        .Voornaam
        .isin(['Bart', 'Jeroen'])
    )
    .groupby('Voornaam')
    .count()
)

# MARKDOWN ********************

#  3) How many certificates are currently listed in `sdc_certificaten.csv` ?

# CELL ********************

df_cert.select('certificaat').distinct().count()

# MARKDOWN ********************

#  4) Which certificate is listed the most?

# CELL ********************

display(
    df_cert
    .groupby('certificaat')
    .count()
    .sort('count', ascending=False)
    .limit(3)
)

# MARKDOWN ********************

#  5) Which certificates does colleague `LaSo` have?

# CELL ********************

display(
    df_cert.filter('personeel == "LaSo"')
)

# MARKDOWN ********************

#  6) For figuring out who doesn't have a certificate, we need to join `sdc_personeel.csv` and `sdc_certifaten.csv`. Think carefully how you join these two. Please create the join and assign it to a new dataframe variable. Use arguments `left_on` and `right_on` instead on `on` to specify the fields of the two tables to join on.

# CELL ********************

df_joined = df_ppl.join(df_cert, df_ppl.personeelcode == df_cert.personeel, 'left')

display(df_joined)

# MARKDOWN ********************

#  7) So we now have the merged file. Now use for example a `.groupby()` with a `.count()` to figure out who doesn't have any certificates.

# CELL ********************

# The trick here is to find Null values:
from pyspark.sql.functions import col
no_match_df = df_joined.filter(col('certificaat').isNull())
display(no_match_df)

# MARKDOWN ********************

#  8) In which year were the most certificates received? Do a `.groupby()` and as an extra: try to create a nice barplot of the result

# CELL ********************

display(
    df_joined
    .filter(col('certificaat').isNotNull())
    .groupby('jaar_behaald')
    .count()
    .sort('count', ascending=False)
)

# CELL ********************

import plotly.express as px

# CELL ********************

px.bar(
    title='Top 5 highest rated B&W movies',
    data_frame=df_joined.filter(col('certificaat').isNotNull()).groupby('jaar_behaald').count().sort('count', ascending=False),
    x='jaar_behaald',
    y='count'
)
