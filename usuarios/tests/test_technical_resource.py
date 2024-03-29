import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.modelos import TypeIdentification, TechnicalResource, Genre, EducationLevel
from application import application as app
from utils.utils import generate_string_random

from utils.technical_resource import TechnicalResourceCreate

def new_technical_resource():
    return {
        "personalInformation": {
            "name": "Juan",
            "lastName": "Perez",
            "typeIdentification": TypeIdentification.CC,
            "identification":  '123456789' + generate_string_random(5),
            "birthdate": '1993-10-31',
            "genre": Genre.MALE,
            "phoneNumber": "1234567",
            "mobileNumber": "1234567890",
            "city": "Bogota",
            "state": "Bogota",
            "country": "Colombia",
            "address": "Calle 123",
            "photo": "//"
        },
        "academicInformation" : [
            {
                "schoolName": "Universidad Nacional",
                "educationLevel": EducationLevel.MASTER,
                "professionalSector": 1,
                "startDate": '2010-10-31',
                "endDate": '2012-10-31',
            }
        ],
        "professionalExperience" : [
            {
                "companyName": "ABC",
                "titleJob": "Desarrollador",
                "startDate": '2010-10-31',
                "endDate": '2012-10-31',
                "details": "Desarrollador de software"
            }
        ],
        "additionalInformation" : {
            "driverLicense": "abcdef",
            "transferAvailability": True,
            "vehicule": "abcdef"
        },
        "programmingLanguages" : [
            {
                "name": "Python",
                "score":5
            }
        ],
        "languages" : [
            {
                "language": 1,
                "score": 5
            }
        ],
        "personalSkills" : [
            {
                "name": "Trabajo en equipo",
                "score": 5
            }
        ]
    }

def test_technical_resource_create():
    # Llama a la función TechnicalResourceCreate
    response = TechnicalResourceCreate(userId = 1, user_data = new_technical_resource())
    assert response[1] == 201

def test_technical_resource_create_identification_exits():
    technical_resource = new_technical_resource()
    # Llama a la función TechnicalResourceCreate
    response = TechnicalResourceCreate(userId = 1, user_data = technical_resource)
    response_2 = TechnicalResourceCreate(userId = 1, user_data = technical_resource)

    assert response_2[1] == 412
