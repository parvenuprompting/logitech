import json
import os
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    LongType,
    BooleanType,
    ArrayType,
    MapType,
    TimestampType,
    IntegerType
)

def _map_json_type_to_spark(json_type, format_type=None):
    """
    Maps a JSON schema type to a PySpark DataType.
    """
    if json_type == "string":
        if format_type == "date-time":
            return TimestampType()
        return StringType()
    elif json_type == "number":
        return DoubleType()
    elif json_type == "integer":
        return LongType()  # Safe default
    elif json_type == "boolean":
        return BooleanType()
    else:
        # Default fallback
        return StringType()

def load_schema_from_json(schema_path: str) -> StructType:
    """
    Reads a JSON Schema file and converts it to a PySpark StructType.
    Simplistic implementation tailored for the known telemetry schema.
    """
    with open(schema_path, "r") as f:
        schema_def = json.load(f)

    fields = []
    
    properties = schema_def.get("properties", {})
    required_fields = set(schema_def.get("required", []))

    for field_name, field_def in properties.items():
        json_type = field_def.get("type")
        nullable = field_name not in required_fields
        
        spark_type = None

        if json_type == "object":
            # Recursive struct handling (specifically for 'payload' in our case)
            if "properties" in field_def:
                sub_fields = []
                sub_props = field_def.get("properties", {})
                for sub_name, sub_def in sub_props.items():
                    sub_type = _map_json_type_to_spark(sub_def.get("type"), sub_def.get("format"))
                    # Assuming nullable for all sub-properties for flexibility unless strictly defined
                    sub_fields.append(StructField(sub_name, sub_type, True))
                spark_type = StructType(sub_fields)
            else:
                # Map unknown objects to MapType(String, String) or similar if needed, 
                # but StructType is preferred if schema is known.
                spark_type = MapType(StringType(), StringType())

        elif json_type == "array":
            items = field_def.get("items", {})
            element_type = _map_json_type_to_spark(items.get("type"), items.get("format"))
            spark_type = ArrayType(element_type)
        
        else:
            spark_type = _map_json_type_to_spark(json_type, field_def.get("format"))

        fields.append(StructField(field_name, spark_type, nullable))

    return StructType(fields)
