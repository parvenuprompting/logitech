-- Databricks Cost Analysis Dashboard Query
-- Requires: System Tables enabled (system.billing.usage)

-- 1. Daily Cost Trend per SKU
SELECT 
  usage_date,
  sku_name,
  SUM(usage_quantity) as dbu_consumed,
  SUM(usage_quantity * list_price) as estimated_cost_usd
FROM system.billing.usage
WHERE usage_date >= date_sub(current_date(), 30)
GROUP BY 1, 2
ORDER BY 1 DESC;

-- 2. Cost per Job (Identify expensive jobs)
SELECT 
  usage_metadata.job_id as job_id,
  -- Note: specific metadata fields depend on cloud provider/schema version
  -- usage_metadata.job_name as job_name, 
  SUM(usage_quantity * list_price) as total_cost_last_30d
FROM system.billing.usage
WHERE usage_date >= date_sub(current_date(), 30)
  AND usage_metadata.job_id IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

-- 3. Budget Burn Rate
WITH monthly_spend AS (
  SELECT SUM(usage_quantity * list_price) as current_spend
  FROM system.billing.usage
  WHERE month(usage_date) = month(current_date())
)
SELECT 
  current_spend,
  2000 as dev_budget_limit, -- Example budget
  (current_spend / 2000) * 100 as burn_percent
FROM monthly_spend;
