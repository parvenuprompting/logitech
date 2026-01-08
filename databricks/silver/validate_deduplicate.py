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
import sys
import os

# Add current directory to path to import local modules (for standard python execution)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from schema_loader import load_schema_from_json
except ImportError:
    # Fallback for Databricks Notebook execution where files are in same dir but need help
    # Or assuming the user will handle the library installation. 
    # For now, we assume schema_loader is available.
    pass

# Config
BRONZE_TABLE = "bronze.telemetry"
SILVER_TABLE = "silver.trip_events"
CHECKPOINT_PATH = "/mnt/datalake/checkpoints/silver_validate_dedup"
# Adjust path relative to this script: ../schema_validation/schemas/telemetry_event_v1.0.0.json
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schema_validation/schemas/telemetry_event_v1.0.0.json")

# Load Target Schema
try:
    silver_schema = load_schema_from_json(SCHEMA_PATH)
except Exception as e:
    print(f"Error loading schema from {SCHEMA_PATH}: {e}")
    # Fallback or exit? Raising error is safer to enforce governance.
    raise e

# COMMAND ----------

def process_bronze_batch(df, epoch_id):
    # 1. Deduplicatie moved to Stream Definition (see below) to use Watermark & State Store
    
    # 2. Parse Payload
    # Extract fields from raw_json
    parsed = df.withColumn("data", from_json(col("raw_payload"), silver_schema)) \
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

    # 4. Write to Silver
    validated.write \
        .format("delta") \
        .mode("append") \
        .saveAsTable(SILVER_TABLE)

# COMMAND ----------

# Stream from Bronze
# Added withWatermark and dropDuplicates here to fix Memory Leak risk (Stateful Deduplication)
stream = spark.readStream \
    .format("delta") \
    .table(BRONZE_TABLE) \
    .withWatermark("timestamp", "10 minutes") \
    .dropDuplicates(["vehicle_id", "timestamp"]) \
    .writeStream \
    .foreachBatch(process_bronze_batch) \
    .option("checkpointLocation", CHECKPOINT_PATH) \
    .trigger(availableNow=True) \
    .start()
