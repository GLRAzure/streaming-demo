# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC Before running this notebook, you must create the library from this maven repo: azure-eventhubs-spark_2.11-2.3.6

# COMMAND ----------

#Import the python libraries we'll need.
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

#Retrieve the event hub connection and consumer group from the secrets.
#If you are not familiar with creating secret scopes backed by Azure Key Vault you can walk through https://docs.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes#--create-an-azure-key-vault-backed-secret-scope
event_hub_connection_string = dbutils.secrets.get("streamingdemo","eventhubsreader")
consumer_group = dbutils.secrets.get("streamingdemo","databricksconsumergroup")

#Specify the temp directory for storing the streaming data from the hub.  Note, Databricks will create it if it does not exist.
tempDir = "/dbfs/tmp/streamingTemp"

# COMMAND ----------

#Create some filters for the queries below.
dbutils.widgets.dropdown("City", "Pittsburgh", ["Pittsburgh", "Cleveland", "Rochester", "Detroit"])
dbutils.widgets.dropdown("Sensor", "temperature", ["temperature", "pressure", "humidity"])

city = getArgument("City")
sensor = getArgument("Sensor")

# COMMAND ----------

#Build the event hub connection configuration.
ehConf = {
  'eventhubs.connectionString' : event_hub_connection_string,
  'eventhubs.consumerGroup' : consumer_group
}

streamingInputDF = spark \
  .readStream \
  .format("eventhubs") \
  .options(**ehConf) \
  .load()

#Kafka equivalent
#streamingInputDF = spark.readStream
#  .format("kafka")
#  .option("kafka.bootstrap.servers", "YOUR.HOST:PORT1,YOUR.HOST:PORT2")   // comma separated list of broker:host
#  .option("subscribe", "YOUR_TOPIC1,YOUR_TOPIC2")    // comma separated list of topics
#  .option("startingOffsets", "latest") // read data from the end of the stream
#  .load()

# COMMAND ----------

#Read the input stream of data, and immediately write out to the temp directory in delta format.  Since the event hub stream is using a cursor, you cannot have multiple readers at the same time.  You will get an error eventually.
streamingInputDF.writeStream \
 .format("delta") \
 .option("checkpointLocation", tempDir + "/_checkpoint") \
 .queryName("streaming_query") \
 .outputMode("append") \
 .start(tempDir)

# COMMAND ----------

#Delta handles having multiple readers more elegantly.  Open up a stream from the temp directory where we wrote the data in delta format.
streamingData = spark.readStream \
    .format("delta") \
    .load(tempDir)

# COMMAND ----------

#Display the raw data.  Event hubs body comes in as binary, so we need to cast to a string so it's readable.
display(streamingData.withColumn("body", streamingData["body"].cast("string")))

# COMMAND ----------

#Now lets break apart the json payload so we can reference the actual values.
schema = StructType([
  StructField("city", StringType()),
  StructField("room", StringType()),
  StructField("sensor", StringType()), 
  StructField("value", DoubleType())
])

payloadDF = streamingData \
  .selectExpr("cast (body as STRING) jsonData", "enqueuedTime") \
  .select(from_json("jsonData", schema).alias("payload"), "enqueuedTime")\
  .select(col("payload.city"),col("payload.room"), col("payload.sensor"), col("payload.value"), col("enqueuedTime"))\

display(payloadDF)

# COMMAND ----------

#Do a filter on the data by city and sensor and show as a tabular view.
display(payloadDF.select("room", "value").where((col("payload.city") == city) & (col("payload.sensor") == sensor)))

# COMMAND ----------

#Run the same query, but this time have it plot as a line graph.
display(payloadDF.where((col("payload.city") == city) & (col("payload.sensor") == sensor)))

# COMMAND ----------

#Run the same query one more time, but display as a bar chart.
display(payloadDF.where((col("payload.city") == city) & (col("payload.sensor") == sensor)))

# COMMAND ----------

#Click on the "View:" and head over to the dashboard

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Don't forget to click the "Stop Execution" on the notebook so that the streams will be stopped!!