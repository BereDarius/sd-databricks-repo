from pyspark import pipelines as dp
from pyspark.sql.functions import col


# This file defines a sample transformation.
# Edit the sample below or add new transformations
# using "+ Add" in the file browser.


@dp.table
def listings_raw():
    return spark.read.csv("/Volumes/airbnb/v01/sf-listings/sf-airbnb.csv", header=True, inferSchema=True, quote='"', escape='"', multiLine=True)
