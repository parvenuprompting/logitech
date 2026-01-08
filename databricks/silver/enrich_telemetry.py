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

# Mock Weather UDFs
def get_weather_v1(lat, lon, time):
    return "Sunny" # Placeholder

def get_weather_v2_api(lat, lon, time):
    # Call to external API (e.g. OpenWeatherMap)
    # Rate limited! In prod usage: Batch lookup or join with ingested weather dataset.
    return "Rainy" # Mock

get_weather_udf = udf(get_weather_v1) # Default to v1

# COMMAND ----------

def enrich_batch(df, epoch_id):
    # 1. Check Feature Version for Weather
    weather_config = get_logic_config("weather_enrichment")
    
    # Dynamic Logic Selection
    if weather_config and weather_config.version.startswith("v2"):
        # Use V2 logic (e.g. API based)
        weather_expr = lit("Rainy (V2)") 
    else:
        # Use V1 logic (Static/Mock)
        weather_expr = lit("Sunny (V1)")
        
    # 2. Enrich
    # Join with Vehicle Dimension (Broadcast)
    # Assuming silver.vehicles exists (if not, we mock it or left join fails gracefully)
    # vehicles = spark.table("silver.vehicles")
    
    enriched = df.withColumn("weather_condition", weather_expr) \
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
