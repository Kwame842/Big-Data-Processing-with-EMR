# job1_location_metrics.py

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, sum, countDistinct, avg, max, min, to_timestamp, unix_timestamp
import sys
import logging
