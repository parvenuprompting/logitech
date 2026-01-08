# Performance Validation Plan

## 1. Throughput Test (5.000 events/sec)
**Tool:** `tools/load_generator/simulate_events.py`
**Config:**
```bash
export NUM_VEHICLES=1000
export EVENTS_PER_SEC=5000
```
**Monitor:**
1.  View **Event Hub Metrics** (Incoming Requests).
2.  View **Databricks Spark UI** (Input Rate vs Processing Rate).
3.  **Pass Criteria:** Processing Rate >= 5000 records/sec sustained for 10 mins.

## 2. Latency Test (P95 < 10s)
**Tool:** `monitoring/latency_metrics.sql`
**Monitor:**
1.  Run the SQL query in Databricks SQL.
2.  **Pass Criteria:** `p95_latency_sec` column stays below 10.

## 3. Failover Scenario
**Test:** Kill Driver Node.
1.  Manually restart the Driver from Spark UI / Cloud Console.
2.  **Expectation:** Job recovers automatically within < 2 mins via Checkpointing.
3.  **Verify:** No data loss (Count(Bronze) == Count(Silver)).

## 4. Rollback Plan
See `docs/operations/rollback_strategy.md` (To be created if not exists).
