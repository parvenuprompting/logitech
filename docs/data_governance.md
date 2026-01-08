# Data Governance — LogiTech Fleet Platform

**Versie**: 1.0  
**Eigenaar**: Data Platform Team  
**Review**: Jaarlijks

## 1. Data Classificatie

### 1.1 Classificatie Niveaus

| Niveau | Definitie | Voorbeelden | Toegang |
|--------|-----------|-------------|---------|
| **Publiek** | Geen impact bij publicatie | Aggregaties zonder PII | Alle medewerkers |
| **Intern** | Bedrijfsvertrouwelijk | Ritstatistieken, vlootoverzicht | LogiTech medewerkers |
| **Confidentieel** | Privacy-gevoelig | Voertuig locaties, chauffeur gedrag | Strikte need-to-know |
| **Restricted** | Wettelijk beschermd | Onbewerkte GPS-data (<3 maanden) | Data Platform Team only |

### 1.2 Data Types

| Data Type | Classificatie | Retentie | Anonimisering |
|-----------|---------------|----------|---------------|
| **GPS Locatie (raw)** | Restricted | 3 maanden → Confidentieel | Na 3 maanden: grid-based (100m precisie) |
| **Voertuig ID** | Confidentieel | 5 jaar | Pseudonimisering |
| **Timestamp** | Intern | 5 jaar | Geen |
| **Diagnostische codes** | Intern | 5 jaar | Geen |
| **Chauffeur ID** | Restricted | 3 maanden → verwijderd | Na 3 maanden: volledig verwijderd |

## 2. Toegangsbeleid

### 2.1 Role-Based Access Control

| Rol | Bronze | Silver | Gold | Cosmos DB | Terraform |
|-----|--------|--------|------|-----------|-----------|
| **Data Engineer** | Read/Write | Read/Write | Read | Read | Write |
| **Data Analyst** | Read | Read | Read | - | - |
| **Planner** | - | - | Read (aggregaties) | Read (alerts) | - |
| **Compliance Officer** | Read (audit) | Read (audit) | Read (audit) | - | - |
| **Data Platform Team** | Admin | Admin | Admin | Admin | Admin |

### 2.2 Unity Catalog Grants

```sql
-- Voorbeeld: Analysts mogen alleen geaggregeerde data
GRANT SELECT ON gold.fct_trip_analysis TO `analysts`;
DENY SELECT ON silver.trip_events TO `analysts`;

-- Voorbeeld: Column-level security
GRANT SELECT (vehicle_id, timestamp, speed) ON silver.trip_events TO `planners`;
DENY SELECT (gps_lat, gps_lon) ON silver.trip_events TO `planners`;
```

## 3. Data Lineage & Audit

### 3.1 Azure Purview Integration

- **Automatische lineage**: Bronze → Silver → Gold
- **Schema tracking**: Alle wijzigingen gelogd
- **Access audit**: Wie heeft welke data geraadpleegd
- **Compliance reports**: GDPR-ready exports

### 3.2 Audit Requirements

| Event Type | Retention | Review Frequency |
|------------|-----------|------------------|
| **Schema wijzigingen** | 5 jaar | Bij elke wijziging |
| **Access logs** | 2 jaar | Maandelijks (compliance) |
| **Data exports** | 5 jaar | Per export |
| **Anonimisering runs** | 5 jaar | Kwartaal |

## 4. Data Quality

### 4.1 Quality Dimensions

| Dimensie | Metric | Threshold | Actie bij breach |
|----------|--------|-----------|------------------|
| **Completeness** | % non-null required fields | >99.5% | Alert + DLQ |
| **Accuracy** | % schema-valid events | >99.9% | Alert + reject |
| **Timeliness** | Event age bij Bronze write | <30s P95 | Alert + backpressure |
| **Consistency** | % duplicate events | <0.1% | Deduplicatie in Silver |

### 4.2 Data Quality Tests (dbt)

```yaml
# Voorbeeld: dbt schema.yml
models:
  - name: fct_trip_analysis
    tests:
      - dbt_utils.expression_is_true:
          expression: "distance_km >= 0"
      - dbt_utils.recency:
          datepart: day
          field: trip_date
          interval: 2
```

## 5. GDPR Compliance

### 5.1 Rechten van Betrokkenen

| Recht | Proces | SLA |
|-------|--------|-----|
| **Inzage** | Self-service dashboard voor chauffeurs | 48 uur |
| **Rectificatie** | Ticket naar Data Platform Team | 5 werkdagen |
| **Vergetelheid** | Automatische anonimisering na 3 maanden | N/A (automated) |
| **Dataportabiliteit** | Export via dashboard | 48 uur |
| **Bezwaar** | Opt-out via portal → stop tracking | Onmiddellijk |

### 5.2 Anonimiseringsstrategie

#### Na 3 maanden:
- **GPS**: Grid-based (100m × 100m)
- **Chauffeur ID**: Volledig verwijderd
- **Voertuig ID**: Pseudoniem blijft (voor analytics)
- **Timestamp**: Afgerond naar uur

#### Audit:
```sql
-- Verificatie: geen raw GPS ouder dan 90 dagen
SELECT COUNT(*) 
FROM silver.trip_events
WHERE gps_precision = 'exact' 
  AND timestamp < CURRENT_DATE() - INTERVAL 90 DAYS;
-- Expected: 0
```

## 6. Data Retention

### 6.1 Retention per Layer

| Layer | Default Retention | Exception | Rationale |
|-------|-------------------|-----------|-----------|
| **Bronze** | 5 jaar | Audit events: 7 jaar | Reproducibility + compliance |
| **Silver** | 5 jaar (anoniem) | - | GDPR-compliant analytics |
| **Gold** | 5 jaar | - | Business intelligence |
| **Cosmos DB** | 24 uur (TTL) | - | Operational alerts only |

### 6.2 Delete Policy

```python
# Voorbeeld: Databricks job voor Bronze cleanup
DELETE FROM bronze.telemetry
WHERE event_date < CURRENT_DATE() - INTERVAL 5 YEARS;

OPTIMIZE bronze.telemetry;
VACUUM bronze.telemetry RETAIN 168 HOURS;  # 7 dagen
```

## 7. Change Management

### 7.1 Schema Change Process

Zie [Schema Governance](schema_governance/README.md)

### 7.2 Data Classification Change

| Trigger | Proces |
|---------|--------|
| Nieuwe data source | Classificatie assessment + Legal review |
| Regulatory wijziging | Re-classificatie + impact analyse |
| Security incident | Emergency re-classification mogelijk |

## 8. Compliance Checks

### 8.1 Kwartaal Review

- [ ] Purview lineage controle
- [ ] Access audit (unexpected access patterns)
- [ ] GDPR anonimisering verificatie
- [ ] Data quality metrics review
- [ ] Retention policy compliance

### 8.2 Annual Audit

- [ ] Full security assessment
- [ ] GDPR compliance audit (extern)
- [ ] Data classification review
- [ ] Disaster recovery test
- [ ] Cost optimization review
