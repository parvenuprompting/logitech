# Non-Functional Requirements — LogiTech Fleet Platform

**Versie**: 1.0  
**Status**: Goedgekeurd  
**Datum**: 2026-01-08

## 1. Performance

### 1.1 Latency

| Metric | Requirement | Meetmethode |
|--------|-------------|-------------|
| **Alert Latency P50** | <5s | Event timestamp → Cosmos DB write |
| **Alert Latency P95** | <10s | Event timestamp → Cosmos DB write (HARD REQUIREMENT) |
| **Alert Latency P99** | <15s | Event timestamp → Cosmos DB write |
| **Dashboard Refresh** | <3s | Cosmos DB read → UI render |
| **Analytics Query P95** | <30s | Power BI refresh time |

### 1.2 Throughput

| Component | Requirement | Scaling Strategy |
|-----------|-------------|------------------|
| **Event Ingestion** | 2.000–5.000 events/sec sustained | Event Hubs auto-inflate |
| **Peak Ingestion** | 10.000 events/sec (burst) | Event Hubs partitioning (32 partitions) |
| **Streaming Processing** | 5.000 events/sec | Databricks auto-scaling (2-10 workers) |
| **Alert Delivery** | 1.000 alerts/sec | Azure Functions elastic scale |

## 2. Availability & Reliability

### 2.1 Uptime

| Service | SLA | Downtime/maand |
|---------|-----|----------------|
| **Ingestie (Event Hubs)** | 99.9% | 43 min |
| **Realtime Alerts** | 99.5% | 3.6 uur |
| **Analytics (Power BI)** | 99.0% | 7.2 uur |
| **Data Lake** | 99.99% | 4.3 min |

### 2.2 Data Durability

- **Event Hubs**: 7 dagen retentie (disaster recovery)
- **Bronze Layer**: 100% durability (Azure Storage LRS)
- **Silver/Gold**: 100% durability (geo-redundant backup)

### 2.3 Recovery

| Scenario | RPO | RTO | Procedure |
|----------|-----|-----|-----------|
| Event Hub failure | 0 (no data loss) | 10 min | Auto-failover to secondary partition |
| Databricks job failure | Checkpoint | 5 min | Auto-restart from last checkpoint |
| Cosmos DB region failure | <1 min | <5 min | Multi-region write enabled |
| Data Lake corruption | 24 uur | 2 uur | Restore from geo-redundant backup |

## 3. Schaalbaarheid

### 3.1 Data Volume

| Layer | Huidige Volume | 1 jaar | 5 jaar | Retention |
|-------|----------------|--------|--------|-----------|
| **Bronze** | - | ~15 TB | ~75 TB | 5 jaar |
| **Silver** | - | ~10 TB | ~50 TB | 5 jaar (anoniem na 3 maanden) |
| **Gold** | - | ~5 TB | ~25 TB | 5 jaar |

### 3.2 Fleet Groei

| Metric | Huidig | 2 jaar | Scaling Plan |
|--------|--------|--------|--------------|
| **Trucks** | 200 | 500 | Event Hubs partition scaling |
| **Events/truck/dag** | ~10.000 | ~15.000 | Databricks cluster auto-scale |
| **Total events/sec** | 2.000 | 5.000 | Horizontal scaling bewezen tot 10k |

## 4. Security & Compliance

### 4.1 GDPR

| Requirement | Implementation | Verificatie |
|-------------|----------------|-------------|
| **Right to be Forgotten** | Anonimisering na 3 maanden | Purview audit trail |
| **Data Minimization** | Alleen operationeel noodzakelijke velden | Schema review |
| **Consent Management** | Opt-in via driver portal | Legal approval |
| **Data Lineage** | Azure Purview end-to-end | Quarterly audit |

### 4.2 Access Control

- **Azure AD**: SSO voor alle services
- **RBAC**: Least-privilege per team
- **Databricks Unity Catalog**: Column-level access control
- **Secrets**: Azure Key Vault (geen hardcoded credentials)

### 4.3 Encryption

- **At Rest**: AES-256 voor alle storage
- **In Transit**: TLS 1.3 voor alle connections
- **Keys**: Customer-managed keys (CMK) via Key Vault

## 5. Observability

### 5.1 Monitoring

| Metric | Alert Threshold | Action |
|--------|-----------------|--------|
| **Alert Latency P95** | >10s | PagerDuty escalation |
| **Event Hub Lag** | >1 min | Auto-scale trigger |
| **Databricks Job Failure** | Any | Slack notification |
| **Cost Overage** | >80% maandbudget | Email to PM |

### 5.2 Logging

- **Retention**: 90 dagen (operational logs)
- **Audit Logs**: 5 jaar (compliance)
- **Log Analytics**: Centralized in Azure Monitor

## 6. Cost

### 6.1 Budget

| Omgeving | Maandelijks | Jaarlijks |
|----------|-------------|-----------|
| **Development** | €2.000 | €24.000 |
| **PoC** | €5.000 | €60.000 |
| **Production** | €15.000 | €180.000 |

### 6.2 Cost per Event

Target: **€0.001/event** (production scale 5k events/sec)

## 7. Acceptatiecriteria

### 7.1 PoC Success Criteria

- [ ] Alert latency P95 <10s gemeten over 1 week
- [ ] 0 data loss gedurende PoC-periode
- [ ] Schema wijziging zonder downtime
- [ ] GDPR-anonimisering gevalideerd
- [ ] Cost binnen 110% van budget

### 7.2 Production Readiness

- [ ] Load test: 10.000 events/sec sustained (1 uur)
- [ ] Failover test: <5 min RTO
- [ ] Security audit passed
- [ ] Legal approval GDPR-implementatie
- [ ] Runbook compleet + team trained
