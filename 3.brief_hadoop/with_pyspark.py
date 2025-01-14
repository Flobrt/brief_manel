from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, count

# Créer une session Spark
spark = SparkSession.builder \
    .appName('WordCountWithDataFrame') \
    .getOrCreate()

# file_path = "input/prompts.csv"
# df = spark.read.text(file_path)

file_path = "input/prompts.csv"
df = spark.read.text(file_path)

# Transformation pour compter les mots
word_counts = (
    df
    .select(explode(split(col("value"), "\\s+")).alias("word"))  # Diviser les lignes en mots
    .groupBy("word")  # Grouper par mot
    .agg(count("*").alias("count"))  # Compter les occurrences
    .orderBy(col("count").desc())  # Trier par fréquence décroissante
)

# Afficher les résultats
word_counts.show()

# Arrêter la session Spark
spark.stop()

