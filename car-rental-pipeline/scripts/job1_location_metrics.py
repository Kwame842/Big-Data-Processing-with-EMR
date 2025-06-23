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
