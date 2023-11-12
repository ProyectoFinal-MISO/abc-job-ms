from flask_restful import Resource
from modelos.modelos import db, TeamProject, MembersTeamProject, Role
from utils.get_details_objects import get_role_detail
from flask import request, Response

class VistaMembersTeamProjectCreate(Resource):
    def post(self):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            if not parse_json.get('teamId', None) or not parse_json.get('userId', None) or not parse_json.get('isIntern', None) or not parse_json.get('role', None):
                return {'mensaje': 'Field is missing'}, 400
            team = TeamProject.query.filter_by(id=parse_json.get('teamId', None)).first()
            if not team:
                return {'mensaje': 'Team not exist'}, 404
            role = Role.query.filter_by(id=parse_json.get('role', None)).first()
            if not role:
                return {'mensaje': 'Role not exist'}, 404
            new_member = MembersTeamProject(
                teamId = parse_json.get('teamId', None),
                userId = parse_json.get('userId', None),
                isIntern = parse_json.get('isIntern', None),
                role = parse_json.get('role', None)
            )
            db.session.add(new_member)
            db.session.commit()
            return {
                "id": new_member.id,
            }, 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "Error": e
            }, 400

class VistaMembersTeamProject(Resource):
    def get(self, id_member):
        try:
            id_member = int(id_member)
        except ValueError:
            return {'mensaje': 'Member id is not integer'}, 400
        team = MembersTeamProject.query.filter_by(id=id_member).first()
        if team:
            return {
                'id': team.id,
                'teamId': team.teamId,
                'userId': team.userId,
                'isIntern': team.isIntern,
                'role': get_role_detail(team.role)
            }, 200
        else:
            return {'mensaje': 'Member not exist'}, 404

    def delete(self, id_member):
        try:
            id_member = int(id_member)
        except ValueError:
            return {'mensaje': 'Member id is not integer'}, 400
        team = MembersTeamProject.query.filter_by(id=id_member).first()
        if team:
            db.session.delete(team)
            db.session.commit()
            return {'mensaje': 'Member deleted'}, 200
        else:
            return {'mensaje': 'Member not exist'}, 404

    def put(self, id_member):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            if not parse_json.get('teamId', None) or not parse_json.get('userId', None) or not parse_json.get('isIntern', None) or not parse_json.get('role', None):
                return {'mensaje': 'Field is missing'}, 400
            team = TeamProject.query.filter_by(id=parse_json.get('teamId', None)).first()
            if not team:
                return {'mensaje': 'Member not exist'}, 404
            role = Role.query.filter_by(id=parse_json.get('role', None)).first()
            if not role:
                return {'mensaje': 'Role not exist'}, 404
            try:
                id_member = int(id_member)
            except ValueError:
                return {'mensaje': 'Member id is not integer'}, 400
            member = MembersTeamProject.query.filter_by(id=id_member).first()
            if member:
                member.teamId = parse_json.get('teamId', None),
                member.userId = parse_json.get('userId', None)
                member.isIntern = parse_json.get('isIntern', None)
                member.role = parse_json.get('role', None)
                db.session.commit()
                return {'mensaje': 'Member was updated'}, 200
            else:
                return {'mensaje': 'Member not exist'}, 404
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "Error": e
            }, 400

class VistaMembersTeamProjectList(Resource):
    def get(self):
        members = MembersTeamProject.query.all()
        if members:
            return {
                "members": [
                    {
                        'id': member.id,
                        'teamId': member.teamId,
                        'userId': member.userId,
                        'isIntern': member.isIntern,
                        'role': get_role_detail(member.role)
                    } for member in members
                ]
            }, 200
        else:
            return {'mensaje': 'Members not exist'}, 204

class VistaMembersTeamProjectByTeamId(Resource):
    def get(self, id_team):
        try:
            id_team = int(id_team)
        except ValueError:
            return {'mensaje': 'Team id is not integer'}, 400
        team = TeamProject.query.filter_by(id=id_team).first()
        if not team:
            return {'mensaje': 'Team not exist'}, 404
        members = MembersTeamProject.query.filter_by(teamId=id_team).all()
        if members:
            return {
                "members": [
                    {
                        'id': member.id,
                        'teamId': member.teamId,
                        'userId': member.userId,
                        'isIntern': member.isIntern,
                        'role': get_role_detail(member.role)
                    } for member in members
                ]
            }, 200
        else:
            return {'mensaje': 'Members not exist'}, 204
