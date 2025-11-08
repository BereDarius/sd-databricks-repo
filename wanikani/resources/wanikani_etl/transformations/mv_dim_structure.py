from pyspark import pipelines as dp

@dp.table
def mv_dim_structure():
  return spark.sql(f"""

SELECT DISTINCT trim(element) AS name
FROM vw_vocabulary_full
LATERAL VIEW explode(split(csv_structures, ',')) AS element

""")
