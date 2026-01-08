# Versioned Silver Logic Framework

Dit framework stelt ons in staat om businesslogica in de Silver Layer te wijzigen zonder risico (A/B testing, Canary rollouts).

## Usage Pattern

In je PySpark/SQL job:

```python
# 1. Load active config
def get_logic_version(feature_name):
    return spark.read.table("config.silver_feature_versions") \
        .filter(f"feature_name = '{feature_name}' AND is_active = true") \
        .first()

# 2. Apply logic based on version
config = get_logic_version("trip_distance_calculation")
params = json.loads(config.parameters_json)

if config.version.startswith("v1"):
    # Legacy logic
    df = apply_haversine(df)
elif config.version.startswith("v2"):
    # New logic (e.g. Map-matched distance)
    df = apply_osrm_distance(df)
```

## Governance
- **New Version**: Voeg rij toe aan `config.silver_feature_versions` met `is_active=false`.
- **Canary Test**: Zet `target_audience="CANARY"` en `is_active=true` voor beperkte uitrol.
- **Rollout**: Zet v1 `valid_to` op nu, en v2 `target_audience="ALL"`.
