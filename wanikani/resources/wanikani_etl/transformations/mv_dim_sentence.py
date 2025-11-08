from pyspark import pipelines as dp

@dp.table
def mv_dim_sentence():
    return spark.sql(r"""

SELECT
  word_jp
  ,TRIM(REGEXP_REPLACE(sentence_jp_and_en, r'\s*\(.*\)$', '')) AS sentence_jp
  ,TRIM(REGEXP_EXTRACT(sentence_jp_and_en, r'\(([^)]*)\)', 1)) AS sentence_en

FROM vw_vocabulary_full
LATERAL VIEW EXPLODE(SPLIT(csv_sentences_jp_and_en, '\n')) AS sentence_jp_and_en
WHERE csv_sentences_jp_and_en IS NOT NULL AND csv_sentences_jp_and_en != ''

""")
