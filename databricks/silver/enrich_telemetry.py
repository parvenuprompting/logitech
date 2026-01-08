# Databricks Notebook source
# MAGIC %md
# MAGIC # Silver: Enrichment
# MAGIC 
# MAGIC **Doel**: Verrijk gevalideerde trip data met:
# MAGIC 1. Weerdata (API / Lookup)
# MAGIC 2. Geografische context (Regio/Snelweg)
# MAGIC 3. Voertuig Master Data (Type, Fuel capacity)
# MAGIC 
# MAGIC Uses **Versioned Logic Framework** for safe evolution.

# COMMAND ----------

from pyspark.sql.functions import *
import json

# Config
SOURCE_TABLE = "silver.trip_events"
TARGET_TABLE = "silver.enriched_trip_events"
CHECKPOINT_PATH = "/mnt/datalake/checkpoints/silver_enrichment"

# Helper to get active version config
def get_logic_config(feature_name):
    try:
        row = spark.read.table("config.silver_feature_versions") \
            .filter(f"feature_name = '{feature_name}' AND is_active = true") \
            .orderBy(col("valid_from").desc()) \
            .first()
        return row
    except:
        return None

# COMMAND ----------


def enrich_batch(df, epoch_id):
    # 1. Weather Enrichment via Broadcast Join (Best Practice)
    # Avoid UDFs for external lookups. Join with a pre-loaded/cached dataset.
    
    # Mock Weather Dataset (In prod: spark.table("gold.weather_grid"))
    weather_data = [
        (52, 4, "Rainy"),
        (52, 5, "Cloudy"),
        (51, 4, "Sunny"),
        (51, 5, "Stormy")
    ]
    weather_schema = ["grid_lat", "grid_lon", "weather_lookup"]
    weather_df = spark.createDataFrame(weather_data, weather_schema)
    
    # Join Logic: Round coordinates to join with grid
    # Using broadcast() for efficiency as weather reference data is small relative to telemetry
    df_prepared = df.withColumn("grid_lat", round(col("latitude"), 0).cast("long")) \
                    .withColumn("grid_lon", round(col("longitude"), 0).cast("long"))
    
    enriched = df_prepared.join(broadcast(weather_df), ["grid_lat", "grid_lon"], "left") \
        .withColumn("weather_condition", coalesce(col("weather_lookup"), lit("Unknown"))) \
        .drop("grid_lat", "grid_lon", "weather_lookup") \
        .withColumn("region", lit("EU-West")) # Placeholder for Geo-lookup
    
    # 3. Write
    enriched.write \
        .format("delta") \
        .mode("append") \
        .option("mergeSchema", "true") \
        .saveAsTable(TARGET_TABLE)

# COMMAND ----------

spark.readStream \
    .format("delta") \
    .table(SOURCE_TABLE) \
    .writeStream \
    .foreachBatch(enrich_batch) \
    .option("checkpointLocation", CHECKPOINT_PATH) \
    .start()
