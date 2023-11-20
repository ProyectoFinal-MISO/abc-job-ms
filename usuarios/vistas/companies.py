from flask_restful import Resource
from modelos.modelos import db, Company
from utils.utils import enum_serializer, location_user
from flask import request, Response
from flask_jwt_extended import jwt_required
from enum import Enum

import json

class VistaCompany(Resource):

    @jwt_required()
    def get(self, id_company):

        try:
            id_company = int(id_company)
        except ValueError:
            return {'mensaje': 'Company id is not integer'}, 400

        company = Company.query.filter_by(userId=id_company).first()
        if company:
            location = location_user(company)
            return {
                'id': company.id,
                'userId': company.userId,
                'personalInformation': {
                    'name': company.name,
                    'typeIdentification':  f"{company.typeIdentification.name}",
                    'identification': company.identification,
                    'phoneNumber': company.phoneNumber,
                    'mobileNumber': company.mobileNumber,
                    'city': company.city,
                    'state': company.state,
                    'country': company.country,
                    'address': company.address,
                    'photo': company.photo
                },
                'location': location,
            }, 200
        else:
            return {'mensaje': 'Company not exist'}, 404

    @jwt_required()
    def delete(self, id_company):
        try:
            id_company = int(id_company)
        except ValueError:
            return {'mensaje': 'Company id is not integer'}, 400

        company = Company.query.filter_by(userId=id_company).first()
        if company:
            db.session.delete(company)
            db.session.commit()
            return {'mensaje': 'Company deleted'}, 200
        else:
            return {'mensaje': 'Company not exist'}, 404

    @jwt_required()
    def put(self, id_company):

            if not request.is_json:
                return {"mensaje": "Error format body"}, 400
            parse_json = request.get_json()
            if parse_json.get('name', None) and parse_json.get('typeIdentification', None) and parse_json.get('identification', None) and parse_json.get('phoneNumber', None) and parse_json.get('mobileNumber', None) and parse_json.get('city', None) and parse_json.get('state', None) and parse_json.get('country', None) and parse_json.get('address', None):
                try:
                    id_company = int(id_company)
                except ValueError:
                    return {'mensaje': 'Company id is not integer'}, 400

                company = Company.query.filter_by(userId=id_company).first()
                if company:
                    company.name = parse_json.get('name', None)
                    company.typeIdentification = parse_json.get('typeIdentification', None)
                    company.identification = parse_json.get('identification', None)
                    company.phoneNumber = parse_json.get('phoneNumber', None)
                    company.mobileNumber = parse_json.get('mobileNumber', None)
                    company.city = parse_json.get('city', None)
                    company.state = parse_json.get('state', None)
                    company.country = parse_json.get('country', None)
                    company.address = parse_json.get('address', None)
                    company.photo = parse_json.get('photo', None)
                    db.session.commit()
                    return {'mensaje': 'Company was updated'}, 200
                else:
                    return {'mensaje': 'Company not exist'}, 404
            else:
                return {'mensaje': 'Field is missing'}, 400
