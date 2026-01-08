# LogiTech Real-time Fleet Platform

Modern Lakehouse-architectuur op Azure voor realtime fleet monitoring en historische analytics.

## 🎯 Features

- **Realtime alerting** (<10s latency) voor operationele events
- **Historische analytics** (5 jaar retentie, GDPR-compliant)
- **Medallion Architecture** (Bronze/Silver/Gold) met Delta Lake
- **Lage TCO** door minimale dubbele logica

## 🏗️ Architectuur

```
IoT Devices → Event Hubs → Databricks (Bronze → Silver → Gold) → Serving Layer
                                ↓
                         Realtime Alerts (Cosmos DB + Functions)
```

### Technologie Stack

| Component | Technologie |
|-----------|-------------|
| **Ingestie** | Azure Event Hubs / IoT Hub |
| **Storage** | Azure Data Lake Gen2 + Delta Lake |
| **Processing** | Azure Databricks (Spark Structured Streaming) |
| **Analytics** | dbt (batch only) |
| **Realtime Alerts** | Cosmos DB + Azure Functions |
| **Dashboards** | Power BI |
| **IaC** | Terraform |

## 📁 Projectstructuur

```
logitech/
├── docs/
│   ├── architecture_decision_records/  # ADRs
│   ├── schema_governance/              # Event contracts
│   ├── nfr_specification.md
│   └── data_governance.md
├── infrastructure/
│   └── terraform/                       # Azure resources
├── databricks/
│   ├── bronze/                          # Raw data ingestion
│   ├── silver/                          # Clean & enriched
│   ├── streaming/                       # Realtime processing
│   └── schema_validation/               # Schema Registry
├── dbt/
│   ├── models/                          # Batch analytics
│   └── tests/
├── functions/
│   └── alert_dispatcher/                # Azure Functions
├── dashboards/                          # Power BI templates
└── monitoring/
    └── cost_tracking/                   # Cost governance
```

## 🚀 Quick Start

### Prerequisites

- Azure subscription met rechten voor Databricks, Event Hubs, Data Lake Gen2
- Terraform >= 1.5
- Python >= 3.10
- dbt >= 1.6

### Setup

```bash
# Clone repository
git clone <repo-url>
cd logitech

# Terraform infrastructure
cd infrastructure/terraform
terraform init
terraform plan
terraform apply

# dbt setup
cd ../../dbt
dbt deps
dbt run
```

## 📋 Development Workflow

### Fase 0: Architectuur & Governance ✅
- [x] Implementatieplan
- [ ] ADRs
- [ ] Schema Governance (Fase 0.5)

### Fase 1: Bronze Layer
- [ ] Event Hubs provisioning
- [ ] Data Lake setup
- [ ] Bronze ingestion jobs

### Fase 2: Realtime Processing
- [ ] Streaming jobs met feature flags
- [ ] Alert rollback mechanisme
- [ ] Cosmos DB + Functions

→ Zie [task.md](file:///Users/T/.gemini/antigravity/brain/50d6e4ec-b43c-44a8-a43a-16da1cf317ed/task.md) voor volledige takenlijst

## 🔐 Governance

### Schema Changes
Alle event contract wijzigingen vereisen approval via [Schema Governance](docs/schema_governance/).

### Silver Layer Changes
Strikte change policy met impactanalyse. Zie [implementation_plan.md](file:///Users/T/.gemini/antigravity/brain/50d6e4ec-b43c-44a8-a43a-16da1cf317ed/implementation_plan.md#silver-layer-change-policy).

### Cost Management
- Hard budgets per omgeving
- Weekly cost reviews (PoC-fase)
- Databricks cluster policies

## 🎯 KPI's

| Metric | Target | Status |
|--------|--------|--------|
| Alert Latency P95 | <10s | 🔴 Not deployed |
| Dubbele logica | 0 | ✅ Architectural |
| GDPR Compliance | 100% | 🟡 In progress |

## 📚 Documentatie

- [Implementatieplan](file:///Users/T/.gemini/antigravity/brain/50d6e4ec-b43c-44a8-a43a-16da1cf317ed/implementation_plan.md)
- [Takenlijst](file:///Users/T/.gemini/antigravity/brain/50d6e4ec-b43c-44a8-a43a-16da1cf317ed/task.md)
- ADRs: `docs/architecture_decision_records/`

## 🤝 Contributing

1. Maak feature branch: `git checkout -b feature/nieuwe-feature`
2. Volg governance policies (schema/Silver changes)
3. Run tests: `dbt test` of `pytest`
4. Submit PR met impactanalyse

## 📄 License

Proprietary - LogiTech Fleet Platform
