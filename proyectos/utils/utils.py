from enum import Enum

def enum_serializer(obj):
    if isinstance(obj, Enum):
        return obj.name
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
