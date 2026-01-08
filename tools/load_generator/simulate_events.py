import time
import uuid
import json
import random
import os
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

# Config
EVENT_HUB_CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME", "telemetry")
NUM_VEHICLES = int(os.getenv("NUM_VEHICLES", "10"))
EVENTS_PER_SEC = int(os.getenv("EVENTS_PER_SEC", "5"))

# Mock Data
VEHICLE_IDS = [f"TRUCK_{i:03d}" for i in range(1, NUM_VEHICLES + 1)]
EVENT_TYPES = ["position", "position", "position", "position", "idle", "alert"]

def generate_event(vehicle_id):
    """
    Generates a single telemetry event compliant with v1.0.0 schema
    """
    event_type = random.choice(EVENT_TYPES)
    
    # Simulate realistic driving data
    base_lat = 52.3676
    base_lon = 4.9041
    lat_offset = random.uniform(-0.1, 0.1)
    lon_offset = random.uniform(-0.1, 0.1)
    
    speed = random.uniform(0, 90) if event_type == "position" else 0
    rpm = random.uniform(1000, 2500) if speed > 0 else 600
    
    payload = {
        "event_id": str(uuid.uuid4()),
        "vehicle_id": vehicle_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "payload": {
            "latitude": base_lat + lat_offset,
            "longitude": base_lon + lon_offset,
            "speed_kmh": round(speed, 1),
            "heading": round(random.uniform(0, 360), 0),
            "fuel_level_percent": round(random.uniform(10, 100), 1),
            "engine_temp_c": round(random.uniform(70, 95), 1),
            "engine_rpm": round(rpm, 0)
        }
    }
    
    # Add anomaly occasionally
    if random.random() < 0.01:
        payload["version"] = "1.0.0" # Extra field
        
    return payload

def main():
    if not EVENT_HUB_CONNECTION_STR:
        print("ERROR: EVENT_HUB_CONNECTION_STR environment variable not set.")
        print("Usage: export EVENT_HUB_CONNECTION_STR='...'; python simulate_events.py")
        return

    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR,
        eventhub_name=EVENT_HUB_NAME
    )

    print(f"Starting simulation for {NUM_VEHICLES} vehicles.")
    print(f"Target throughput: {EVENTS_PER_SEC} events/sec. Press Ctrl+C to stop.")

    try:
        with producer:
            while True:
                batch = producer.create_batch()
                
                for _ in range(EVENTS_PER_SEC):
                    vehicle_id = random.choice(VEHICLE_IDS)
                    event_data = generate_event(vehicle_id)
                    json_data = json.dumps(event_data)
                    
                    try:
                        batch.add(EventData(json_data))
                    except ValueError:
                        # Batch full, send and create new
                        producer.send_batch(batch)
                        batch = producer.create_batch()
                        batch.add(EventData(json_data))
                
                producer.send_batch(batch)
                print(f"Sent batch of {EVENTS_PER_SEC} events at {datetime.now().time()}")
                time.sleep(1.0)
                
    except KeyboardInterrupt:
        print("Simulation stopped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
