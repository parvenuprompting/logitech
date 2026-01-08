# ADR-001: Keuze voor Lakehouse over Lambda Architectuur

**Status**: Goedgekeurd  
**Datum**: 2026-01-08  
**Beslissers**: Architectuurteam

## Context

Voor het LogiTech Fleet Platform moeten we zowel realtime alerting (<10s) als historische analytics (5 jaar) ondersteunen. Traditioneel zou dit leiden tot een Lambda-architectuur met aparte hot/cold paths.

## Beslissing

We kiezen voor een **Modern Lakehouse-architectuur** met Databricks + Delta Lake, GEEN Lambda-architectuur.

## Rationale

### Pro Lakehouse:
- **Eén businesslogica-implementatie**: Geen duplicatie tussen batch en streaming
- **Delta Lake uniformiteit**: Streaming én batch lezen dezelfde bron
- **Lager onderhoud**: Geen synchronisatie tussen hot/cold paths
- **Cost efficiency**: Geen dubbele infrastructuur

### Contra Lambda:
- **Dubbele logica**: Streaming én batch implementeren zelfde business rules
- **Drift risico**: Hot/cold paths kunnen uit sync raken
- **Hogere TCO**: 2 separate processing stacks

## Consequentie

- Databricks wordt centrale processing layer
- Streaming én batch jobs gebruiken Delta Lake
- dbt wordt ALLEEN batch (geen streaming in dbt)
- Silver Layer bevat alle businesslogica (single source of truth)

## Alternatieven

- Lambda-architectuur: Afgewezen (onderhoudslast)
- Kappa-architectuur (pure streaming): Afgewezen (overkill voor 5 jaar historische data)
