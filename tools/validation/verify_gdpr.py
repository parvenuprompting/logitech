import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sha2

def verify_gdpr(spark, table_name="silver.trip_events"):
    print(f"Verifying GDPR compliance for {table_name}...")
    
    df = spark.table(table_name)
    
    # Check 1: Old data must be anonymized
    # Assuming threshold is 90 days
    threshold_date = "date_sub(current_date(), 90)"
    
    old_data = df.filter(f"timestamp < {threshold_date}")
    
    # Check if vehicle_id looks like a SHA256 hash (64 hex chars)
    # Using a simple regex for demo purposes
    non_compliant_count = old_data.filter("vehicle_id NOT RLIKE '^[a-fA-F0-9]{64}$'").count()
    
    if non_compliant_count > 0:
        print(f"FAILED: Found {non_compliant_count} records older than 90 days with raw vehicle_ids.")
    else:
        print("PASSED: All historical records appear anonymized.")

    # Check 2: Geo fuzzing (decimals <= 2)
    # lat - round(lat, 2) should be 0 if rounded
    # This is a strict check, logic usually involves floor/ceil
    pass 

if __name__ == "__main__":
    spark = SparkSession.builder.appName("GDPR_Verify").getOrCreate()
    verify_gdpr(spark)
