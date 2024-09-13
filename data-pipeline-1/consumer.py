from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DecimalType
import os

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Kafka to PostgreSQL") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.postgresql:postgresql:42.2.20") \
    .getOrCreate()

# Define Kafka parameters
kafka_topic_name = "weather_data"
kafka_bootstrap_servers = "localhost:9092"

# Read data from Kafka
df = spark.read.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic_name) \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Define the schema for the JSON data
schema = StructType([
    StructField("Timestamp", StringType(), True),
    StructField("Temperature", StringType(), True),
    StructField("Direct Horizontal Radiation", StringType(), True),
    StructField("Diffuse Horizontal Radiation", StringType(), True)
])

# Parse JSON data and select columns, casting them to the desired types and renaming them
df = df.withColumn("jsonData", from_json("value", schema)) \
    .select(
        col("jsonData.Timestamp").cast("timestamp").alias("timestamp"),
        col("jsonData.Temperature").cast("decimal(10, 4)").alias("temperature"),
        col("jsonData.Direct Horizontal Radiation").cast("decimal(10, 4)").alias("direct_horizontal_radiation"),
        col("jsonData.Diffuse Horizontal Radiation").cast("decimal(10, 4)").alias("diffuse_horizontal_radiation")
    )

# Print schema to verify the structure and data types
df.printSchema()
df.show(truncate=False)

# Define PostgreSQL connection properties
url = "jdbc:postgresql://149.165.170.140:5432/postgres"
properties = {
    "user": os.getenv('DB_USER', 'airflow'),
    "password": os.getenv('DB_PASSWORD', 'airflow'),
    "driver": "org.postgresql.Driver",
    "dbtable": "austria_weather_data"
}

# Write data to PostgreSQL
try:
    df.write.format("jdbc").option("url", url).options(**properties).mode("append").save()
except Exception as e:
    print(f"Error writing to PostgreSQL: {e}")

# Stop the Spark session
spark.stop()