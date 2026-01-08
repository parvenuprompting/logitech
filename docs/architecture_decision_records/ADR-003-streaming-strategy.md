# ADR-003: Streaming Strategie (Structured Streaming vs DLT)

**Status**: Goedgekeurd  
**Datum**: 2026-01-08  
**Beslissers**: Architectuurteam

## Context

Voor realtime alerting (<10s latency) moeten we streaming verwerking implementeren in Databricks.

## Beslissing

We gebruiken **Spark Structured Streaming** als primaire streaming oplossing, met **Delta Live Tables (DLT)** als optie voor minder latency-kritische flows.

## Rationale

### Structured Streaming (Hot Path)
- **Latency**: <10s mogelijk met continuous processing
- **Controle**: Volledige controle over watermarks, triggers, checkpoints
- **Feature flags**: Eenvoudig runtime kill-switch implementeren
- **Backpressure**: Handmatig tunen mogelijk

### Delta Live Tables (Warm Path)
- **Simplicity**: Declaratieve syntax, minder boilerplate
- **Auto-scaling**: Automatische resource management
- **Lineage**: Built-in data quality + lineage tracking
- **Use case**: Niet voor <10s alerts, wel voor Silver batch transformaties

## Keuzerichtlijn

| Use Case | Technologie | Rationale |
|----------|-------------|-----------|
| Realtime alerts (<10s) | Structured Streaming | Latency + feature flags |
| Silver batch transformaties | DLT of Spark batch | Kies op basis van complexiteit |
| Gold aggregaties | dbt | Batch-only |

## Consequenties

- Hot path: Handmatig geschreven Structured Streaming jobs
- Feature flags via config Delta tables
- DLT mogelijk voor Silver, maar niet verplicht
- **Geen dbt in streaming** (strikte scheiding)

## Alternatieven

- Kafka Streams: Afgewezen (geen Delta Lake integratie)
- Flink: Afgewezen (team expertise + Azure native)
