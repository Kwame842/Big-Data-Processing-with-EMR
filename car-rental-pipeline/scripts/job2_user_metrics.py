# job2_user_metrics.py

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, sum, count, avg, max, min, to_date, to_timestamp, unix_timestamp
import sys
import logging

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UserTransactionMetrics")

# ----------------------------
# Argument parsing
# ----------------------------
if len(sys.argv) != 3:
    print("Usage: spark-submit job2_user_metrics.py <input_path> <output_path>")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]


# ----------------------------
# Spark session
# ----------------------------
spark = SparkSession.builder.appName("UserTransactionMetrics").getOrCreate()


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

user_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("phone_number", StringType(), True),
    StructField("driver_license_number", StringType(), True),
    StructField("driver_license_expiry", StringType(), True),
    StructField("creation_date", StringType(), True),
    StructField("is_active", IntegerType(), True),
])



# ----------------------------
# Read data
# ----------------------------
try:
    logger.info("Reading datasets...")
    transactions = spark.read.csv(f"{input_path}/rental_transactions.csv", header=True, schema=rental_schema)
    users = spark.read.csv(f"{input_path}/users.csv", header=True, schema=user_schema)

    logger.info("Parsing timestamps and computing rental hours...")
    transactions = transactions \
        .withColumn("rental_start_time", to_timestamp("rental_start_time", "dd/MM/yyyy HH:mm")) \
        .withColumn("rental_end_time", to_timestamp("rental_end_time", "dd/MM/yyyy HH:mm")) \
        .withColumn("rental_date", to_date("rental_start_time")) \
        .withColumn("rental_hours", (unix_timestamp("rental_end_time") - unix_timestamp("rental_start_time")) / 3600)

    logger.info("Joining with user data...")
    df = transactions.join(users, "user_id", "left")

    logger.info("Computing daily metrics...")
    daily_metrics = df.groupBy("rental_date").agg(
        count("rental_id").alias("total_transactions"),
        sum("total_amount").alias("daily_revenue")
    )

    logger.info("Computing user-specific metrics...")
    user_metrics = df.groupBy("user_id", "first_name", "last_name").agg(
        count("rental_id").alias("total_transactions"),
        sum("total_amount").alias("total_spent"),
        avg("total_amount").alias("avg_transaction_value"),
        max("total_amount").alias("max_transaction"),
        min("total_amount").alias("min_transaction"),
        sum("rental_hours").alias("total_rental_hours")
    )

    logger.info("Writing metrics to S3...")
    daily_metrics.write.mode("overwrite").parquet(f"{output_path}/daily_metrics/")
    user_metrics.write.mode("overwrite").parquet(f"{output_path}/user_metrics/")

    logger.info("User transaction job completed successfully!")

except Exception as e:
    logger.error(f"Job failed: {str(e)}")
    raise

finally:
    spark.stop()
