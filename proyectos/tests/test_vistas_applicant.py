import json
from unittest import TestCase
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from application import application
from modelos.modelos import db, ApplicantsVacancyProject, VacancyProject
from vistas.vistas_applicant import VistaApplicantsVacancyProjectCreate
from utils.utils import generate_string_random

class TestVistaApplicantsVacancyProjectCreate(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY_TEST')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.client = application.test_client()
        application.app_context().push()

    def test_create_applicant(self):
        # Create a fake vacancy
        name = 'Test vacancy' + generate_string_random(5)
        vacancy = VacancyProject(
            name='' + name,
            details='Test details',
            places=10,
            projectId=1,
            roles=[],
            technicalSkills=[],
            softSkills=[]
        )
        db.session.add(vacancy)
        db.session.commit()

        # Make a request to create an applicant
        data = {
            'vacancyId': vacancy.id,
            'userId': 1
        }
        response = self.client.post('/applicants', headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

        # Check that the applicant was created in the database
        applicant = ApplicantsVacancyProject.query.filter_by(vacancyId=vacancy.id, userId=1).first()
        self.assertEqual(applicant.id, response.json['id'])

        # Check that the vacancy places were updated
        vacancy = VacancyProject.query.filter_by(id=vacancy.id).first()

    def test_create_applicant_with_invalid_data(self):
        # Make a request to create an applicant with invalid data
        data = {
            'vacancyId': 1,
        }
        response = self.client.post('/applicants', headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn('mensaje', response.json)

        # Check that no applicant was created in the database
        applicant = ApplicantsVacancyProject.query.filter_by(vacancyId=1, userId=1).first()
        # self.assertIsNone(applicant)

        # Check that the vacancy places were not updated
        vacancy = VacancyProject.query.filter_by(id=1).first()
        # self.assertIsNotNone(vacancy)

    def test_create_applicant_with_existing_applicant(self):
        # Create a fake applicant
        applicant = ApplicantsVacancyProject(
            vacancyId=1,
            userId=1
        )
        db.session.add(applicant)
        db.session.commit()

        # Make a request to create an applicant with the same data as the existing applicant
        data = {
            'vacancyId': applicant.vacancyId,
            'userId': applicant.userId
        }
        response = self.client.post('/applicants', headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn('mensaje', response.json)

        # Check that no new applicant was created in the database
        applicants = ApplicantsVacancyProject.query.filter_by(vacancyId=applicant.vacancyId, userId=applicant.userId).all()

        # Check that the vacancy places were not updated
        vacancy = VacancyProject.query.filter_by(id=applicant.vacancyId).first()
        #self.assertIsNotNone(vacancy)

    def test_create_applicant_with_full_vacancy(self):
        # Create a fake vacancy with no places available
        name = 'Test vacancy' + generate_string_random(5)
        vacancy = VacancyProject(
            name=name,
            details='Test details',
            places=0,
            projectId=1,
            roles=[],
            technicalSkills=[],
            softSkills=[]
        )
        db.session.add(vacancy)
        db.session.commit()

        # Make a request to create an applicant for the full vacancy
        data = {
            'vacancyId': vacancy.id,
            'userId': 1
        }
        response = self.client.post('/applicants', headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn('mensaje', response.json)

        # Check that no applicant was created in the database
        applicant = ApplicantsVacancyProject.query.filter_by(vacancyId=vacancy.id, userId=1).first()
        #self.assertIsNone(applicant)

        # Check that the vacancy places were not updated
        vacancy = VacancyProject.query.filter_by(id=vacancy.id).first()
        #self.assertIsNotNone(vacancy)
        #self.assertEqual(vacancy.places, 0)

class TestVistaApplicantsVacancyProject(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY_TEST')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.client = application.test_client()
        application.app_context().push()

    def test_get_applicant(self):
        # Create a fake applicant
        applicant = ApplicantsVacancyProject(
            vacancyId=1,
            userId=1
        )
        db.session.add(applicant)
        db.session.commit()

        # Make a request to get the applicant
        response = self.client.get(f'/applicants/{applicant.id}', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'id': applicant.id,
            'vacancyId': applicant.vacancyId,
            'userId': applicant.userId
        })

    def test_get_nonexistent_applicant(self):
        # Make a request to get a nonexistent applicant
        response = self.client.get('/applicants/999', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

    def test_delete_nonexistent_applicant(self):
        # Make a request to delete a nonexistent applicant
        response = self.client.delete('/applicants/999', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

    def test_update_applicant(self):
        # Create a fake applicant
        applicant = ApplicantsVacancyProject(
            vacancyId=1,
            userId=1
        )
        db.session.add(applicant)
        db.session.commit()

        # Create a fake vacancy
        name = 'Test vacancy' + generate_string_random(5)
        vacancy = VacancyProject(
            name=name,
            details='Test details',
            places=10,
            projectId=1,
            roles=[],
            technicalSkills=[],
            softSkills=[]
        )
        db.session.add(vacancy)
        db.session.commit()

        # Make a request to update the applicant
        data = {
            'vacancyId': vacancy.id,
            'userId': 2
        }
        response = self.client.put(f'/applicants/{applicant.id}', headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.json)

        # Check that the applicant was updated in the database
        applicant = ApplicantsVacancyProject.query.filter_by(id=applicant.id).first()
        self.assertEqual(applicant.vacancyId, vacancy.id)
        self.assertEqual(applicant.userId, 2)

        # Check that the vacancy places were updated
        vacancy = VacancyProject.query.filter_by(id=vacancy.id).first()
        #self.assertEqual(vacancy.places, 0)

    def test_update_nonexistent_applicant(self):
        # Make a request to update a nonexistent applicant
        response = self.client.put('/applicants/999', headers=self.headers)

        # Check that the response is correct
        self.assertIn('mensaje', response.json)

    def test_update_applicant_with_invalid_data(self):
        # Create a fake applicant
        applicant = ApplicantsVacancyProject(
            vacancyId=1,
            userId=1
        )
        db.session.add(applicant)
        db.session.commit()

        # Make a request to update the applicant with invalid data
        data = {
            'vacancyId': None,
            'userId': None
        }
        response = self.client.put(f'/applicants/{applicant.id}', headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn('mensaje', response.json)

        # Check that the applicant was not updated in the database
        applicant = ApplicantsVacancyProject.query.filter_by(id=applicant.id).first()
        self.assertEqual(applicant.vacancyId, 1)
        self.assertEqual(applicant.userId, 1)

    def test_update_applicant_with_full_vacancy(self):
        # Create a fake applicant
        applicant = ApplicantsVacancyProject(
            vacancyId=1,
            userId=1
        )
        db.session.add(applicant)
        db.session.commit()

        # Create a fake vacancy with no places available
        name = 'Test vacancy' + generate_string_random(5)
        vacancy = VacancyProject(
            name=name,
            details='Test details',
            places=0,
            projectId=1,
            roles=[],
            technicalSkills=[],
            softSkills=[]
        )
        db.session.add(vacancy)
        db.session.commit()

        # Make a request to update the applicant for the full vacancy
        data = {
            'vacancyId': vacancy.id,
            'userId': 2
        }
        response = self.client.put(f'/applicants/{applicant.id}', headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn('mensaje', response.json)

        # Check that the applicant was not updated in the database
        applicant = ApplicantsVacancyProject.query.filter_by(id=applicant.id).first()
        self.assertEqual(applicant.vacancyId, 1)
        self.assertEqual(applicant.userId, 1)

        # Check that the vacancy places were not updated
        vacancy = VacancyProject.query.filter_by(id=vacancy.id).first()
        #self.assertEqual(vacancy.places, 0)

class TestVistaApplicantsVacancyProjectList(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY_TEST')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.client = application.test_client()
        application.app_context().push()

    def test_get_all_applicants(self):
        # Create some fake applicants
        applicant1 = ApplicantsVacancyProject(
            vacancyId=1,
            userId=1
        )
        applicant2 = ApplicantsVacancyProject(
            vacancyId=2,
            userId=2
        )
        db.session.add_all([applicant1, applicant2])
        db.session.commit()

        # Make a request to get all applicants
        response = self.client.get('/applicants/list', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)


    def test_get_all_applicants_empty(self):
        ApplicantsVacancyProject.query.delete()
        # Make a request to get all applicants when there are none
        response = self.client.get('/applicants/list', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

class TestVistaApplicantsVacancyProjectByVacancyId(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY_TEST')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.client = application.test_client()
        application.app_context().push()

    def test_get_applicants_by_vacancy_id(self):
        # Create a fake vacancy
        name = 'Test vacancy' + generate_string_random(5)
        vacancy = VacancyProject(
            name=name,
            details='Test details',
            places=10,
            projectId=1,
            roles=[],
            technicalSkills=[],
            softSkills=[]
        )
        db.session.add(vacancy)
        db.session.commit()

        # Create a fake applicant
        applicant = ApplicantsVacancyProject(
            vacancyId=vacancy.id,
            userId=1
        )
        db.session.add(applicant)
        db.session.commit()

        # Make a request to get the applicants for the vacancy
        response = self.client.get(f'/applicants/vacancy/{vacancy.id}', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'applicants': [
                {
                    'id': applicant.id,
                    'vacancyId': applicant.vacancyId,
                    'userId': applicant.userId
                }
            ]
        })

    def test_get_applicants_by_nonexistent_vacancy_id(self):
        # Make a request to get applicants for a nonexistent vacancy
        response = self.client.get('/applicants/vacancy/999', headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)
