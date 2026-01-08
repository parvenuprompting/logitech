# Operations Runbook - LogiTech Fleet Platform

**Version:** 1.0
**Last Updated:** 2026-01-08

---

## 1. System Overview
Het LogiTech Fleet Platform verwerkt real-time telemetrie van vrachtwagens.
*   **Critical Path:** Event Hub -> Silver (Streaming) -> Alerts (Cosmos DB).
*   **Analytics Path:** Silver -> Gold (dbt Batch) -> Power BI.

## 2. Incident Management

### Alert: High End-to-End Latency (>10s)
*   **Symptoom:** Dashboard update traag, alerts komen laat binnen.
*   **Triage:**
    1.  Check `monitoring.latency_metrics` query in Databricks SQL.
    2.  Check Event Hub Lag (Azure Portal metrics).
    3.  Check Spark Streaming UI (Micro-batch duration > Trigger interval?).
*   **Mitigatie:**
    *   *Scale Up:* Verhoog `max_workers` in cluster policy of zet `NUM_PARTITIONS` hoger in Event Hub (vereist herdeploy).
    *   *Backpressure:* Als input > processing, zal Spark automatisch throttlen (`maxOffsetsPerTrigger`).

### Alert: "Alert Storm" (Veel alerts van 1 voertuig)
*   **Symptoom:** Duizenden emails/Slack berichten.
*   **Oorzaak:** Defecte sensor of bug in logica.
*   **Mitigatie:**
    1.  Check `monitoring.dlq_analysis` query.
    2.  **Kill Switch:** Voeg `vehicle_id` toe aan `config.kill_switch_active_vehicles` tabel.
        ```sql
        INSERT INTO config.kill_switch_active_vehicles VALUES ('TRUCK_123', current_timestamp())
        ```
    3.  De Streaming job herlaadt deze config elke 5 min (of bij restart).

## 3. Deployment Procedures

### Hotfix Deployment (Silver Streaming Job)
1.  Maak branch `hotfix/xxx`.
2.  Pas code aan in `databricks/silver/`.
3.  Commit & Push -> CI checkt syntax/tests.
4.  **Stop** de draaiende Streaming Job in Databricks Workflows (Graceful Cancel).
5.  Deploy nieuwe code (via CI/CD of handmatig uploaden).
6.  Start Job. *Let op:* Check of Checkpoints compatibel zijn. Bij twijfel: nieuwe checkpoint directory (replay Bronze data indien nodig).

### dbt Model Update (Gold Layer)
1.  Pas `.sql` model aan.
2.  Run lokaal: `dbt run --select my_model`.
3.  Commit/Push -> CI draait `dbt test`.
4.  Merge naar Main.
5.  Productie Job (Databricks Workflow) pikt changes op bij volgende run.

## 4. Disaster Recovery (DR)

### Corruption in Silver Table
Als `silver.trip_events` corrupt is:
1.  **Stop** downstream jobs (Gold/Enrichment).
2.  **Tijdreis herstel:**
    ```sql
    RESTORE TABLE silver.trip_events TO TIMESTAMP AS OF '2026-01-08T10:00:00'
    ```
3.  Als restore niet mogelijk is:
    *   Delete corrupte records `DELETE FROM ... WHERE ...`.
    *   **Replay:** Start Streaming Job met optie `startingOffsets: "earliest"` en een **nieuwe checkpoint location** om data opnieuw uit Bronze te verwerken (De-duplication logica moet robuust zijn).

## 5. Contact List
*   **Data Engineering:** data-platform@logitech.com
*   **DevOps:** ops@logitech.com
*   **Product Owner:** po@logitech.com
