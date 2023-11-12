from flask_restful import Resource
from modelos.modelos import db, ApplicantsVacancyProject
from flask import request, Response
from flask_jwt_extended import jwt_required
from enum import Enum

import json

class VistaApplicantsVacancyProject(Resource):

    def post(self):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            print(parse_json)
            if not parse_json.get('vacancyId', None) or not parse_json.get('userId', None):
                new_applicant = ApplicantsVacancyProject(
                    vacancyId=parse_json.get('vacancyId', None),
                    userId=parse_json.get('userId', None)
                )
                db.session.add(new_applicant)
                db.session.commit()
                return {
                    "id": new_applicant.id,
                }, 201
            else:
                return {'mensaje': 'Field is missing'}, 400
        except Exception as e:
            db.session.rollback()
            return {
                "Error": e
            }, 400

    def get(self, id_applicant):
        try:
            id_applicant = int(id_applicant)
        except ValueError:
            return {'mensaje': 'Applicant id is not integer'}, 400
        applicant = ApplicantsVacancyProject.query.filter_by(id=id_applicant).first()
        if applicant:
            return {
                'id': applicant.id,
                'vacancyId': applicant.vacancyId,
                'userId': applicant.userId
            }, 200
        else:
            return {'mensaje': 'Applicant not exist'}, 404

    def delete(self, id_applicant):
        try:
            id_applicant = int(id_applicant)
        except ValueError:
            return {'mensaje': 'Applicant id is not integer'}, 400
        applicant = ApplicantsVacancyProject.query.filter_by(id=id_applicant).first()
        if applicant:
            db.session.delete(applicant)
            db.session.commit()
            return {'mensaje': 'Applicant deleted'}, 200
        else:
            return {'mensaje': 'Applicant not exist'}, 204

    def put(self, id_applicant):
        try:
            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            if not parse_json.get('vacancyId', None) or not parse_json.get('userId', None):
                try:
                    id_applicant = int(id_applicant)
                except ValueError:
                    return {'mensaje': 'Applicant id is not integer'}, 400

                applicant = ApplicantsVacancyProject.query.filter_by(id=id_applicant).first()
                if applicant:
                    applicant.vacancyId = parse_json.get('vacancyId', None)
                    applicant.userId = parse_json.get('userId', None)
                    db.session.commit()
                    return {'mensaje': 'Applicant was updated'}, 200
                else:
                    return {'mensaje': 'Applicant not exist'}, 204
            else:
                return {'mensaje': 'Field is missing'}, 400
        except Exception as e:
            db.session.rollback()
            return {
                "Error": e
            }, 400

class VistaApplicantsVacancyProjectList(Resource):
    def get(self):
        applicants = ApplicantsVacancyProject.query.all()
        if applicants:
            return {
                "applicants": [
                    {
                        'id': applicant.id,
                        'vacancyId': applicant.vacancyId,
                        'userId': applicant.userId
                    } for applicant in applicants
                ]
            }, 200
        else:
            return {'mensaje': 'Applicants not exist'}, 204

class VistaApplicantsVacancyProjectByVacancyId(Resource):
    def get(self, id_vacancy):
        try:
            id_vacancy = int(id_vacancy)
        except ValueError:
            return {'mensaje': 'Vacancy id is not integer'}, 400
        applicants = ApplicantsVacancyProject.query.filter_by(vacancyId=id_vacancy).all()
        if applicants:
            return {
                "applicants": [
                    {
                        'id': applicant.id,
                        'vacancyId': applicant.vacancyId,
                        'userId': applicant.userId
                    } for applicant in applicants
                ]
            }, 200
        else:
            return {'mensaje': 'Applicants not exist'}, 204
