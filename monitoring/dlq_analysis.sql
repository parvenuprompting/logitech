-- Alert Dead Letter Queue Analysis
-- Monitor rate limiting effectiveness and potential alert storms

-- 1. Recent DLQ Volume
SELECT 
  window(dlq_ingest_time, "5 minutes") as time_window,
  alert_type,
  failure_reason,
  count(*) as blocked_alert_count
FROM monitoring.alert_dead_letter_queue
WHERE dlq_ingest_time > current_timestamp() - INTERVAL 1 HOUR
GROUP BY time_window, alert_type, failure_reason
ORDER BY time_window DESC;

-- 2. Top Offending Vehicles (Noise Makers)
SELECT 
  vehicle_id,
  count(*) as blocked_count
FROM monitoring.alert_dead_letter_queue
WHERE dlq_ingest_time > current_timestamp() - INTERVAL 24 HOURS
GROUP BY vehicle_id
ORDER BY blocked_count DESC
LIMIT 10;

-- 3. Alert Storm Detection
-- Trigger Alert if DLQ ingest rate > 1000/min
/*
  SELECT count(*) FROM monitoring.alert_dead_letter_queue 
  WHERE dlq_ingest_time > current_timestamp() - INTERVAL 1 MINUTE
  HAVING count(*) > 1000
*/
