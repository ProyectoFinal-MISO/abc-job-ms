import pytest
from datetime import datetime, timezone
import random
import string

from src.utils.tecnical_resource import TecnicalResourceCreate, TecnicalResourceDelete, AcademicInformationDelete, ProfessionalExperienceDelete, AditionalInformationDelete

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

def test_tecnical_resource_delete(new_tecnical_resource):
    tr = TecnicalResourceCreate(1, new_tecnical_resource)
    response = TecnicalResourceDelete(tr[0]['id'])
    assert response.status_code == 204

def test_tecnical_resource_delete_not_found():
    response = TecnicalResourceDelete(50)
    assert response.status_code == 404

def generar_cadena_aleatoria(l):
    caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y dígitos
    cadena_aleatoria = ''.join(random.choice(caracteres) for _ in range(l))
    return cadena_aleatoria
