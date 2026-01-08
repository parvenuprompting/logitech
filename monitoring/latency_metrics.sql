-- End-to-End Latency Breakdown
-- Analyzes the lag between Event Time, Ingestion Time, and Processing Time

WITH latency_data AS (
   SELECT 
     event_id,
     event_type,
     timestamp as event_time_gen,
     -- processing_time would be added by each layer. 
     -- Assuming we log these in a metrics table or extract from bronze/silver metadata
     processed_at as silver_processed_time,
     
     -- Calculate Lags
     (unix_timestamp(processed_at) - unix_timestamp(timestamp)) as e2e_latency_seconds
   FROM silver.enhanced_trip_events
   WHERE timestamp >= date_sub(current_timestamp(), 1) -- Last 24 hours
)

SELECT
  window(from_unixtime(unix_timestamp(silver_processed_time)), '5 minutes') as time_window,
  percentile_approx(e2e_latency_seconds, 0.50) as p50_latency_sec,
  percentile_approx(e2e_latency_seconds, 0.95) as p95_latency_sec,
  percentile_approx(e2e_latency_seconds, 0.99) as p99_latency_sec,
  max(e2e_latency_seconds) as max_latency_sec
FROM latency_data
GROUP BY 1
ORDER BY 1 DESC;
