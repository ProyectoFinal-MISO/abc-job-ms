from flask_restful import Resource
from modelos.modelos import db, VacancyProject, Project, Role, TechnicalSkills, SoftSkills, vacancy_role_association
from utils.get_details_objects import get_roles_details, get_technical_skills_details, get_soft_skills_details
from flask import request, Response

import json

class VistaVacancyProjectCreate(Resource):
    def post(self):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            if not parse_json.get('name', None) or not parse_json.get('details', None) or not parse_json.get('places', None) or not parse_json.get('roles', None) or not parse_json.get('technicalSkills', None) or not parse_json.get('softSkills', None):
                return {'mensaje': 'Field is missing'}, 400
            vacacy = VacancyProject.query.filter_by(name=parse_json.get('name', None)).first()
            if vacacy:
                return {'mensaje': 'Vacancy already exist'}, 400
            project = Project.query.filter_by(id=parse_json.get('projectId', None)).first()
            if not project:
                return {'mensaje': 'Project not exist'}, 400
            roles = []
            for role in parse_json.get('roles', None):
                r = Role.query.filter_by(id=role).first()
                if not r:
                    return {'mensaje': 'Role ' + str(role) + ' not exist'}, 400
                roles.append(r)
            technical_skills = []
            for technical_skill in parse_json.get('technicalSkills', None):
                ts = TechnicalSkills.query.filter_by(id=technical_skill).first()
                if not ts:
                    return {'mensaje': 'Technical skill ' + str(technical_skill) + ' not exist'}, 400
                technical_skills.append(ts)
            soft_skills = []
            for soft_skill in parse_json.get('softSkills', None):
                ss = SoftSkills.query.filter_by(id=soft_skill).first()
                if not ss:
                    return {'mensaje': 'Soft skill ' + str(soft_skill) + ' not exist'}, 400
                soft_skills.append(ss)
            try:
                places = int(parse_json.get('places', None))
            except ValueError:
                return {'mensaje': 'Places is not integer'}, 400
            new_vacancy = VacancyProject(
                name=parse_json.get('name', None),
                projectId=parse_json.get('projectId', None),
                details=parse_json.get('details', None),
                places=places,
                roles=roles,
                technicalSkills=technical_skills,
                softSkills=soft_skills
            )
            db.session.add(new_vacancy)
            db.session.commit()
            return {
                "id": new_vacancy.id,
            }, 201

        except Exception as e:
            db.session.rollback()
            return {
                "Error": e
            }, 400

class VistaVacancyProject(Resource):

    def get(self, id_vacancy):
        try:
            id_vacancy = int(id_vacancy)
        except ValueError:
            return {'mensaje': 'Vacancy id is not integer'}, 400
        vacancy = VacancyProject.query.filter_by(id=id_vacancy).first()
        if vacancy:
            # roles = get_roles_details(vacancy.roles)
            # technical_skills = get_technical_skills_details(vacancy.technicalSkills)
            # soft_skills = get_soft_skills_details(vacancy.softSkills)
            return {
                'id': vacancy.id,
                'name': vacancy.name,
                'projectId': vacancy.projectId,
                'details': vacancy.details,
                'places': vacancy.places,
                'roles': json.dumps(vacancy.roles, default=enum_serializer),,
                'technicalSkills': vacancy.technicalSkills,
                'softSkills': vacancy.softSkills
            }, 200
        else:
            return {'mensaje': 'Vacancy not exist'}, 404

    def delete(self, id_vacancy):
        try:
            id_vacancy = int(id_vacancy)
        except ValueError:
            return {'mensaje': 'Vacancy id is not integer'}, 400
        vacancy = VacancyProject.query.filter_by(id=id_vacancy).first()
        if vacancy:
            db.session.delete(vacancy)
            db.session.commit()
            return {'mensaje': 'Vacancy deleted'}, 200
        else:
            return {'mensaje': 'Vacancy not exist'}, 204

    def put(self, id_vacancy):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            if not parse_json.get('name', None) or not parse_json.get('details', None) or not parse_json.get('places', None) or not parse_json.get('roles', None) or not parse_json.get('technicalSkills', None) or not parse_json.get('softSkills', None):
                return {'mensaje': 'Field is missing'}, 400
            vacacy = VacancyProject.query.filter_by(name=parse_json.get('name', None)).first()
            if vacacy:
                return {'mensaje': 'Vacancy already exist'}, 400
            project = Project.query.filter_by(id=parse_json.get('projectId', None)).first()
            if not project:
                return {'mensaje': 'Project not exist'}, 400
            roles = []
            for role in parse_json.get('roles', None):
                r = Role.query.filter_by(id=role).first()
                if not r:
                    return {'mensaje': 'Role ' + str(role) + ' not exist'}, 400
                roles.append(r)
            technical_skills = []
            for technical_skill in parse_json.get('technicalSkills', None):
                ts = TechnicalSkills.query.filter_by(id=technical_skill).first()
                if not ts:
                    return {'mensaje': 'Technical skill ' + str(technical_skill) + ' not exist'}, 400
                technical_skills.append(ts)
            soft_skills = []
            for soft_skill in parse_json.get('softSkills', None):
                ss = SoftSkills.query.filter_by(id=soft_skill).first()
                if not ss:
                    return {'mensaje': 'Soft skill ' + str(soft_skill) + ' not exist'}, 400
                soft_skills.append(ss)
            try:
                places = int(parse_json.get('places', None))
            except ValueError:
                return {'mensaje': 'Places is not integer'}, 400
            vacancy = VacancyProject.query.filter_by(id=id_vacancy).first()
            if vacancy:
                vacancy.name = parse_json.get('name', None)
                vacancy.projectId = parse_json.get('projectId', None)
                vacancy.details = parse_json.get('details', None)
                vacancy.places = places
                vacancy.roles = roles
                vacancy.technicalSkills = technical_skills
                vacancy.softSkills = soft_skills
                db.session.commit()
                return {'mensaje': 'Vacancy was updated'}, 200
            else:
                return {'mensaje': 'Vacancy not exist'}, 204
        except Exception as e:
            db.session.rollback()
            return {
                "Error": e
            }, 400
