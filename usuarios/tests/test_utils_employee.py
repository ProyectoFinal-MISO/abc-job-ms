import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.modelos import TypeIdentification, Employee
from application import application as app
from modelos.populate_db import populate_database

from utils.utils import generate_string_random
from utils.employee import EmployeeCreate

populate_database()

def test_employee_create():
    data = {
        "personalInformation": {
            "name": "Sample Employee",
            "lastName": "Sample Employee",
            "typeIdentification": TypeIdentification.CC,
            "identification": '12345' + generate_string_random(10),
            "phoneNumber": "555-555-5555",
            "mobileNumber": "555-555-5555",
            "city": 1,
            "state": 1,
            "country": 1,
            "address": "Sample Address",
            "photo": "//"
        }
    }

    # Llama a la función EmployeeCreate
    response = EmployeeCreate(userId = 1, user_data = data)
    print(response[0].get('mensaje'))
    assert response[1] == 201

def test_employee_create_identification_exits():
    data = {
        "personalInformation": {
            "name": "Sample Employee",
            "typeIdentification": TypeIdentification.NIT,
            "identification": '123456789' + generate_string_random(5),
            "phoneNumber": "555-555-5555",
            "mobileNumber": "555-555-5555",
            "city": 1,
            "state": 1,
            "country": 1,
            "address": "Sample Address",
            "photo": "//"
        }
    }
    # Llama a la función EmployeeCreate
    response = EmployeeCreate(userId = 1, user_data = data)
    response_2 = EmployeeCreate(userId = 1, user_data = data)

    assert response_2[1] == 400
