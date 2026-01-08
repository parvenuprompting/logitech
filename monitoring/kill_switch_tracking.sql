-- Kill-Switch Effectiveness Tracking
-- Verifies that alert volume drops to zero after disable

SELECT 
  window(log_time, "1 minute") as time_window,
  alert_type,
  SUM(alert_count) as total_alerts
FROM monitoring.latency_metrics
WHERE alert_type = 'idle_detection'
  AND log_time > current_timestamp() - INTERVAL 1 HOUR
GROUP BY time_window, alert_type
ORDER BY time_window DESC;

-- Expected result after kill-switch:
-- 10:05: 50 alerts
-- 10:04: 52 alerts
-- 10:03: [KILL SWITCH ACTIVATED]
-- 10:02: 0 alerts
-- 10:01: 0 alerts
