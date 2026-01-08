-- Init Script voor Alert Feature Flags
-- Run once to setup configuration table

CREATE SCHEMA IF NOT EXISTS config;

CREATE TABLE IF NOT EXISTS config.alert_feature_flags (
  alert_type STRING,
  enabled BOOLEAN,
  canary_vehicle_ids ARRAY<STRING>,
  max_alerts_per_minute INT,
  updated_at TIMESTAMP
) USING DELTA;

-- Seed initial config
MERGE INTO config.alert_feature_flags AS target
USING (
  SELECT 
    'idle_detection' as alert_type, 
    true as enabled, 
    array("TRUCK_001", "TRUCK_002") as canary_vehicle_ids, 
    100 as max_alerts_per_minute,
    current_timestamp() as updated_at
  UNION ALL
  SELECT 
    'route_deviation', 
    false, -- Disabled by default
    array() as canary_vehicle_ids, 
    50,
    current_timestamp()
  UNION ALL
  SELECT 
    'geofence_breach', 
    false, -- Disabled by default (safe rollout)
    array("TRUCK_005"), 
    200,
    current_timestamp()
) AS source
ON target.alert_type = source.alert_type
WHEN NOT MATCHED THEN INSERT *;
