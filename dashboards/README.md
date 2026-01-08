# Power BI Setup Guide

Dit document beschrijft hoe je Power BI verbindt met het LogiTech Fleet Platform (Databricks Gold Layer) om de vereiste dashboards te bouwen.

## 1. Verbinding Maken

1.  Open Power BI Desktop.
2.  Kies **Get Data** -> **More...** -> **Azure Databricks**.
3.  Vul de connectiegegevens in (te vinden in Databricks Workspace -> Compute -> Advanced -> JDBC/ODBC):
    *   **Server Hostname**: `adb-xxxxxxxxx.azuredatabricks.net`
    *   **HTTP Path**: `sql/protocolv1/o/xxxxxxxx/xxxx`
4.  Kies **DirectQuery** modus (belangrijk voor realtime/near-realtime).
5.  Selecteer in de Navigator de database: `gold`.

## 2. Dashboards Bouwen

### A. Fleet Overview Dashboard (Realtime)
**Doel**: Operationeel inzicht in de huidige status van de vloot.

*   **Bron Tabel**: `dim_vehicles`
*   **Visualisaties**:
    *   **Kaart**: `current_latitude`, `current_longitude` (Kleur: `latest_status`).
    *   **KPI Cards**:
        *   Totaal Aantal Voertuigen.
        *   Aantal Actief (`latest_status = 'moving'`).
        *   Aantal Alerts (Join met `stg_alerts` indien nodig).
    *   **Filters**: Regio, Status.

### B. Trip Analytics Dashboard (Historisch)
**Doel**: Trendanalyse en diepgravende ritanalyses.

*   **Bron Tabel**: `fct_trip_analysis`
*   **Relatie**: Koppel `fct_trip_analysis` aan `dim_vehicles` op `vehicle_id`.
*   **Visualisaties**:
    *   **Line Chart**: Gemiddelde snelheid per uur van de dag.
    *   **Bar Chart**: Totaal kilometers per dag.
    *   **Heatmap**: Hotspots van events (`latitude`, `longitude`).
    *   **Scatter Plot**: Brandstofverbruik vs. Snelheid.

### C. Compliance & Cost Dashboard
**Doel**: GDPR compliance check en kosteninzicht.

*   **Bron Tabel**: `monitoring.cost_dashboard` (Custom SQL Query) en `fct_daily_fleet_summary`.
*   **Visualisaties**:
    *   **Line Chart**: Dagelijkse kosten (DBU consumption).
    *   **Gauge**: Budget verbruik vs. Limiet.
    *   **Table**: Lijst van jobs met de hoogste kosten.

## 3. SQL Queries voor Power BI Modellen

Indien je geen directe tabeltoegang wilt gebruiken, kun je deze SQL queries gebruiken als bron:

**Fleet State:**
```sql
SELECT * FROM gold.dim_vehicles WHERE last_seen_at > date_sub(current_timestamp(), 1)
```

**Trip KPI's:**
```sql
SELECT 
    date_day,
    sum(total_distance_km) as total_km,
    avg(avg_speed_kmh) as avg_speed
FROM gold.fct_daily_fleet_summary
GROUP BY 1
ORDER BY 1 DESC
```
