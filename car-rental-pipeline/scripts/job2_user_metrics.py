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