import json
from unittest import TestCase
from unittest.mock import patch

from faker import Faker
from faker.generator import random

from flask_jwt_extended import create_access_token

from application import application
from modelos.modelos import db, TypeIdentification, Company
from vistas.companies import VistaCompany


class TestCompanies(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.data_factory = Faker()
        self.client = application.test_client()
        application.app_context().push()



    def test_get_company(self):
        # Create a fake company
        company = Company(
            userId=1,
            name=self.data_factory.company(),
            typeIdentification=TypeIdentification.NIT,
            identification=self.data_factory.random_number(digits=9),
            phoneNumber=self.data_factory.phone_number(),
            mobileNumber=self.data_factory.phone_number(),
            city=self.data_factory.city(),
            state=self.data_factory.state(),
            country=self.data_factory.country(),
            address=self.data_factory.address()
        )
        db.session.add(company)
        db.session.commit()

        # Make a request to get the company
        response = self.client.get(f"/user/company/{company.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'id': company.id,
            'userId': company.userId,
            'name': company.name,
            'identification': company.identification,
            'phoneNumber': company.phoneNumber,
            'mobileNumber': company.mobileNumber,
            'city': company.city,
            'state': company.state,
            'country': company.country,
            'address': company.address
        })

    def test_get_company_with_non_integer_id(self):
        # Make a request to get a company with a non-integer id
        response = self.client.get(f"/user/company/abc", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)

    def test_get_nonexistent_company(self):

        # Make a request to get a nonexistent company
        response = self.client.get(f"/user/company/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)

    def test_delete_company(self):
        # Create a company to delete
        company = Company(
            userId=1,
            name=self.data_factory.company(),
            typeIdentification=TypeIdentification.NIT,
            identification=self.data_factory.random_number(digits=9),
            phoneNumber=self.data_factory.phone_number(),
            mobileNumber=self.data_factory.phone_number(),
            city=self.data_factory.city(),
            state=self.data_factory.state(),
            country=self.data_factory.country(),
            address=self.data_factory.address()
        )
        db.session.add(company)
        db.session.commit()

        # Delete the company
        response = self.client.delete(f'/user/company/{company.id}', headers=self.headers)

        # Check that the company was deleted
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Company deleted')

    def test_delete_nonexistent_company(self):
        # Delete a nonexistent company
        response = self.client.delete('/user/company/999', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Company not exist')

    def test_delete_company_with_noninteger_id(self):
        # Delete a company with a non-integer ID
        response = self.client.delete('/user/company/abc', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Company id is not integer')

    def test_put_company(self):
        # Create a company to update
        company = Company(
            userId=1,
            name=self.data_factory.company(),
            typeIdentification=TypeIdentification.NIT,
            identification=self.data_factory.random_number(digits=9),
            phoneNumber=self.data_factory.phone_number(),
            mobileNumber=self.data_factory.phone_number(),
            city=self.data_factory.city(),
            state=self.data_factory.state(),
            country=self.data_factory.country(),
            address=self.data_factory.address()
        )
        db.session.add(company)
        db.session.commit()

        # Update the company
        updated_company = {
            'name': self.data_factory.company(),
            'typeIdentification': "CC",
            'identification': self.data_factory.numerify('##########'),
            'phoneNumber': self.data_factory.numerify('##########'),
            'mobileNumber': self.data_factory.numerify('##########'),
            'city': self.data_factory.city(),
            'state': self.data_factory.state(),
            'country': self.data_factory.country(),
            'address': self.data_factory.address(),
        }
        response = self.client.put(f'/user/company/{company.id}', json=updated_company, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        # Check that the company was updated
        response = self.client.get(f'/user/company/{company.id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], updated_company['name'])
        self.assertEqual(response.json['identification'], updated_company['identification'])
        self.assertEqual(response.json['phoneNumber'], updated_company['phoneNumber'])
        self.assertEqual(response.json['mobileNumber'], updated_company['mobileNumber'])
        self.assertEqual(response.json['city'], updated_company['city'])
        self.assertEqual(response.json['state'], updated_company['state'])
        self.assertEqual(response.json['country'], updated_company['country'])
        self.assertEqual(response.json['address'], updated_company['address'])

    def test_update_nonexistent_company(self):
        # Update the company
        updated_company = {
            'name': self.data_factory.company(),
            'typeIdentification': "CC",
            'identification': self.data_factory.numerify('##########'),
            'phoneNumber': self.data_factory.numerify('##########'),
            'mobileNumber': self.data_factory.numerify('##########'),
            'city': self.data_factory.city(),
            'state': self.data_factory.state(),
            'country': self.data_factory.country(),
            'address': self.data_factory.address(),
        }
        # Update a nonexistent company
        response = self.client.put(f'/user/company/999', json=updated_company, headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Company not exist')

    def test_update_company_with_noninteger_id(self):
        # Update the company
        updated_company = {
            'name': self.data_factory.company(),
            'typeIdentification': "CC",
            'identification': self.data_factory.numerify('##########'),
            'phoneNumber': self.data_factory.numerify('##########'),
            'mobileNumber': self.data_factory.numerify('##########'),
            'city': self.data_factory.city(),
            'state': self.data_factory.state(),
            'country': self.data_factory.country(),
            'address': self.data_factory.address(),
        }
        # Update a nonexistent company
        response = self.client.put(f'/user/company/abc', json=updated_company, headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Company id is not integer')

    def test_update_company_with_field_missing(self):
        # Update the company
        updated_company = {
            'name': self.data_factory.company(),
            'identification': self.data_factory.numerify('##########'),
            'phoneNumber': self.data_factory.numerify('##########'),
            'mobileNumber': self.data_factory.numerify('##########'),
            'city': self.data_factory.city(),
            'state': self.data_factory.state(),
            'country': self.data_factory.country(),
            'address': self.data_factory.address(),
        }
        # Update a nonexistent company
        response = self.client.put(f'/user/company/abc', json=updated_company, headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Field is missing')

def generate_string_random(length):
    import string
    import random
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
