import json
from unittest import TestCase
from unittest.mock import patch

from faker import Faker
from faker.generator import random

from application import application
from modelos.modelos import db

class TestUsuarios(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = application.test_client()
        application.app_context().push()

    def test_health(self):
        solicitud_nuevo_usuario = self.client.get(
            "/evaluations/ping",
        )
        self.assertEqual(solicitud_nuevo_usuario.status_code, 200)