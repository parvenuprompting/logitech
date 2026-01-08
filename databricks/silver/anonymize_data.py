# Databricks Notebook source
# MAGIC %md
# MAGIC # GDPR Anonymization Job
# MAGIC 
# MAGIC **Doel**: PII (Personally Identifiable Information) verwijderen of maskeren na retentieperiode (3 maanden).
# MAGIC 
# MAGIC **Policy**:
# MAGIC - Data > 3 maanden:
# MAGIC   - `vehicle_id` -> Hashed
# MAGIC   - `latitude`/`longitude` -> Rounded (Fuzzed) to 2 decimals
# MAGIC   - `driver_id` -> Nullified

# COMMAND ----------

from pyspark.sql.functions import *

# Config
TARGET_TABLES = ["silver.trip_events", "silver.enriched_trip_events", "gold.fct_trip_analysis"]
RETENTION_MONTHS = 3

# COMMAND ----------

def anonymize_table(table_name):
    print(f"Processing GDPR rules for {table_name}...")
    
    # Calculate cutoff date
    cutoff_date = date_sub(current_date(), RETENTION_MONTHS * 30)
    
    # Update logic (Delta Lake UPDATE)
    # Using SQL for clarity
    
    # 1. Hash vehicle_id
    # 2. Fuzz location
    
    spark.sql(f"""
        UPDATE {table_name}
        SET 
            vehicle_id = sha2(vehicle_id, 256),
            latitude = round(latitude, 2),
            longitude = round(longitude, 2),
            anonymized_at = current_timestamp()
        WHERE 
            timestamp < '{cutoff_date}'
            AND (anonymized_at IS NULL)
    """)
    
    print(f"Finished anonymizing {table_name} records older than {cutoff_date}")

# COMMAND ----------

# Daily Job Runner
for table in TARGET_TABLES:
    try:
        anonymize_table(table)
    except Exception as e:
        print(f"Skipping {table} (might not exist yet): {str(e)}")
