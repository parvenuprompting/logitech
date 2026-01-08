# ADR-002: Medallion Architecture (Bronze/Silver/Gold)

**Status**: Goedgekeurd  
**Datum**: 2026-01-08  
**Beslissers**: Architectuurteam

## Context

We hebben een duidelijke scheiding nodig tussen raw data, clean data, en business-aggregaties.

## Beslissing

We implementeren **Medallion Architecture** met drie lagen:

### Bronze Layer
- **Doel**: Immutable raw data capture
- **Eigenschappen**: Append-only, geen transformaties, volledige historische waarheid
- **Format**: Delta Lake, partitioned by time + vehicle_id

### Silver Layer
- **Doel**: Clean, enriched, canonieke data
- **Eigenschappen**: Alle businesslogica, validatie, deduplicatie, verrijking
- **Ownership**: Data Platform Team (strikte change policy)

### Gold Layer
- **Doel**: Business-vriendelijke aggregaties en dimensies
- **Eigenschappen**: dbt models, optimized for queries, pre-aggregated

## Rationale

- **Reproducibility**: Bronze = single source of truth, altijd reproduceerbaar
- **Separation of concerns**: Raw ingest ≠ business logic ≠ reporting
- **GDPR**: Anonimisering in Silver, Bronze blijft onveranderd
- **Debuggability**: Altijd terug naar Bronze mogelijk

## Consequenties

- Streaming én batch lezen van Bronze
- Silver is de "waarheidsbron" voor businesslogica
- Gold is read-only voor business users
- Geen data verwijderen uit Bronze (GDPR via anonimisering in Silver/Gold)

## Implementatie

```
Bronze: databricks/bronze/
Silver: databricks/silver/
Gold: dbt/models/marts/
```
