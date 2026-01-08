import unittest
import json
import uuid
from datetime import datetime
from validate_incoming_events import validate_event

class TestSchemaEvolution(unittest.TestCase):
    
    def setUp(self):
        self.base_event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": "2026-01-08T12:00:00Z",
            "vehicle_id": "VEH001234",
            "event_type": "position",
            "schema_version": "1.0.0",
            "payload": {
                "latitude": 52.0,
                "longitude": 4.0,
                "speed_kmh": 80
            }
        }

    def test_valid_event_v1(self):
        """Test of een standaard v1 event valide is."""
        is_valid, msg = validate_event(self.base_event)
        self.assertTrue(is_valid, f"Base event zou valide moeten zijn: {msg}")

    def test_missing_required_field(self):
        """Test breaking change: verplicht veld ontbreekt (simulatie van foute producer)."""
        invalid_event = self.base_event.copy()
        del invalid_event["vehicle_id"]
        is_valid, msg = validate_event(invalid_event)
        self.assertFalse(is_valid)
        self.assertIn("vehicle_id", msg)

    def test_invalid_enum_value(self):
        """Test dat alleen toegestane event types werken."""
        invalid_event = self.base_event.copy()
        invalid_event["event_type"] = "GHOST_RIDE"
        is_valid, msg = validate_event(invalid_event)
        self.assertFalse(is_valid)
        self.assertIn("GHOST_RIDE", msg)

    def test_extra_field_backward_compatibility(self):
        """Test backward compatibility: extra velden in payload mogen (additionalProperties=True)."""
        compatible_event = self.base_event.copy()
        compatible_event["payload"]["new_sensor_value"] = 123.456
        is_valid, msg = validate_event(compatible_event)
        self.assertTrue(is_valid, f"Extra payload fields moeten mogen (backward compatible): {msg}")

    def test_forbidden_root_field(self):
        """Test dat unknown fields op root niveau niet mogen (additionalProperties=False)."""
        invalid_event = self.base_event.copy()
        invalid_event["unknown_root_field"] = "hacker"
        is_valid, msg = validate_event(invalid_event)
        self.assertFalse(is_valid)
        # Msg zou iets moeten bevatten over additional properties niet toegestaan

    def test_pattern_validation(self):
        """Test regex validatie op vehicle_id."""
        invalid_event = self.base_event.copy()
        invalid_event["vehicle_id"] = "BUS123" # Fout format, moet VEH... zijn
        is_valid, msg = validate_event(invalid_event)
        self.assertFalse(is_valid)
        self.assertIn("VEH", msg) # De regex zit in de error msg vaak of de value

if __name__ == '__main__':
    unittest.main()
