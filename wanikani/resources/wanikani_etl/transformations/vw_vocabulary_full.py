from pyspark import pipelines as dp

@dp.view
def vw_vocabulary_full():
  df_vocabulary_sentences_no_readings = spark.read.csv(
    "/Volumes/wanikani/raw/vocabulary_data/wanikani_vocabulary.csv",
    header=True,
    inferSchema=True,
    quote='"',
    escape='"',
    multiLine=True
  )

  df_vocabulary_readings_no_sentences = spark.read.csv(
    "/Volumes/wanikani/raw/vocabulary_data/wanikani_vocabulary_no_sentences.csv",
    header=True,
    inferSchema=True,
    quote='"',
    escape='"',
    multiLine=True
  )

  # Dictionary mapping original column names to their lowercase aliases
  column_aliases = {
    "level": "difficulty_level",
    "characters": "word_jp",
    "meaning": "meaning_en",
    "structure": "csv_structures",
    "sentences": "csv_sentences_jp_and_en",
    "reading": "reading_hiragana_jp",
  }

  full_cols = df_vocabulary_sentences_no_readings.columns
  no_sent_cols = [col for col in df_vocabulary_readings_no_sentences.columns if col not in full_cols or col == "Characters"]

  df_joined = df_vocabulary_sentences_no_readings.join(
    df_vocabulary_readings_no_sentences.select([col.lower() for col in no_sent_cols]), on="Characters", how="inner"
  )

  df_aliased = df_joined.selectExpr(
    *[f"`{col}` as {column_aliases[col.lower()]}" if col.lower() in column_aliases else f"`{col}`" for col in df_joined.columns]
  )

  return df_aliased
