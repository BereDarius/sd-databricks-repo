from pyspark import pipelines as dp


# This file defines a sample transformation.
# Edit the sample below or add new transformations
# using "+ Add" in the file browser.


@dp.table
def listings_cleaned_mlflow():
    return spark.read.csv(
        "/Volumes/airbnb/v01/sf-listings/airbnb-cleaned-mlflow.csv",
        header=True,
        inferSchema=True,
        quote='"',
        escape='"',
        multiLine=True,
    )
