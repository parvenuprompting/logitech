# LogiTech Tools

Dit directory bevat hulpmiddelen voor ontwikkeling en testen.

## Load Generator (`load_generator/`)

Gebruik dit script om de end-to-end datapipeline te stress-testen.

### Vereisten
- Python 3.8+
- `azure-eventhub` package (`pip install azure-eventhub`)

### Gebruik

1.  Set Environment Variables:
    ```bash
    export EVENT_HUB_CONNECTION_STR="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=..."
    export EVENT_HUB_NAME="telemetry"
    export NUM_VEHICLES=20
    export EVENTS_PER_SEC=10
    ```

2.  Run Script:
    ```bash
    python load_generator/simulate_events.py
    ```

## Impact Analysis (`impact_analysis/`)
(Zie documentatie in `docs/governance/silver_layer_policy.md`)
