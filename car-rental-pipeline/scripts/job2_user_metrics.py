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