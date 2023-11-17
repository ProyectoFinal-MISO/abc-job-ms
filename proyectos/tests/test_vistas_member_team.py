import json
from unittest import TestCase
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from application import application
from modelos.modelos import db, MembersTeamProject, Role, TeamProject
from vistas.vistas_member_team import VistaMembersTeamProjectCreate

from utils.utils import generate_string_random
from utils.get_details_objects import get_role_detail

class TestVistaMembersTeamProjectCreate(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY_TEST')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.client = application.test_client()
        application.app_context().push()

    def test_post_members(self):
        # Create a fake team
        team = TeamProject(
            name = "Team1" + generate_string_random(5),
            projectId = 1
        )
        db.session.add(team)
        db.session.commit()

        # Create a fake role
        role = Role(
            name = "Role1" + generate_string_random(5)
        )
        db.session.add(role)
        db.session.commit()

        # Make a request to create a new member
        data = {
            "teamId": team.id,
            "userId": 1,
            "isIntern": True,
            "role": role.id
        }
        response = self.client.post("/members", headers=self.headers, json=data)

        # Check that the response is correct
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json['id'], int)

class TestVistaMembersTeamProject(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY_TEST')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.client = application.test_client()
        application.app_context().push()

    def test_get_member(self):
        # Create a fake member
        member = MembersTeamProject(
            teamId=1,
            userId=1,
            isIntern=True,
            role=1
        )
        db.session.add(member)
        db.session.commit()

        # Make a request to get the member
        response = self.client.get(f"/members/{member.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['teamId'], member.teamId)
        self.assertEqual(response.json['userId'], member.userId)
        self.assertEqual(response.json['isIntern'], member.isIntern)

    def test_get_member_not_exist(self):
        # Make a request to get a member that does not exist
        response = self.client.get("/members/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

    def test_delete_member(self):
        # Create a fake member
        member = MembersTeamProject(
            teamId=1,
            userId=1,
            isIntern=True,
            role=1
        )
        db.session.add(member)
        db.session.commit()

        # Make a request to delete the member
        response = self.client.delete(f"/members/{member.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.json)

    def test_delete_member_not_exist(self):
        # Make a request to delete a member that does not exist
        response = self.client.delete("/members/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

    # def test_put_member(self):
    #     # Create a fake member
    #     member = MembersTeamProject(
    #         teamId=1,
    #         userId=1,
    #         isIntern=True,
    #         role=1
    #     )
    #     db.session.add(member)
    #     db.session.commit()

    #     # Create a fake team
    #     team = TeamProject(
    #         name = "Team1" + generate_string_random(5),
    #         projectId = 1
    #     )
    #     db.session.add(team)
    #     db.session.commit()

    #     # Create a fake role
    #     role = Role(
    #         name = "Role1" + generate_string_random(5)
    #     )
    #     db.session.add(role)
    #     db.session.commit()

    #     # Make a request to update the member
    #     data = {
    #         "teamId": team.id,
    #         "userId": 2,
    #         "isIntern": 0,
    #         "role": role.id
    #     }
    #     response = self.client.put(f"/members/{member.id}", headers=self.headers, json=data)

    #     # Check that the response is correct
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('mensaje', response.json)
    #     updated_member = MembersTeamProject.query.filter_by(id=member.id).first()
    #     self.assertEqual(updated_member.userId, 2)
    #     self.assertEqual(updated_member.isIntern, 0)

    # def test_put_member_missing_fields(self):
    #     # Create a fake member
    #     member = MembersTeamProject(
    #         teamId=1,
    #         userId=1,
    #         isIntern=True,
    #         role=1
    #     )
    #     db.session.add(member)
    #     db.session.commit()

    #     # Make a request to update the member with missing fields
    #     data = {
    #         "teamId": 1,
    #         "userId": 2,
    #         "isIntern": 0
    #     }
    #     response = self.client.put(f"/members/{member.id}", headers=self.headers, json=data)

    #     # Check that the response is correct
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn('mensaje', response.json)

    # def test_put_member_team_not_exist(self):
    #     # Create a fake member
    #     member = MembersTeamProject(
    #         teamId=1,
    #         userId=1,
    #         isIntern=True,
    #         role=1
    #     )
    #     db.session.add(member)
    #     db.session.commit()

    #     # Make a request to update the member with a non-existent team
    #     data = {
    #         "teamId": 999,
    #         "userId": 2,
    #         "isIntern": 0,
    #         "role": 1
    #     }
    #     response = self.client.put(f"/members/{member.id}", headers=self.headers, json=data)

    #     # Check that the response is correct
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn('mensaje', response.json)

    # def test_put_member_role_not_exist(self):
    #     # Create a fake member
    #     member = MembersTeamProject(
    #         teamId=1,
    #         userId=1,
    #         isIntern=True,
    #         role=1
    #     )
    #     db.session.add(member)
    #     db.session.commit()

    #     # Create a fake team
    #     team = TeamProject(
    #         name = "Team1" + generate_string_random(5),
    #         projectId = 1
    #     )
    #     db.session.add(team)
    #     db.session.commit()

    #     # Make a request to update the member with a non-existent role
    #     data = {
    #         "teamId": team.id,
    #         "userId": 2,
    #         "isIntern": 0,
    #         "role": 999
    #     }
    #     response = self.client.put(f"/members/{member.id}", headers=self.headers, json=data)

    #     # Check that the response is correct
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn('mensaje', response.json)

    # def test_put_member_not_exist(self):
    #     # Create a fake team
    #     team = TeamProject(
    #         name = "Team1" + generate_string_random(5),
    #         projectId = 1
    #     )
    #     db.session.add(team)
    #     db.session.commit()

    #     # Create a fake role
    #     role = Role(
    #         name = "Role1" + generate_string_random(5)
    #     )
    #     db.session.add(role)
    #     db.session.commit()

    #     # Make a request to update a member that does not exist
    #     data = {
    #         "teamId": team.id,
    #         "userId": 2,
    #         "isIntern": 0,
    #         "role": role.id
    #     }
    #     response = self.client.put("/members/999", headers=self.headers, json=data)

    #     # Check that the response is correct
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn('mensaje', response.json)

class TestVistaMembersTeamProjectList(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY_TEST')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.client = application.test_client()
        application.app_context().push()

    def test_get_members(self):
        # Create a fake member
        member = MembersTeamProject(
            teamId=1,
            userId=1,
            isIntern=True,
            role=1
        )
        db.session.add(member)
        db.session.commit()

        # Make a request to get all members
        response = self.client.get("/members/list", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['members'][0]['teamId'], member.teamId)
        self.assertEqual(response.json['members'][0]['userId'], member.userId)
        self.assertEqual(response.json['members'][0]['isIntern'], member.isIntern)

    def test_get_members_empty(self):
        MembersTeamProject.query.delete()
        # Make a request to get all members when there are none
        response = self.client.get("/members/list", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 204)

class TestVistaMembersTeamProjectByTeamId(TestCase):

    def setUp(self):
        token = create_access_token(identity='JWT_SECRET_KEY_TEST')
        self.headers = {'Authorization': 'Bearer ' + token}
        self.client = application.test_client()
        application.app_context().push()

    def test_get_members_by_team_id(self):
        # Create a fake team
        team = TeamProject(
            name = "Team1" + generate_string_random(5),
            projectId = 1
        )
        db.session.add(team)
        db.session.commit()

        # Create fake members
        member1 = MembersTeamProject(
            teamId=team.id,
            userId=1,
            isIntern=True,
            role=1
        )
        member2 = MembersTeamProject(
            teamId=team.id,
            userId=2,
            isIntern=True,
            role=2
        )
        db.session.add(member1)
        db.session.add(member2)
        db.session.commit()

        # Make a request to get members by team id
        response = self.client.get(f"/members/team/{team.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['members'][0]['teamId'], member1.teamId)
        self.assertEqual(response.json['members'][0]['userId'], member1.userId)
        self.assertEqual(response.json['members'][0]['isIntern'], member1.isIntern)
        self.assertEqual(response.json['members'][1]['teamId'], member2.teamId)
        self.assertEqual(response.json['members'][1]['userId'], member2.userId)
        self.assertEqual(response.json['members'][1]['isIntern'], member2.isIntern)

    def test_get_members_by_team_id_not_exist(self):
        # Make a request to get members for a team that does not exist
        response = self.client.get("/members/team/999", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn('mensaje', response.json)

    def test_get_members_by_team_id_no_members(self):
        # Create a fake team
        team = TeamProject(
            name = "Team1" + generate_string_random(5),
            projectId = 1
        )
        db.session.add(team)
        db.session.commit()

        # Make a request to get members for a team with no members
        response = self.client.get(f"/members/team/{team.id}", headers=self.headers)

        # Check that the response is correct
        self.assertEqual(response.status_code, 204)
