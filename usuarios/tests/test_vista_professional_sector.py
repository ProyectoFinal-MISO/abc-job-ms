import json
from unittest import TestCase
from unittest.mock import patch

from faker import Faker
from faker.generator import random

from flask_jwt_extended import create_access_token

from application import application
from modelos.modelos import db, TypeIdentification, ProfessionalSector
from vistas.professional_sector import VistaProfessionalSector


class TestCompanies(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.data_factory = Faker()
        self.client = application.test_client()
        application.app_context().push()

    def test_get_professional_sector(self):
        # Create a fake professional_sector
        professional_sector = ProfessionalSector(
            name="Sector1" + generate_string_random(5),
            code="s1" + generate_string_random(5)
        )
        db.session.add(professional_sector)
        db.session.commit()

        # Make a request to get the professional_sector
        response = self.client.get(f"/users/professional_sector", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)

def generate_string_random(length):
    import string
    import random
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
