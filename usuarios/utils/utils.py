from modelos.modelos import Country, State, City

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

def location_user(user):

    countries = Country.query.all()
    states = State.query.all()
    cities = City.query.all()


    found_country = None
    for country in countries:
        if country.id == user.country:
            found_country = country.name
            break

    found_state = None
    for state in states:
        if state.id == user.state:
            found_state = state.name
            break

    found_city = None
    for city in cities:
        if city.id == user.city:
            found_city = city.name
            break

    return {
        'country': found_country,
        'state': found_state,
        'city': found_city,
    }
