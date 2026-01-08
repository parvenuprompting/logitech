-- Cost Anomaly Detection
-- Detects days where cost is > 1.5x the 7-day moving average

WITH daily_cost AS (
    SELECT 
        usage_date,
        SUM(usage_quantity * list_price) as total_cost
    FROM system.billing.usage
    GROUP BY 1
),
moving_stats AS (
    SELECT
        usage_date,
        total_cost,
        AVG(total_cost) OVER (ORDER BY usage_date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) as avg_cost_7d,
        STDDEV(total_cost) OVER (ORDER BY usage_date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) as std_cost_7d
    FROM daily_cost
)
SELECT 
    *,
    (total_cost - avg_cost_7d) as excess_cost,
    CASE 
        WHEN total_cost > (avg_cost_7d * 1.5) THEN 'High Anomaly'
        WHEN total_cost > (avg_cost_7d * 1.2) THEN 'Medium Warning'
        ELSE 'Normal'
    END as status
FROM moving_stats
WHERE usage_date >= date_sub(current_date(), 30)
ORDER BY usage_date DESC;
