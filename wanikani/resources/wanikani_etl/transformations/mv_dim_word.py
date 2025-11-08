from pyspark import pipelines as dp

@dp.table
def mv_dim_word():
  return spark.sql(f"""

SELECT
  word_jp
  ,reading_hiragana_jp
  ,meaning_en
  ,difficulty_level
FROM vw_vocabulary_full

""")
