# User Training Guide - LogiTech Fleet Platform

## 1. Accessing the Platform
*   **Dashboards:** [Link to Power BI Workspace]
*   **Data Explorer:** [Link to Databricks SQL Warehouse]

## 2. Using the Fleet Overview Dashboard
*   **Map View:** Shows real-time location. Colors indicate status (Green=Moving, Red=Idle/Stopped).
*   **Filters:** Use the right-side panel to filter by Region or Vehicle Type.
*   **Drill-down:** Right-click a vehicle -> "Drill through" -> "Vehicle Details" for historical trips.

## 3. Reporting Issues
*   **Data Incorrect?** Check the "Last Updated" timestamp. If >15 mins old, report to #data-platform.
*   **Missing Vehicles?** Check if vehicle is active in source system (ERP).

## 4. Self-Service SQL
*   Use the `gold` schema for ad-hoc queries.
*   **Example:** "Show me total distance per truck last week"
    ```sql
    SELECT vehicle_id, sum(distance_km) 
    FROM gold.fct_trip_analysis 
    WHERE start_time > date_sub(current_date(), 7)
    GROUP BY 1
    ```
