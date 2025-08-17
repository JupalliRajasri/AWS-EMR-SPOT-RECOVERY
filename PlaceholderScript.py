from pyspark.sql import SparkSession


appName = "sr_placeholder"
spark = SparkSession.builder.appName(appName).getOrCreate()

print("Placeholder code for dummy steps")