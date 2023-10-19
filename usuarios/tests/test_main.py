import json
from unittest import TestCase
from unittest.mock import patch

from faker import Faker
from faker.generator import random

from application import application
from modelos.modelos import Usuario, db

class TestUsuarios(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = application.test_client()
        application.app_context().push()
        self.usuario = Usuario(
                    username = "dacperezce",
                    email = "daniel@gmail.com",
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

    def test_crear_usuario_ok(self):

        nuevo_usuario = {
            "username":self.data_factory.name(),
            "password":self.data_factory.word(),
            "email":self.data_factory.word()
        }

        solicitud_nuevo_usuario = self.client.post(
            "/users",
            data=json.dumps(nuevo_usuario),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 201)

        usuario_nuevo = Usuario.query.get(2)        
        db.session.delete(usuario_nuevo)
        db.session.commit()
    
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