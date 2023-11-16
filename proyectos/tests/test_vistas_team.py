import json
from unittest import TestCase
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from application import application
from modelos.modelos import db, Project, TeamProject
from vistas.vistas_team import VistaTeamProjectCreate

from utils.utils import generate_string_random

class TestVistaTeamProjectCreate(TestCase):

    def setUp(self):
        self.headers = {}
        self.client = application.test_client()
        application.app_context().push()

    def test_post_team_project(self):
        # Create a fake project
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        db.session.commit()

        # Make a request to create a team for the project
        data = {
            "name": "Team1" + generate_string_random(5),
            "projectId": project.id
        }
        response = self.client.post("/teams", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json['id'], int)

        # Check that the team was created in the database
        team = TeamProject.query.filter_by(id=response.json['id']).first()
        self.assertIsNotNone(team)
        self.assertEqual(team.name, data['name'])
        self.assertEqual(team.projectId, data['projectId'])

    def test_post_team_project_missing_fields(self):
        # Make a request to create a team for the project with missing fields
        data = {
            "name": "Team1"
        }
        response = self.client.post("/teams", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['mensaje'], 'Field is missing')

    def test_post_team_project_existing_team_name(self):
        # Create a fake project and team
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        team = TeamProject(
            name="Team1",
            projectId=project.id
        )
        db.session.add(team)
        db.session.commit()

        # Make a request to create a team for the project with an existing team name
        data = {
            "name": "Team1",
            "projectId": project.id
        }
        response = self.client.post("/teams", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['mensaje'], 'Team name already exists')

    def test_post_team_project_nonexistent_project(self):
        # Make a request to create a team for a nonexistent project
        data = {
            "name": "Team1" + generate_string_random(5),
            "projectId": 999
        }
        response = self.client.post("/teams", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

class TestVistaTeamProject(TestCase):

    def setUp(self):
        self.headers = {}
        self.client = application.test_client()
        application.app_context().push()

    def test_get_team_project(self):
        # Create a fake project and team
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        team = TeamProject(
            name="Team1" + generate_string_random(5),
            projectId=project.id
        )
        db.session.add(team)
        db.session.commit()

        # Make a request to get the team
        response = self.client.get(f"/teams/{team.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], team.name)
        self.assertEqual(response.json['projectId'], team.projectId)

    def test_get_team_project_nonexistent_team(self):
        # Make a request to get a nonexistent team
        response = self.client.get("/teams/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

    def test_delete_team_project(self):
        # Create a fake project and team
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        team = TeamProject(
            name="Team1" + generate_string_random(5),
            projectId=project.id
        )
        db.session.add(team)
        db.session.commit()

        # Make a request to delete the team
        response = self.client.delete(f"/teams/{team.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mensaje'], 'Team deleted')

        # Check that the team was deleted from the database
        team = TeamProject.query.filter_by(id=team.id).first()
        self.assertIsNone(team)

    def test_delete_team_project_nonexistent_team(self):
        # Make a request to delete a nonexistent team
        response = self.client.delete("/teams/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

    def test_put_team_project(self):
        # Create a fake project and team
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        team = TeamProject(
            name="Team1" + generate_string_random(5),
            projectId=project.id
        )
        db.session.add(team)
        db.session.commit()

        # Make a request to update the team
        data = {
            "name": "Team2" + generate_string_random(5),
            "projectId": project.id
        }
        response = self.client.put(f"/teams/{team.id}", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mensaje'], 'Team was updated')

        # Check that the team was updated in the database
        team = TeamProject.query.filter_by(id=team.id).first()
        self.assertIsNotNone(team)
        self.assertEqual(team.name, data['name'])
        self.assertEqual(team.projectId, data['projectId'])

    def test_put_team_project_missing_fields(self):
        # Create a fake project and team
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        team = TeamProject(
            name="Team1" + generate_string_random(5),
            projectId=project.id
        )
        db.session.add(team)
        db.session.commit()

        # Make a request to update the team with missing fields
        data = {
            "name": "Team2"
        }
        response = self.client.put(f"/teams/{team.id}", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['mensaje'], 'Field is missing')

        # Check that the team was not updated in the database
        team = TeamProject.query.filter_by(id=team.id).first()
        self.assertIsNotNone(team)

    def test_put_team_project_existing_team_name(self):
        # Create a fake project and team
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        team1 = TeamProject(
            name="Team3",
            projectId=project.id
        )
        db.session.add(team1)
        team2 = TeamProject(
            name="Team2",
            projectId=project.id
        )
        db.session.add(team2)
        db.session.commit()

        # Make a request to update the team with an existing team name
        data = {
            "name": "Team3",
            "projectId": project.id
        }
        response = self.client.put(f"/teams/{team2.id}", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['mensaje'], 'Team name already exists')

        # Check that the team was not updated in the database
        team2 = TeamProject.query.filter_by(id=team2.id).first()
        self.assertIsNotNone(team2)
        self.assertEqual(team2.name, "Team2")

    def test_put_team_project_nonexistent_team(self):
        # Make a request to update a nonexistent team
        data = {
            "name": "Team2" + generate_string_random(5),
            "projectId": 999
        }
        response = self.client.put("/teams/999", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

    def test_put_team_project_nonexistent_project(self):
        # Create a fake project and team
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        team = TeamProject(
            name="Team1" + generate_string_random(5),
            projectId=project.id
        )
        db.session.add(team)
        db.session.commit()

        # Make a request to update the team with a nonexistent project
        data = {
            "name": "Team2" + generate_string_random(5),
            "projectId": 999
        }
        response = self.client.put(f"/teams/{team.id}", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

        # Check that the team was not updated in the database
        team = TeamProject.query.filter_by(id=team.id).first()
        self.assertIsNotNone(team)

class TestVistaTeamProjectList(TestCase):
    def setUp(self):
        self.headers = {}
        self.client = application.test_client()
        application.app_context().push()

    def test_get_team_project_list(self):
        # Create a fake project and team
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        team = TeamProject(
            name="Team1" + generate_string_random(5),
            projectId=project.id
        )
        db.session.add(team)
        db.session.commit()

        # Make a request to get the team list
        response = self.client.get("/teams/list", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)

    def test_get_team_project_list_empty(self):
        TeamProject.query.delete()
        # Make a request to get an empty team list
        response = self.client.get("/teams/list", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 204)

class TestVistaTeamProjectByProjectId(TestCase):

    def setUp(self):
        self.headers = {}
        self.client = application.test_client()
        application.app_context().push()

    # def test_get_teams_by_project_id(self):
    #     # Create a fake project and teams
    #     project = Project(
    #         name="Project1" + generate_string_random(5),
    #         companyId=1,
    #         details="Details1"
    #     )
    #     db.session.add(project)
    #     team1 = TeamProject(
    #         name="Team1" + generate_string_random(5),
    #         projectId=project.id
    #     )
    #     db.session.add(team1)
    #     team2 = TeamProject(
    #         name="Team2" + generate_string_random(5),
    #         projectId=project.id
    #     )
    #     db.session.add(team2)
    #     db.session.commit()

    #     # Make a request to get the teams for the project
    #     response = self.client.get(f"/teams/project/{project.id}", headers=self.headers)

    #     # Check that the response is correct
    #     self.assertEqual(response.json['teams'][0]['projectId'], team1.projectId)
    #     self.assertEqual(response.json['teams'][1]['projectId'], team2.projectId)

    def test_get_teams_by_project_id_nonexistent_project(self):
        # Make a request to get teams for a nonexistent project
        response = self.client.get("/teams/project/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

    def test_get_teams_by_project_id_no_teams(self):
        # Create a fake project with no teams
        project = Project(
            name="Project1" + generate_string_random(5),
            companyId=1,
            details="Details1"
        )
        db.session.add(project)
        db.session.commit()

        # Make a request to get the teams for the project
        response = self.client.get(f"/teams/project/{project.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 204)
