import json
from unittest import TestCase
from unittest.mock import patch

from application import application
from modelos.modelos import db, Project

from utils.utils import generate_string_random

class TestVistaProjectCreate(TestCase):

    def setUp(self):
        self.headers = {}
        self.client = application.test_client()
        application.app_context().push()

    def test_create_project(self):
        # Create a fake project
        project_data = {
            "name": "Project1" + generate_string_random(5),
            "companyId": 1,
            "details": "Details1"
        }

        # Make a request to create the project
        response = self.client.post("/projects", headers=self.headers, json=project_data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertIsInstance(response.json["id"], int)

        # Check that the project was created in the database
        project = Project.query.filter_by(name=project_data["name"]).first()
        self.assertIsNotNone(project)
        self.assertEqual(project.companyId, project_data["companyId"])
        self.assertEqual(project.details, project_data["details"])

    def test_create_project_missing_fields(self):
        # Create a fake project with missing fields
        project_data = {
            "name": "Project1" + generate_string_random(5),
            "companyId": 1
        }

        # Make a request to create the project
        response = self.client.post("/projects", headers=self.headers, json=project_data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn("mensaje", response.json)

    def test_create_project_duplicate_name(self):
        # Create a fake project with a duplicate name
        project_data = {
            "name": "Project1" + generate_string_random(5),
            "companyId": 1,
            "details": "Details1"
        }
        project = Project(
            name=project_data["name"],
            companyId=project_data["companyId"],
            details=project_data["details"]
        )
        db.session.add(project)
        db.session.commit()

        # Make a request to create the project
        response = self.client.post("/projects", headers=self.headers, json=project_data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn("mensaje", response.json)

class TestVistaProject(TestCase):

    def setUp(self):
        self.headers = {}
        self.client = application.test_client()
        application.app_context().push()

    def test_get_project(self):
        # Create a fake project
        project_data = {
            "name": "Project1" + generate_string_random(5),
            "companyId": 1,
            "details": "Details1"
        }
        project = Project(
            name=project_data["name"],
            companyId=project_data["companyId"],
            details=project_data["details"]
        )
        db.session.add(project)
        db.session.commit()

        # Make a request to get the project
        response = self.client.get(f"/projects/{project.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], project.id)
        self.assertEqual(response.json["name"], project.name)
        self.assertEqual(response.json["companyId"], project.companyId)
        self.assertEqual(response.json["details"], project.details)

    def test_get_project_nonexistent(self):
        # Make a request to get a nonexistent project
        response = self.client.get("/projects/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn("mensaje", response.json)

    def test_delete_project(self):
        # Create a fake project
        project_data = {
            "name": "Project1" + generate_string_random(5),
            "companyId": 1,
            "details": "Details1"
        }
        project = Project(
            name=project_data["name"],
            companyId=project_data["companyId"],
            details=project_data["details"]
        )
        db.session.add(project)
        db.session.commit()

        # Make a request to delete the project
        response = self.client.delete(f"/projects/{project.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensaje", response.json)

        # Check that the project was deleted from the database
        project = Project.query.filter_by(id=project.id).first()
        self.assertIsNone(project)

    def test_delete_project_nonexistent(self):
        # Make a request to delete a nonexistent project
        response = self.client.delete("/projects/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn("mensaje", response.json)

    def test_update_project(self):
        # Create a fake project
        project_data = {
            "name": "Project1" + generate_string_random(5),
            "companyId": 1,
            "details": "Details1"
        }
        project = Project(
            name=project_data["name"],
            companyId=project_data["companyId"],
            details=project_data["details"]
        )
        db.session.add(project)
        db.session.commit()

        # Update the project
        new_project_data = {
            "name": "Project2" + generate_string_random(5),
            "companyId": 2,
            "details": "Details2"
        }
        response = self.client.put(f"/projects/{project.id}", headers=self.headers, json=new_project_data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensaje", response.json)

        # Check that the project was updated in the database
        updated_project = Project.query.filter_by(id=project.id).first()
        self.assertEqual(updated_project.name, new_project_data["name"])
        self.assertEqual(updated_project.companyId, new_project_data["companyId"])
        self.assertEqual(updated_project.details, new_project_data["details"])

    def test_update_project_missing_fields(self):
        # Create a fake project
        project_data = {
            "name": "Project1" + generate_string_random(5),
            "companyId": 1,
            "details": "Details1"
        }
        project = Project(
            name=project_data["name"],
            companyId=project_data["companyId"],
            details=project_data["details"]
        )
        db.session.add(project)
        db.session.commit()

        # Update the project with missing fields
        new_project_data = {
            "name": "Project2" + generate_string_random(5),
            "companyId": 2
        }
        response = self.client.put(f"/projects/{project.id}", headers=self.headers, json=new_project_data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn("mensaje", response.json)

        # Check that the project was not updated in the database
        updated_project = Project.query.filter_by(id=project.id).first()
        self.assertEqual(updated_project.name, project_data["name"])
        self.assertEqual(updated_project.companyId, project_data["companyId"])
        self.assertEqual(updated_project.details, project_data["details"])

    def test_update_project_duplicate_name(self):
        name = "Project1" + generate_string_random(5)
        # Create two fake projects
        project1_data = {
            "name": name,
            "companyId": 1,
            "details": "Details1"
        }
        project1 = Project(
            name=project1_data["name"],
            companyId=project1_data["companyId"],
            details=project1_data["details"]
        )
        db.session.add(project1)
        project2_data = {
            "name": "Project2" + generate_string_random(5),
            "companyId": 1,
            "details": "Details2"
        }
        project2 = Project(
            name=project2_data["name"],
            companyId=project2_data["companyId"],
            details=project2_data["details"]
        )
        db.session.add(project2)
        db.session.commit()

        # Update the second project to have the same name as the first project
        new_project_data = {
            "name": name,
            "companyId": 2,
            "details": "Details2"
        }
        response = self.client.put(f"/projects/{project2.id}", headers=self.headers, json=new_project_data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn("mensaje", response.json)

        # Check that the project was not updated in the database
        updated_project = Project.query.filter_by(id=project2.id).first()
        self.assertEqual(updated_project.name, project2_data["name"])
        self.assertEqual(updated_project.companyId, project2_data["companyId"])
        self.assertEqual(updated_project.details, project2_data["details"])

    def test_update_project_nonexistent(self):
        # Update a nonexistent project
        new_project_data = {
            "name": "Project2" + generate_string_random(5),
            "companyId": 2,
            "details": "Details2"
        }
        response = self.client.put("/projects/999", headers=self.headers, json=new_project_data)

         # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn("mensaje", response.json)

class TestVistaProjectList(TestCase):
    def setUp(self):
        self.client = application.test_client()
        application.app_context().push()

    def test_get_projects(self):
        # Create some fake projects
        project1 = Project(name="Project1" + generate_string_random(5), companyId=1, details="Details1")
        project2 = Project(name="Project2" + generate_string_random(5), companyId=2, details="Details2")
        db.session.add_all([project1, project2])
        db.session.commit()

        # Make a request to get the projects
        response = self.client.get("/projects/list")

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)

class TestVistaProjectListByCompanyId(TestCase):
    def setUp(self):
        self.client = application.test_client()
        application.app_context().push()

    def test_get_projects_by_company_id(self):
        # Create fake projects for the company
        name1 = "Project1" + generate_string_random(5)
        project1_data = {
            "name": name1,
            "companyId": 1,
            "details": "Details1"
        }
        project1 = Project(
            name=project1_data["name"],
            companyId=project1_data["companyId"],
            details=project1_data["details"]
        )
        db.session.add(project1)
        name2 = "Project2" + generate_string_random(5)
        project2_data = {
            "name": name2,
            "companyId": 1,
            "details": "Details2"
        }
        project2 = Project(
            name=project2_data["name"],
            companyId=project2_data["companyId"],
            details=project2_data["details"]
        )
        db.session.add(project2)
        db.session.commit()

        # Make a request to get the projects for the company
        response = self.client.get(f"projects/company/1")

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_projects_by_company_id_nonexistent_company(self):
        # Make a request to get the projects for a nonexistent company
        response = self.client.get("/projects/company/999")

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn("mensaje", response.json)
