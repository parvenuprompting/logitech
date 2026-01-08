# Incident Response Playbook

**Severity Levels:**
- **SEV-1 (Critical):** Data loss, Security Breach, Complete Outage. ETA < 1h.
- **SEV-2 (High):** Latency > 1min, Partial Data Loss. ETA < 4h.
- **SEV-3 (Medium):** Non-critical bug, Dashboard delay. ETA < 24h.

## Scenarios

### 1. High Latency (>10s)
**Trigger:** Azure Monitor Alert 'HighLatency'.
**Steps:**
1.  **Ack:** Acknowledge PagerDuty alert.
2.  **Verify:** Check `monitoring.latency_metrics` query. Is it ingestion lag or processing lag?
3.  **Ingestion:** If Event Hub ingress > egress -> Scale Up Spark Cluster.
4.  **Processing:** Check Logic Apps / Functions. Restart if stuck.
5.  **Resolution:** Update status page.

### 2. Data Quality Issue (Corrupt Data)
**Trigger:** `dbt test` failure or User Report.
**Steps:**
1.  **Identify:** Query `silver.trip_events` for invalid records.
2.  **Isolate:** Stop Enrichment job to prevent bad data propagation.
3.  **Fix:** Update `validation_deduplicate.py` logic.
4.  **Recover:** Run `tools/repair/replay_data.py` (conceptual) or restore Delta Table.

### 3. Security Breach (Public Access)
**Trigger:** Azure Security Center Alert.
**Steps:**
1.  **Contain:** Rotate Access Keys immediately.
2.  **Block:** IP Whitelist restriction via Azure Networking.
3.  **Audit:** Check `system.access.audit` logs for unauthorized reads.
