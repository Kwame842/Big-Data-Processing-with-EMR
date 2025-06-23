# job1_location_metrics.py

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, sum, countDistinct, avg, max, min, to_timestamp, unix_timestamp
import sys
import logging

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LocationVehicleMetrics")

# ----------------------------
# Argument parsing
# ----------------------------
if len(sys.argv) != 3:
    print("Usage: spark-submit job1_location_metrics.py <input_path> <output_path>")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

# ----------------------------
# Spark session
# ----------------------------
spark = SparkSession.builder.appName("LocationVehiclePerformance").getOrCreate()

# ----------------------------
# Define schemas
# ----------------------------
rental_schema = StructType([
    StructField("rental_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("vehicle_id", StringType(), True),
    StructField("rental_start_time", StringType(), True),
    StructField("rental_end_time", StringType(), True),
    StructField("pickup_location", StringType(), True),
    StructField("dropoff_location", StringType(), True),
    StructField("total_amount", DoubleType(), True),
])

# ----------------------------
# Read data
# ----------------------------
try:
    logger.info("Reading data from S3...")
    transactions = spark.read.csv(f"{input_path}/rental_transactions.csv", header=True, schema=rental_schema)
    vehicles = spark.read.csv(f"{input_path}/vehicles.csv", header=True, inferSchema=True)
    locations = spark.read.csv(f"{input_path}/locations.csv", header=True, inferSchema=True)

    logger.info("Parsing timestamp columns...")
    transactions = transactions \
        .withColumn("rental_start_time", to_timestamp("rental_start_time", "dd/MM/yyyy HH:mm")) \
        .withColumn("rental_end_time", to_timestamp("rental_end_time", "dd/MM/yyyy HH:mm"))

    logger.info("Joining datasets...")
    df = transactions.join(vehicles, "vehicle_id", "left") \
                     .join(locations.withColumnRenamed("location_id", "pickup_location"), "pickup_location", "left")

    logger.info("Calculating location metrics...")
    location_metrics = df.groupBy("pickup_location").agg(
        sum("total_amount").alias("total_revenue"),
        countDistinct("rental_id").alias("total_transactions"),
        avg("total_amount").alias("avg_transaction_amount"),
        max("total_amount").alias("max_transaction_amount"),
        min("total_amount").alias("min_transaction_amount"),
        countDistinct("vehicle_id").alias("unique_vehicles")
    )

    logger.info("Calculating vehicle metrics...")
    df = df.withColumn("rental_hours", (unix_timestamp("rental_end_time") - unix_timestamp("rental_start_time")) / 3600)

    vehicle_metrics = df.groupBy("vehicle_type").agg(
        avg("rental_hours").alias("avg_rental_hours"),
        sum("total_amount").alias("revenue_by_vehicle_type")
    )

    logger.info("Writing metrics to S3...")
    location_metrics.write.mode("overwrite").parquet(f"{output_path}/location_metrics/")
    vehicle_metrics.write.mode("overwrite").parquet(f"{output_path}/vehicle_metrics/")

    logger.info("Job completed successfully!")

except Exception as e:
    logger.error(f"Job failed: {str(e)}")
    raise

finally:
    spark.stop()
