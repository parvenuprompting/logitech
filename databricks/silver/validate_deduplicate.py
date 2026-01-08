# Databricks Notebook source
# MAGIC %md
# MAGIC # Silver: Validate & Deduplicate
# MAGIC 
# MAGIC **Doel**:
# MAGIC 1. Lees Bronze data (Raw JSON)
# MAGIC 2. Dedupliceer (Exactly-Once semantics herstellen indien nodig)
# MAGIC 3. Parse & Valideer structuur (Silver Schema)
# MAGIC 4. Schrijf naar Silver Delta Table

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

# Config
BRONZE_TABLE = "bronze.telemetry"
SILVER_TABLE = "silver.trip_events"
CHECKPOINT_PATH = "/mnt/datalake/checkpoints/silver_validate_dedup"
SCHEMA_PATH = "schemas/trip_event.json"

# Load Target Schema
with open(SCHEMA_PATH, 'r') as f:
    schema_json = json.load(f)
    # Convert JSON schema to Spark StructType (Simplified mapping)
    # In prod: use robust converter or schema registry fetch
    # Here: Manual definition matching json for robust parsing
    silver_schema = StructType([
        StructField("event_id", StringType(), False),
        StructField("vehicle_id", StringType(), False),
        StructField("timestamp", TimestampType(), False),
        StructField("event_type", StringType(), False),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("speed_kmh", DoubleType(), True),
        StructField("heading", DoubleType(), True),
        StructField("fuel_level_percent", DoubleType(), True),
        StructField("engine_temp_c", DoubleType(), True)
    ])

# COMMAND ----------

def process_bronze_batch(df, epoch_id):
    # 1. Deduplicatie
    # Bronze is append-only, duplicates possible due to at-least-once delivery.
    # We deduplicate on unique event_id within the micro-batch window.
    # For robust global dedup, we rely on Delta MERGE or watermark dropDuplicates in stream.
    # Hier: Start with simple dropDuplicates.
    
    deduped = df.dropDuplicates(["vehicle_id", "timestamp"]) # or event_id if reliable
    
    # 2. Parse Payload
    # Extract fields from raw_json
    parsed = deduped.withColumn("data", from_json(col("raw_payload"), silver_schema)) \
        .select(
            col("vehicle_id"), # From bronze partition/col
            col("timestamp"),
            col("data.event_id"),
            col("data.event_type"),
            col("data.latitude"),
            col("data.longitude"),
            col("data.speed_kmh"),
            col("data.heading"),
            col("data.fuel_level_percent"),
            col("data.engine_temp_c"),
            current_timestamp().alias("processed_at")
        )

    # 3. Validation Logic (Data Quality)
    # Flag invalid records instead of dropping
    validated = parsed.withColumn("is_valid", 
        (col("event_id").isNotNull()) & 
        (col("vehicle_id").isNotNull()) & 
        (col("timestamp").isNotNull())
    ).withColumn("validation_error",
        when(col("event_id").isNull(), "Missing event_id")
        .when(col("timestamp").isNull(), "Missing timestamp")
        .otherwise(None)
    )

    # 4. Write to Silver (Merge to handle late arriving duplicates if using MERGE strategy)
    # For high throughput, APPEND is better, handling dupes downstream or via unique constraint (not yet in Delta OSS fully).
    # We use APPEND here for speed.
    
    validated.write \
        .format("delta") \
        .mode("append") \
        .saveAsTable(SILVER_TABLE)

# COMMAND ----------

# Stream from Bronze
stream = spark.readStream \
    .format("delta") \
    .table(BRONZE_TABLE) \
    .writeStream \
    .foreachBatch(process_bronze_batch) \
    .option("checkpointLocation", CHECKPOINT_PATH) \
    .trigger(availableNow=True) # Batch mode triggering for Silver
    .start()
