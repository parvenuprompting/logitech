# Silver Layer Change Policy

> [!IMPORTANT]
> **Single Source of Truth**
> De Silver Layer bevat de canonieke businesslogica van het LogiTech Fleet Platform. Wijzigingen hierin hebben impact op zowel Real-time Streaming (Alerts) als Batch Analytics (Gold/Reporting).

## 1. Change Approval Matrix

De vereiste goedkeuring hangt af van de impact van de wijziging.

| Change Type | Voorbeeld | Impact Scope | Review Vereisten | Deploy Strategie |
|-------------|-----------|--------------|------------------|------------------|
| **Low Impact** | Nieuwe kolom met simpele verrijking (bijv. weerdata) | Geen impact op bestaande logica | **1 Peer Review** | Standard Rollout |
| **Medium Impact** | Wijziging in bestaande berekening (bijv. `distance_traveled` formule) | Data in Gold verandert, mogelijk metrics anders | **Peer Review + Data Owner Approval** | Canary Rollout |
| **High Impact** | Wijziging in Alert logica (bijv. threshold aanpassing) | Directe impact op operatie (alerts gemist/extra) | **Architect Review + Impact Analyse** | Feature Flag Toggle |
| **Critical** | Schema breaking change (field rename/delete) | Breekt downstream consumers (Streaming & Batch) | **Architect + Stakeholder Approval + ADR** | Versioned Parallel Run |

## 2. Code Review Richtlijnen

Elke Pull Request (PR) die code in `databricks/silver/` aanraakt MOET voldoen aan:

1.  **Unit Tests**: Nieuwe logica moet gedekt zijn door unit tests (PyTest).
2.  **Integration Test**: Draai een integratietest met een sample dataset om te verifiëren dat de pipeline niet crasht.
3.  **Backwards Compatibility Check**:
    - Mag ik oude data nog inlezen met deze nieuwe code?
    - Breekt dit het schema van de Delta tabel? (Schema evolutie test)
4.  **Performance Check**:
    - Gebruik ik `udf` (traag) of native spark functions?
    - Zitten er dure joins in? (Broadcast indicatie?)

## 3. Deployment & Rollback

- **Feature Flags**: Alle wijzigingen aan alert-bepalende logica moeten achter een feature flag zitten (`config.alert_feature_flags`).
- **Rollback**:
    - *Low/Medium*: `git revert` + redeploy job.
    - *High/Critical*: Feature flag uitzetten (secundairen) of versie terugdraaien.
