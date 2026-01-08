# Databricks Notebook source
# MAGIC %md
# MAGIC # Real-time Route Deviation Detection
# MAGIC 
# MAGIC Detecteert voertuigen die van hun geplande route afwijken.
# MAGIC 
# MAGIC **Logic (Simplified for PoC):**
# MAGIC - Join stream met static "Planned Routes" table
# MAGIC - Bereken afstand tussen actuele positie en dichtstbijzijnde route-segment
# MAGIC - Als afstand > threshold (bijv. 500m) -> Alert

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# Config
MESSAGE_TYPE = "position"
ALERT_TYPE = "route_deviation"
BRONZE_TABLE = "bronze.telemetry"
CHECKPOINT_PATH = "/mnt/datalake/checkpoints/detect_route_deviation"

# Feature Flag & Helper Logic (Duplicate code? In prod use shared lib)
def get_feature_config(spark, alert_type):
    try:
        row = spark.read.table("config.alert_feature_flags") \
            .filter(col("alert_type") == alert_type) \
            .select("enabled", "canary_vehicle_ids", "max_alerts_per_minute") \
            .first()
        return row
    except:
        return None

def process_batch(df, epoch_id):
    config = get_feature_config(spark, ALERT_TYPE)
    
    if not config or not config.enabled:
        print(f"Alert {ALERT_TYPE} is DISABLED. Skipping.")
        return

    # Canary Filtering
    canary_list = config.canary_vehicle_ids
    if canary_list and len(canary_list) > 0 and "ALL" not in canary_list:
        df = df.filter(col("vehicle_id").isin(canary_list))
        
    # Biz Logic: Deviation
    # Mock implementation: Filter if 'deviation_meters' field exists and > 500
    # In reality: Spatial Join needed (Hard in pure Spark Struct Streaming without commercial add-ons or H3 lib)
    # PoC Proxy: We assume payload contains 'distance_to_route' calculated by edge/ingest or we simplistic filter.
    
    # Let's assume payload has latitude/longitude. 
    # Mocking deviation logic: validatie op 'route_id' aanwezigheid en random threshold sim.
    # PROD: H3 index join with route-path cells.
    
    alerts = df.select(
            col("vehicle_id"),
            current_timestamp().alias("alert_timestamp"),
            lit(ALERT_TYPE).alias("alert_type"),
            lit("Vehicle deviated from route > 500m").alias("message"),
            col("timestamp").alias("detection_time")
        ).filter("1=0") # Placeholder: No actual logic implemented yet without GIS lib
        
    # ... Write logic same as idle detection (DLQ, Cosmos, Delta) ...
    # Omitted for brevity in this file, mimicking structure.

# COMMAND ----------

stream = spark.readStream \
    .format("delta") \
    .table(BRONZE_TABLE) \
    .writeStream \
    .foreachBatch(process_batch) \
    .option("checkpointLocation", CHECKPOINT_PATH) \
    .trigger(processingTime='30 seconds') \
    .start()
