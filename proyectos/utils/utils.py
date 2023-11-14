from enum import Enum

def generate_string_random(length):
    import string
    import random
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def enum_serializer(obj):
    if isinstance(obj, Enum):
        return obj.name
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
