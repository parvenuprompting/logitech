-- Dashboard Query: Real-time Latency (End-to-End)
-- Target: P95 < 10 seconds

SELECT 
  window(log_time, "5 minutes") as time_window,
  alert_type,
  AVG(avg_latency) as avg_latency_sec,
  MAX(p95_latency) as p95_latency_sec,
  MAX(max_latency) as max_latency_sec
FROM monitoring.latency_metrics
WHERE log_time > current_timestamp() - INTERVAL 1 HOUR
GROUP BY time_window, alert_type
ORDER BY time_window DESC;

-- Alert Rule (Azure Monitor / Databricks SQL Alert)
-- Trigger if P95 > 10s for 2 consecutive 5-min windows
/*
  SELECT p95_latency FROM monitoring.latency_metrics 
  ORDER BY log_time DESC LIMIT 1
  > 10
*/
