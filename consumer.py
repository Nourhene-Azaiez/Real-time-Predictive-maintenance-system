from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os


# Define the schema for the Kafka messages
schema = StructType([
    StructField("UDI", IntegerType()),
    StructField("Product ID", StringType()),
    StructField("Type", StringType()),
    StructField("Air temperature [K]", DoubleType()),
    StructField("Process temperature [K]", DoubleType()),
    StructField("Rotational speed [rpm]", DoubleType()), 
    StructField("Torque [Nm]", DoubleType()),
    StructField("Tool wear [min]", IntegerType()),
    StructField("Target", IntegerType()), 
])

if __name__ == "__main__":
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("KafkaStreamToElasticsearch") \
        .getOrCreate()

    # Define Kafka parameters
    kafka_params = {
        "kafka.bootstrap.servers": "localhost:9092",
        "subscribe": "machineindus",
        "failOnDataLoss":"false",
    }

    # Read data from Kafka topic as a DataFrame
    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .options(**kafka_params) \
        .load()

    # Convert the value column (containing JSON data) to a string and parse JSON
    kafka_df = kafka_df \
        .withColumn("value", col("value").cast("string")) \
        .withColumn("value_json", from_json(col("value"), schema)) \
        .select("value_json.*")
    
    checkpoint_location = os.path.join(os.getcwd(), "checkpoint_location")

    # Write the DataFrame to Elasticsearch
    query = kafka_df \
        .writeStream \
        .format("org.elasticsearch.spark.sql") \
        .outputMode("append") \
        .option("es.mapping.id", "UDI") \
        .option("es.nodes", "localhost") \
        .option("es.port", "9200") \
        .option("es.nodes.wan.only", "true") \
        .option("checkpointLocation", checkpoint_location) \
        .option("es.resource", "indus") \
        .start()

    # Wait for the termination of the query
    query.awaitTermination()
