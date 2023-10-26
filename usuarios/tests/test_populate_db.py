import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.modelos import Languages, ProfessionalSector, Country, State, City
from application import application as app

from modelos.populate_db import upsert_language, upsert_professional_sector, upsert_country, upsert_state, upsert_city, populate_database

def test_upsert_language_creates_new_language(app):
    name = 'Italiano'
    code = 'IT'

    # Llama a la función upsert_language
    upsert_language(name, code)

    # Verifica que el idioma se haya insertado en la base de datos
    language = Languages.query.filter_by(name=name).first()
    assert language is not None

def test_upsert_professional_sector_creates_new_professional_sector(app):
    name = 'Professional sector 3'
    code = 'ProfessionalSector3'

    # Llama a la función upsert_professional_sector
    upsert_professional_sector(name, code)

    # Verifica que el sector profesional se haya insertado en la base de datos
    professional_sector = ProfessionalSector.query.filter_by(name=name).first()
    assert professional_sector is not None

def test_upsert_country_creates_new_country(app):
    name = 'Venezuela'
    code = 'VEN'

    # Llama a la función upsert_country
    upsert_country(name, code)

    # Verifica que el país se haya insertado en la base de datos
    country = Country.query.filter_by(name=name).first()
    assert country is not None

def test_upsert_state_creates_new_state(app):
    name = 'Estado de prueba'
    code = 'EP'
    countryId = 1

    # Llama a la función upsert_state
    upsert_state(name, code, countryId)

    # Verifica que el estado se haya insertado en la base de datos
    state = State.query.filter_by(name=name, countryId=countryId).first()
    assert state is not None

def test_upsert_city_creates_new_city(app):
    name = 'Ciudad de prueba'
    code = 'CP'
    stateId = 1

    # Llama a la función upsert_city
    upsert_city(name, code, stateId)

    # Verifica que la ciudad se haya insertado en la base de datos
    city = City.query.filter_by(name=name, stateId=stateId).first()
    assert city is not None
