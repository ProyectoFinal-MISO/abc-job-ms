from modelos.modelos import Country, State, City

from enum import Enum

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
            found_country = country
            break

    found_state = None
    for state in states:
        if state.id == user.state:
            found_state = state
            break

    found_city = None
    for city in cities:
        if city.id == user.city:
            found_city = city
            break

    return {
        'country': found_country.name,
        'state': found_state.name,
        'city': found_city.name,
    }
