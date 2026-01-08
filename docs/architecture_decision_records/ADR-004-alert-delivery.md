# ADR-004: Alert Delivery Mechanisme

**Status**: Goedgekeurd  
**Datum**: 2026-01-08  
**Beslissers**: Architectuurteam

## Context

Realtime alerts (<10s) moeten betrouwbaar naar planners/dispatchers worden geleverd, zonder de analytics pipeline te vervuilen.

## Beslissing

We gebruiken **Cosmos DB + Azure Functions** als alert delivery layer, BUITEN het Data Lake.

## Architectuur

```
Streaming Job → Cosmos DB (TTL 24h) → Azure Function → WebSocket/Push
```

## Rationale

### Waarom Cosmos DB:
- **Low latency writes**: <10ms P99
- **Change Feed**: Native trigger voor Azure Functions
- **TTL support**: Automatisch cleanup na 24 uur
- **Geo-replication**: Multi-region deployment mogelijk

### Waarom NIET Delta Lake voor alerts:
- Delta is optimized voor analytics, niet voor operational serving
- Streaming naar Delta + query vanaf dashboard = dubbele latency
- Cosmos DB geeft push-model (Change Feed), Delta vereist polling

### Waarom Azure Functions:
- **Event-driven**: Cosmos DB Change Feed trigger
- **Serverless**: Automatische scaling bij alert storms
- **Rate limiting**: Eenvoudig max throughput naar UI implementeren

## Consequenties

- Alerts worden WEL ook opgeslagen in Delta (Silver/Gold) voor analytics
- Cosmos DB is ephemeral storage (24h TTL)
- Alert logic blijft in Databricks (feature flags, rate limiting)
- Azure Function is pure dispatcher (geen businesslogica)

## Data Flow

1. **Streaming job detecteert alert** (Databricks)
2. **Write naar Cosmos DB** (voor delivery) + **Delta** (voor analytics)
3. **Azure Function triggert** op Cosmos Change Feed
4. **Push naar dashboard** via WebSocket/SignalR

## Alternatieven

- Delta Lake + polling: Afgewezen (latency + inefficiënt)
- Event Grid: Afgewezen (geen TTL, geen query capabilities)
- Service Bus: Afgewezen (overkill voor simple push)
