import pytest
from datetime import datetime, timezone
import random
import string

from src.utils.tecnical_resource import TecnicalResourceCreate, AcademicInformationCreate, ProfessionalExperienceCreate, AditionalInformationCreate

@pytest.fixture(scope = 'module')
def new_tecnical_resource():
    tecnical_resource = {
        "email": generar_cadena_aleatoria(10).join("@test.com"),
        "userType": "PERSON",
        "password": "test",
        "personalInformation": {
            "name": "test",
            "lastName" : "test",
            "typeIdentification" : "CC",
            "identification" : generar_cadena_aleatoria(10),
            "age" :30,
            "genre" : "MALE",
            "phoneNumber" :"test2",
            "mobileNumber" : "test",
            "city": "test",
            "nationality" :"test",
            "address" : "test"
        },
        "academicInformation": [
            {
                "schoolName" : "Test1",
                "educationLevel" : "PROFESSIONAL",
                "professionalSector" : "1",
                "startDate" : datetime.now(timezone.utc),
                "endDate" : datetime.now(timezone.utc)
            },
            {
                "schoolName" : "Test2",
                "educationLevel" : "MASTER",
                "professionalSector" : "1",
                "startDate" : datetime.now(timezone.utc),
                "endDate" : datetime.now(timezone.utc)
            }
        ],
        "professionalExperience": [
            {
                "startDate" : datetime.now(timezone.utc),
                "endDate" : datetime.now(timezone.utc),
                "titleJob" : "Test1",
                "companyName" : "Test1",
                "details" : "Lorem ipsum ..."
            },
            {
                "startDate" : datetime.now(timezone.utc),
                "endDate" : datetime.now(timezone.utc),
                "titleJob" : "Test2",
                "companyName" : "Test2",
                "details" : "Lorem ipsum ..."
            }

        ],
        "aditionalInformation": {
            "driverLicense" : "Test",
            "transferAvailability" : 1,
            "vehicule" : "Test"
        }
    }
    return tecnical_resource

def test_tecnical_resource_create(new_tecnical_resource):

    response = TecnicalResourceCreate(1, new_tecnical_resource)

    assert response[1] == 201
    assert response[0]["userId"] == "1"
    assert len(response[0]["academicInformationIds"]) > 0
    assert len(response[0]["professionalExperienceIds"]) > 0
    assert response[0]["aditionalInformationId"] is not None

def test_tecnical_resource_create_missing_personal_information(new_tecnical_resource):
    del new_tecnical_resource['personalInformation']
    response = TecnicalResourceCreate(1, new_tecnical_resource)
    assert response[1] == 400

def test_tecnical_resource_create_missing_academic_information(new_tecnical_resource):
    del new_tecnical_resource['academicInformation']
    response = TecnicalResourceCreate(1, new_tecnical_resource)
    assert response[1] == 400

def test_tecnical_resource_create_missing_professional_experience(new_tecnical_resource):
    del new_tecnical_resource['professionalExperience']
    response = TecnicalResourceCreate(1, new_tecnical_resource)
    assert response[1] == 400

def test_tecnical_resource_create_missing_aditional_information(new_tecnical_resource):
    del new_tecnical_resource['aditionalInformation']
    response = TecnicalResourceCreate(1, new_tecnical_resource)
    assert response[1] == 400

def generar_cadena_aleatoria(l):
    caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y dígitos
    cadena_aleatoria = ''.join(random.choice(caracteres) for _ in range(l))
    return cadena_aleatoria
