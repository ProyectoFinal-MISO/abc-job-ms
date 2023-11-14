import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.modelos import Role, TechnicalSkills, SoftSkills
from application import application as app

from modelos.populate_db import upsert_role, upsert_technical_skill, upsert_soft_skill, populate_database


def test_upsert_role():
    name = 'Project Manager2'

    # Llama a la función upsert_role
    upsert_role(name)

    # Verifica que el idioma se haya insertado en la base de datos
    role = Role.query.filter_by(name=name).first()
    assert role is not None

def test_upsert_technical_skill():
    name = 'Python2'

    # Llama a la función upsert_technical_skill
    upsert_technical_skill(name)

    # Verifica que el idioma se haya insertado en la base de datos
    technical_skill = TechnicalSkills.query.filter_by(name=name).first()
    assert technical_skill is not None

def test_upsert_soft_skill():
    name = 'Escuchar2'

    # Llama a la función upsert_soft_skill
    upsert_soft_skill(name)

    # Verifica que el idioma se haya insertado en la base de datos
    soft_skill = SoftSkills.query.filter_by(name=name).first()
    assert soft_skill is not None

def test_populate_database():
    populate_database()

    # Verifica que el idioma se haya insertado en la base de datos
    soft_skill = SoftSkills.query.filter_by(name="Empatía").first()
    assert soft_skill is not None

    # Verifica que el idioma se haya insertado en la base de datos
    technical_skill = TechnicalSkills.query.filter_by(name="Ruby").first()
    assert technical_skill is not None

    # Verifica que el idioma se haya insertado en la base de datos
    role = Role.query.filter_by(name="Architect").first()
    assert role is not None
