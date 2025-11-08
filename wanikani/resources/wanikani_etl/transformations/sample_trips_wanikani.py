from pyspark import pipelines as dp


# This file defines a sample transformation.
# Edit the sample below or add new transformations
# using "+ Add" in the file browser.


@dp.table
def vocabulary_full():
    return spark.read.csv(
        "/Volumes/wanikani/raw/vocabulary_data/wanikani_vocabulary.csv",
        header=True,
        inferSchema=True,
        quote='"',
        escape='"',
        multiLine=True
    )
