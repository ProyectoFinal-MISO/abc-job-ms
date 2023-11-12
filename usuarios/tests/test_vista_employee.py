import json
from unittest import TestCase
from unittest.mock import patch

from faker import Faker
from faker.generator import random

from flask_jwt_extended import create_access_token

from application import application
from modelos.modelos import db, TypeIdentification, Employee
from vistas.employees import VistaEmployee


class TestEmployees(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY_TEST')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.data_factory = Faker()
        self.client = application.test_client()
        application.app_context().push()



    def test_get_employee(self):
        # Create a fake employee
        employee = Employee(
            userId=1,
            name=self.data_factory.name(),
            lastName=self.data_factory.last_name(),
            typeIdentification=TypeIdentification.CC,
            identification=self.data_factory.random_number(digits=9),
            phoneNumber=self.data_factory.phone_number(),
            mobileNumber=self.data_factory.phone_number(),
            city=self.data_factory.city(),
            state=self.data_factory.state(),
            country=self.data_factory.country(),
            address=self.data_factory.address(),
            photo=self.data_factory.file_name(category='image', extension='png'),
        )
        db.session.add(employee)
        db.session.commit()

        # Make a request to get the employee
        response = self.client.get(f"/users/employee/{employee.userId}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)

    def test_get_employee_with_non_integer_id(self):
        # Make a request to get a employee with a non-integer id
        response = self.client.get(f"/users/employee/abc", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)

    def test_get_nonexistent_employee(self):

        # Make a request to get a nonexistent employee
        response = self.client.get(f"/users/employee/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)

    def test_delete_employee(self):
        # Create a employee to delete
        employee = Employee(
            userId=1,
            name=self.data_factory.name(),
            lastName=self.data_factory.last_name(),
            typeIdentification=TypeIdentification.CC,
            identification=self.data_factory.random_number(digits=9),
            phoneNumber=self.data_factory.phone_number(),
            mobileNumber=self.data_factory.phone_number(),
            city=self.data_factory.city(),
            state=self.data_factory.state(),
            country=self.data_factory.country(),
            address=self.data_factory.address(),
            photo=self.data_factory.file_name(category='image', extension='png'),
        )
        db.session.add(employee)
        db.session.commit()

        # Delete the employee
        response = self.client.delete(f'/users/employee/{employee.userId}', headers=self.headers)

        # Check that the employee was deleted
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mensaje'], 'Employee deleted')

    def test_delete_nonexistent_employee(self):
        # Delete a nonexistent employee
        response = self.client.delete('/users/employee/999', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['mensaje'], 'Employee not exist')

    def test_delete_employee_with_noninteger_id(self):
        # Delete a employee with a non-integer ID
        response = self.client.delete('/users/employee/abc', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['mensaje'], 'Employee id is not integer')

    def test_put_employee(self):
        # Create a employee to update
        employee = Employee(
            userId=1,
            name=self.data_factory.name(),
            lastName=self.data_factory.last_name(),
            typeIdentification=TypeIdentification.CC,
            identification=self.data_factory.random_number(digits=9),
            phoneNumber=self.data_factory.phone_number(),
            mobileNumber=self.data_factory.phone_number(),
            city=self.data_factory.city(),
            state=self.data_factory.state(),
            country=self.data_factory.country(),
            address=self.data_factory.address(),
            photo=self.data_factory.file_name(category='image', extension='png'),
        )
        db.session.add(employee)
        db.session.commit()

        # Update the employee
        updated_employee = {
            'name': self.data_factory.name(),
            'lastName': self.data_factory.last_name(),
            'typeIdentification': "CC",
            'identification': self.data_factory.numerify('##########'),
            'phoneNumber': self.data_factory.numerify('##########'),
            'mobileNumber': self.data_factory.numerify('##########'),
            'city': self.data_factory.city(),
            'state': self.data_factory.state(),
            'country': self.data_factory.country(),
            'address': self.data_factory.address(),
            'photo': self.data_factory.file_name(category='image', extension='png'),
        }
        response = self.client.put(f'/users/employee/{employee.userId}', json=updated_employee, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        # Check that the employee was updated
        response = self.client.get(f'/users/employee/{employee.userId}', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_update_nonexistent_employee(self):
        # Update the employee
        updated_employee = {
            'name': self.data_factory.name(),
            'lastName': self.data_factory.last_name(),
            'typeIdentification': "CC",
            'identification': self.data_factory.numerify('##########'),
            'phoneNumber': self.data_factory.numerify('##########'),
            'mobileNumber': self.data_factory.numerify('##########'),
            'city': self.data_factory.city(),
            'state': self.data_factory.state(),
            'country': self.data_factory.country(),
            'address': self.data_factory.address(),
            'photo': self.data_factory.file_name(category='image', extension='png'),
        }
        # Update a nonexistent employee
        response = self.client.put(f'/users/employee/999', json=updated_employee, headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['mensaje'], 'Employee not exist')

    def test_update_employee_with_noninteger_id(self):
        # Update the employee
        updated_employee = {
            'name': self.data_factory.name(),
            'lastName' : self.data_factory.last_name(),
            'typeIdentification': "CC",
            'identification': self.data_factory.numerify('##########'),
            'phoneNumber': self.data_factory.numerify('##########'),
            'mobileNumber': self.data_factory.numerify('##########'),
            'city': self.data_factory.city(),
            'state': self.data_factory.state(),
            'country': self.data_factory.country(),
            'address': self.data_factory.address(),
            'photo': self.data_factory.file_name(category='image', extension='png'),
        }
        # Update a nonexistent employee
        response = self.client.put(f'/users/employee/abc', json=updated_employee, headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['mensaje'], 'Employee id is not integer')

    def test_update_employee_with_field_missing(self):
        # Update the employee
        updated_employee = {
            'name': self.data_factory.name(),
            'lastName' : self.data_factory.last_name(),
            'identification': self.data_factory.numerify('##########'),
            'phoneNumber': self.data_factory.numerify('##########'),
            'mobileNumber': self.data_factory.numerify('##########'),
            'city': self.data_factory.city(),
            'state': self.data_factory.state(),
            'country': self.data_factory.country(),
            'address': self.data_factory.address(),
            'photo': self.data_factory.file_name(category='image', extension='png'),
        }
        # Update a nonexistent employee
        response = self.client.put(f'/users/employee/abc', json=updated_employee, headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Field is missing')
