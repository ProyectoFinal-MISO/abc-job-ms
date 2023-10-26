import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.modelos import TypeIdentification, Company
from application import application as app

from utils.company import CompanyCreate

def test_company_create():
    data = {
        "personalInformation": {
            "name": "Sample Company",
            "typeIdentification": TypeIdentification.NIT,
            "identification": '123456789' + generate_string_random(5),
            "phoneNumber": "555-555-5555",
            "mobileNumber": "555-555-5555",
            "city": 1,
            "state": 1,
            "country": 1,
            "address": "Sample Address"
        }
    }

    # Llama a la función CompanyCreate
    response = CompanyCreate(userId = 1, user_data = data)

    assert response[1] == 201

def test_company_create_identification_exits():
    data = {
        "personalInformation": {
            "name": "Sample Company",
            "typeIdentification": TypeIdentification.NIT,
            "identification": '9512357' + generate_string_random(10),
            "phoneNumber": "555-555-5555",
            "mobileNumber": "555-555-5555",
            "city": 1,
            "state": 1,
            "country": 1,
            "address": "Sample Address"
        }
    }
    # Llama a la función CompanyCreate
    response = CompanyCreate(userId = 1, user_data = data)
    response_2 = CompanyCreate(userId = 1, user_data = data)

    assert response_2[1] == 400

def generate_string_random(length):
    import string
    import random
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
