import json
import jsonschema
from jsonschema import validate
from datetime import datetime
import uuid
import sys
import os

# Helper om schema te laden (in productie zou dit van Schema Registry komen)
def load_schema(version="1.0.0"):
    schema_path = f"schemas/telemetry_event_v{version}.json"
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"Schema versie {version} niet gevonden op pad {schema_path}")

def validate_event(event_data):
    """
    Valideert een enkel event record tegen het JSON schema.
    Returns: (is_valid, error_message)
    """
    try:
        # 1. Parse JSON indien string
        if isinstance(event_data, str):
            event_obj = json.loads(event_data)
        else:
            event_obj = event_data

        # 2. Extract versie (default naar 1.0.0 indien niet aanwezig voor backward compatibility tests)
        version = event_obj.get("schema_version", "1.0.0")
        
        # 3. Laad schema
        schema = load_schema(version)
        
        # 4. Valideer
        validate(instance=event_obj, schema=schema)
        
        return True, None
        
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except jsonschema.ValidationError as e:
        return False, f"Schema Validation Error: {e.message} at path: {'/'.join(map(str, e.path))}"
    except Exception as e:
        return False, f"Unexpected Error: {str(e)}"

if __name__ == "__main__":
    # Simpele test bij direkte uitvoering
    test_event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "vehicle_id": "VEH001234",
        "event_type": "position",
        "schema_version": "1.0.0",
        "payload": {
            "latitude": 52.3676,
            "longitude": 4.9041,
            "speed_kmh": 85.0
        }
    }
    
    valid, error = validate_event(test_event)
    if valid:
        print("✅ Test event is valid")
    else:
        print(f"❌ Test event invalid: {error}")
        sys.exit(1)
