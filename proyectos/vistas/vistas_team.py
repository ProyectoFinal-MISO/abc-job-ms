from flask_restful import Resource
from modelos.modelos import db, TeamProject, Project
from utils.get_details_objects import get_members_team
from flask import request, Response

class VistaTeamProjectCreate(Resource):
    def post(self):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            if not parse_json.get('name', None) or not parse_json.get('projectId', None):
                return {'mensaje': 'Field is missing'}, 400
            name_team = TeamProject.query.filter_by(name=parse_json.get('name', None)).first()
            if name_team:
                return {'mensaje': 'Team name already exists'}, 400
            project = Project.query.filter_by(id=parse_json.get('projectId', None)).first()
            if not project:
                return {'mensaje': 'Project not exist'}, 404
            new_team = TeamProject(
                name=parse_json.get('name', None),
                projectId=parse_json.get('projectId', None)
            )
            db.session.add(new_team)
            db.session.commit()
            return {
                "id": new_team.id,
            }, 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "Error": e
            }, 400

class VistaTeamProject(Resource):
    def get(self, id_team):
        try:
            id_team = int(id_team)
        except ValueError:
            return {'mensaje': 'Team id is not integer'}, 400
        team = TeamProject.query.filter_by(id=id_team).first()
        if team:
            return {
                'id': team.id,
                'name': team.name,
                'projectId': team.projectId,
                'members': get_members_team(team.id)
            }, 200
        else:
            return {'mensaje': 'Team not exist'}, 404

    def delete(self, id_team):
        try:
            id_team = int(id_team)
        except ValueError:
            return {'mensaje': 'Team id is not integer'}, 400
        team = TeamProject.query.filter_by(id=id_team).first()
        if team:
            db.session.delete(team)
            db.session.commit()
            return {'mensaje': 'Team deleted'}, 200
        else:
            return {'mensaje': 'Team not exist'}, 404

    def put(self, id_team):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            if not parse_json.get('name', None) or not parse_json.get('projectId', None):
                return {'mensaje': 'Field is missing'}, 400
            name_team = TeamProject.query.filter_by(name=parse_json.get('name', None)).first()
            if name_team:
                return {'mensaje': 'Team name already exists'}, 400
            project = Project.query.filter_by(id=parse_json.get('projectId', None)).first()
            if not project:
                return {'mensaje': 'Project not exist'}, 404
            try:
                id_team = int(id_team)
            except ValueError:
                return {'mensaje': 'Team id is not integer'}, 400
            team = TeamProject.query.filter_by(id=id_team).first()
            if team:
                team.name = parse_json.get('name', None)
                team.projectId = parse_json.get('projectId', None)
                db.session.commit()
                return {'mensaje': 'Team was updated'}, 200
            else:
                return {'mensaje': 'Team not exist'}, 404
        except Exception as e:
            db.session.rollback()
            return {
                "Error": e
            }, 400

class VistaTeamProjectList(Resource):
    def get(self):
        teams = TeamProject.query.all()
        if teams:
            return {
                "teams": [
                    {
                        'id': team.id,
                        'name': team.name,
                        'projectId': team.projectId,
                        'members': get_members_team(team.id)
                    } for team in teams
                ]
            }, 200
        else:
            return {'mensaje': 'Teams not exist'}, 204

class VistaTeamProjectByProjectId(Resource):
    def get(self, id_project):
        try:
            id_project = int(id_project)
        except ValueError:
            return {'mensaje': 'Project id is not integer'}, 400
        project = Project.query.filter_by(id=id_project).first()
        if not project:
            return {'mensaje': 'Project not exist'}, 404
        teams = TeamProject.query.filter_by(projectId=id_project).all()
        if teams:
            return {
                "teams": [
                    {
                        'id': team.id,
                        'name': team.name,
                        'projectId': team.projectId,
                        'members': get_members_team(team.id)
                    } for team in teams
                ]
            }, 200
        else:
            return {'mensaje': 'Teams not exist'}, 204
