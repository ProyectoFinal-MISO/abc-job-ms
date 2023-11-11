from flask_restful import Resource
from modelos.modelos import db, Project
from flask import request, Response
from flask_jwt_extended import jwt_required
from enum import Enum

import json

class VistaProjectCreate(Resource):
    def post(self):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            if not not parse_json.get('name', None) or not not parse_json.get('companyId', None) or not not parse_json.get('details', None):
                return {'mensaje': 'Field is missing'}, 400
            project = Project.query.filter_by(name=parse_json.get('name', None)).first()
            if not project:
                new_project = Project(
                    name=parse_json.get('name', None),
                    companyId=parse_json.get('companyId', None),
                    details=parse_json.get('details', None)
                )
                db.session.add(new_project)
                db.session.commit()
                return {
                    "id": new_project.id,
                }, 201
            else:
                return {'mensaje': 'Project name already exists'}, 400
        except Exception as e:
            db.session.rollback()
            return {
                "Error": e
            }, 400

class VistaProject(Resource):
    def get(self, id_project):
        try:
            id_project = int(id_project)
        except ValueError:
            return {'mensaje': 'Project id is not integer'}, 400
        project = Project.query.filter_by(id=id_project).first()
        if project:
            return {
                'id': project.id,
                'name': project.name,
                'companyId': project.companyId,
                'details': project.details
            }, 200
        else:
            return {'mensaje': 'Project not exist'}, 404

    def delete(self, id_project):
        try:
            id_project = int(id_project)
        except ValueError:
            return {'mensaje': 'Project id is not integer'}, 400
        project = Project.query.filter_by(id=id_project).first()
        if project:
            db.session.delete(project)
            db.session.commit()
            return {'mensaje': 'Project deleted'}, 200
        else:
            return {'mensaje': 'Project not exist'}, 404

    def put(self, id_project):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            try:
                id_project = int(id_project)
            except ValueError:
                return {'mensaje': 'Project id is not integer'}, 400
            parse_json = request.get_json()
            if not parse_json.get('name', None) or not parse_json.get('companyId', None) or not parse_json.get('details', None):
                return {'mensaje': 'Field is missing'}, 400
            name_project = Project.query.filter_by(name=parse_json.get('name', None)).first()
            if not name_project:
                project = Project.query.filter_by(id=id_project).first()
                if project:
                    project.name = parse_json.get('name', None)
                    project.companyId = parse_json.get('companyId', None)
                    project.details = parse_json.get('details', None)
                    db.session.commit()
                    return {'mensaje': 'Project was updated'}, 200
                else:
                    return {'mensaje': 'Project not exist'}, 404
            else:
                return {'mensaje': 'Project name already exists'}, 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "Error": e
            }, 400

class VistaProjectList(Resource):
    def get(self):
        projects = Project.query.all()
        projects_list = []
        for project in projects:
            projects_list.append({
                'id': project.id,
                'name': project.name,
                'companyId': project.companyId,
                'details': project.details
            })
        return projects_list, 200

class VistaProjectListByCompanyId(Resource):
    def get(self, id_company):
        try:
            id_company = int(id_company)
        except ValueError:
            return {'mensaje': 'Company id is not integer'}, 400

        print('qqqqqqq')

        projects = Project.query.filter_by(companyId=id_company).all()
        if projects:
            projects_list = []
            for project in projects:
                projects_list.append({
                    'id': project.id,
                    'name': project.name,
                    'companyId': project.companyId,
                    'details': project.details
                })
            return projects_list, 200
        else:
            return {'mensaje': 'Projects not exist'}, 204
