import json
from unittest import TestCase
from datetime import datetime, timezone
from unittest.mock import patch

from faker import Faker
from faker.generator import random

from application import application
from modelos.modelos import Usuario, db, UserType, TypeIdentification, Genre, EducationLevel


def new_technical_resource():
    return {
        "personalInformation": {
            "name": "Juan",
            "lastName": "Perez",
            "typeIdentification": TypeIdentification.CC,
            "identification":  '123456789' + generate_string_random(5),
            "birthdate": datetime(1993, 1, 1, tzinfo=timezone.utc),
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
                "startDate": datetime(2010, 1, 1, tzinfo=timezone.utc),
                "endDate": datetime(2012, 1, 1, tzinfo=timezone.utc)
            }
        ],
        "professionalExperience" : [
            {
                "companyName": "ABC",
                "titleJob": "Desarrollador",
                "startDate": datetime(2010, 1, 1, tzinfo=timezone.utc),
                "endDate": datetime(2012, 1, 1, tzinfo=timezone.utc),
                "details": "Desarrollador de software"
            }
        ],
        "aditionalInformation" : {
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

class TestUsuarios(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = application.test_client()
        application.app_context().push()
        self.usuario = Usuario(
                    username = "dacperezce",
                    email = "daniel@gmail.com",
                    userType=UserType.PERSON,
                    photo="oanodnaosdoansodnaosn",
                    password = "88d5f5ecc3187752b6ed943cb37760a6edb941cd0baf7e47247560f18358db2a",
                    salt = "jS6MzFJiV8AZHvD"
                )
        db.session.add(self.usuario)
        db.session.commit()

    def tearDown(self):
        db.session.delete(self.usuario)
        db.session.commit()

    def test_crear_usuario_bad_request(self):
        nuevo_usuario = {
            "username":"dacperezce",
            "password":"hola",
        }
        solicitud_nuevo_usuario = self.client.post(
            "/users",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 400)

    def test_crear_usuario_no_request(self):
        solicitud_nuevo_usuario = self.client.post(
            "/users"
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 400)

    def test_crear_usuario_repetido(self):
        nuevo_usuario = {
            "username":"dacperezce",
            "password":"hola",
            "email":"daniel@gmail.com"
        }
        solicitud_nuevo_usuario = self.client.post(
            "/users",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 412)

    # def test_crear_usuario_ok(self):
    #     solicitud_nuevo_usuario = self.client.post(
    #         "/users",
    #         data=json.dumps(new_technical_resource()),
    #         headers={'Content-Type': 'application/json'}
    #     )
    #     self.assertEqual(solicitud_nuevo_usuario.status_code, 201)

    def test_generacion_token_no_request(self):
        solicitud_nuevo_usuario = self.client.post(
            "/users/auth"
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 400)

    def test_generacion_token_bad_request(self):
        nuevo_usuario = {
            "username":"dacperezce"
        }
        solicitud_nuevo_usuario = self.client.post(
            "/users/auth",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 400)

    def test_generacion_token_not_user(self):
        nuevo_usuario = {
            "username":"dacperezce1",
            "password":"hola",
        }
        solicitud_nuevo_usuario = self.client.post(
            "/users/auth",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 404)

    def test_generacion_token_wrong_password(self):
        nuevo_usuario = {
            "username":"dacperezce",
            "password":"hola1",
        }
        solicitud_nuevo_usuario = self.client.post(
            "/users/auth",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 404)

    def test_generacion_token_ok(self):
        nuevo_usuario = {
            "username":"dacperezce",
            "password":"hola",
        }
        solicitud_nuevo_usuario = self.client.post(
            "/users/auth",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 200)

    def test_health(self):
        solicitud_nuevo_usuario = self.client.get(
            "/users/ping",
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 200)

    def test_consulta_usuario_ok(self):
        nuevo_usuario = {
            "username":"dacperezce",
            "password":"hola",
        }
        solicitud_nuevo_usuario = self.client.post(
            "/users/auth",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )
        token = solicitud_nuevo_usuario.json.get('token', None)
        solicitud_nuevo_usuario = self.client.get(
            "/users/me",
            headers={'Authorization': f"Bearer {token}"}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 200)

def generate_string_random(length):
    import string
    import random
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
