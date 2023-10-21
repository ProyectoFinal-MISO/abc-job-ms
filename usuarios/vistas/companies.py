from flask_restful import Resource
from modelos.modelos import db, Usuario, UsuarioSchema, Company
from flask import request, Response
import os
from strgen import StringGenerator
import hashlib
from flask_jwt_extended import create_access_token, decode_token, jwt_required, get_jwt_identity
from datetime import datetime

usuaro_schema = UsuarioSchema()

class VistaCompany(Resource):

    @jwt_required()
    def get(self, id_company):

        try:
            id_company = int(id_company)
        except ValueError:
            return {'message': 'Company id is not integer'}, 400

        company = Company.query.filter_by(id=id_company).first()
        if company:
            return {
                'id': company.id,
                'userId': company.userId,
                'name': company.name,
                # TODO: retornar el tipo de identificacion
                # 'typeIdentification': company.typeIdentification,
                'identification': company.identification,
                'phoneNumber': company.phoneNumber,
                'mobileNumber': company.mobileNumber,
                'city': company.city,
                'state': company.state,
                'country': company.country,
                'address': company.address
            }, 200
        else:
            return {'message': 'Company not exist'}, 404

    @jwt_required()
    def delete(self, id_company):
        try:
            id_company = int(id_company)
        except ValueError:
            return {'message': 'Company id is not integer'}, 400

        company = Company.query.filter_by(id=id_company).first()
        if company:
            db.session.delete(company)
            db.session.commit()
            return {'message': 'Company deleted'}, 200
        else:
            return {'message': 'Company not exist'}, 404

    @jwt_required()
    def put(self, id_company):

            if not request.is_json:
                return Response(status=400)
            parse_json = request.get_json()
            if parse_json.get('name', None) and parse_json.get('typeIdentification', None) and parse_json.get('identification', None) and parse_json.get('phoneNumber', None) and parse_json.get('mobileNumber', None) and parse_json.get('city', None) and parse_json.get('state', None) and parse_json.get('country', None) and parse_json.get('address', None):
                try:
                    id_company = int(id_company)
                except ValueError:
                    return {'message': 'Company id is not integer'}, 400

                company = Company.query.filter_by(id=id_company).first()
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
                    db.session.commit()
                    return {'message': 'Employee was updated'}, 200
                else:
                    return {'message': 'Company not exist'}, 404
            else:
                return {'message': 'Field is missing'}, 400


