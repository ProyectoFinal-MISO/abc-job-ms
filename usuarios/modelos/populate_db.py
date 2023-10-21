from modelos.modelos import db, Country, State, City, Languages, ProfessionalSector

def upsert_language(name, code):
    language = Languages.query.filter_by(name=name).first()
    if not language:
        language = Languages(name=name, code=code)
        db.session.add(language)
        db.session.commit()

def upsert_professional_sector(name, code):
    professional_sector = ProfessionalSector.query.filter_by(name=name).first()
    if not professional_sector:
        professional_sector = ProfessionalSector(name=name, code=code)
        db.session.add(professional_sector)
        db.session.commit()

def upsert_country(name, code):
    country = Country.query.filter_by(name=name).first()
    if not country:
        country = Country(name=name, code=code)
        db.session.add(country)
        db.session.commit()

def upsert_state(name, code, countryId):
    state = State.query.filter_by(name=name, countryId=countryId).first()
    if not state:
        state = State(name=name, code=code, countryId=countryId)
        db.session.add(state)
        db.session.commit()

def upsert_city(name, code, stateId):
    city = City.query.filter_by(name=name, stateId=stateId).first()
    if not city:
        city = City(name=name, code=code, stateId=stateId)
        db.session.add(city)
        db.session.commit()


def populate_database():

    languages_data = [
        {"name": "Español", "code": "ES"},
        {"name": "Ingles", "code": "EN"},
        {"name": "Frances", "code": "FR"},
        # Add more countries
    ]
    for language in languages_data:
        upsert_language(language["name"], language["code"])

    professional_sector_data = [
        {"name": "Professional sector 1", "code": "ProfessionalSector1"},
        {"name": "Professional sector 2", "code": "ProfessionalSector2"},
        # Add more countries
    ]
    for professional_sector in professional_sector_data:
        upsert_professional_sector(professional_sector["name"], professional_sector["code"])

    countries_data = [
        {"name": "Colombia", "code": "COL"},
        {"name": "Perú", "code": "PER"},
        {"name": "Estados Unidos", "code": "EUA"},
        # Add more countries
    ]
    for country in countries_data:
        upsert_country(country["name"], country["code"])

    states_data = [
        {"name": "Cundinamarca", "countryId": 1, "code": "CUN"},
        {"name": "Antioquia", "countryId": 1, "code": "ANT"},
        {"name": "Meta", "countryId": 1, "code": "MET"},
        {"name": "Loreto", "countryId": 2, "code": "LOR"},
        {"name": "Puno", "countryId": 2, "code": "PUN"},
        {"name": "Lima", "countryId": 2, "code": "LIM"},
        # Add more states
    ]
    for state in states_data:
        upsert_state(state["name"], state["code"], state["countryId"])

    cities_data = [
        {"name": "Bogotá", "stateId": 1, "code": "BOG"},
        {"name": "Medellin", "stateId": 2, "code": "MED"},
        {"name": "Villavicencio", "stateId": 3, "code": "VLL"},
        # Add more cities
    ]
    for city in cities_data:
        upsert_city(city["name"], city["code"], city["stateId"])

    db.session.commit()
