from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split

spark = SparkSession.builder \
    .appName("Read Parquet File") \
    .config("spark.sql.parquet.compression.codec", "zstd") \
    .getOrCreate()
    

parquet_file_path = "flights-1m.parquet"

df = spark.read.parquet(parquet_file_path)

# 1. Transformation Map : Convertir chaque colonne en un tableau de mots
# Pour chaque colonne, on va splitter les valeurs en mots
columns_words_df = []
for c in df.columns:
    columns_words_df.append(
        df.select(explode(split(col(c), r"\s+")).alias("word"))
    )

# 2. Union de tous les DataFrames de mots dans un seul
all_words_df = columns_words_df[0]
for col_df in columns_words_df[1:]:
    all_words_df = all_words_df.union(col_df)

# 3. Compter les occurrences de chaque mot
word_counts = all_words_df.groupBy("word").count().orderBy("count", ascending=False)

# Afficher les résultats
word_counts.show(20, truncate=False)

# Arrêter la session Spark
spark.stop()