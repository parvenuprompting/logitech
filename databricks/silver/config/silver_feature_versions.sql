-- Silver Layer Versioning Configuration
-- Enables A/B testing and phased rollouts for business logic (transformations)

CREATE TABLE IF NOT EXISTS config.silver_feature_versions (
  feature_name STRING,         -- e.g. "trip_distance_calculation"
  version STRING,              -- e.g. "v1.0", "v2.1-beta"
  is_active BOOLEAN,           -- Active for general use?
  parameters_json STRING,      -- Config params e.g. {"threshold": 500}
  target_audience STRING,      -- "ALL", "CANARY", "DEV"
  valid_from TIMESTAMP,
  valid_to TIMESTAMP
) USING DELTA;

-- Seed Data (Example)
INSERT INTO config.silver_feature_versions VALUES 
('idle_detection_threshold', 'v1.0', true, '{"min_duration_minutes": 5}', 'ALL', current_timestamp(), null),
('idle_detection_threshold', 'v2.0-beta', false, '{"min_duration_minutes": 3}', 'CANARY', current_timestamp(), null);
