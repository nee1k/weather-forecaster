from pyspark.sql import SparkSession
from pyspark.sql.functions import col, pandas_udf, PandasUDFType
from fbprophet import Prophet
import pandas as pd

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Prophet Forecasting") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,org.postgresql:postgresql:42.2.20") \
    .getOrCreate()

# PostgreSQL connection properties
url = "jdbc:postgresql://hostname:port/dbname"
properties = {
    "user": "username",
    "password": "password",
    "driver": "org.postgresql.Driver"
}

# Load data from PostgreSQL
df = spark.read.jdbc(url=url, table="timeseries_table", properties=properties)

# Rename columns for Prophet compatibility
df = df.select(
    col("date_column").alias("ds"),
    col("value_column").alias("y")
)

# Define the Pandas UDF for Prophet forecasting
@pandas_udf("ds timestamp, yhat float", PandasUDFType.GROUPED_MAP)
def forecast_prophet(pdf):
    model = Prophet()
    model.fit(pdf)
    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']]

# Apply the UDF
results = df.groupby("grouping_column").apply(forecast_prophet)

# Collect and use results
# results.show()  # Uncomment this line to display results in the Spark output

# Close Spark session
spark.stop()