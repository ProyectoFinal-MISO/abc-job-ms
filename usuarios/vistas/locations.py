from flask_restful import Resource
from modelos.modelos import db, Usuario, UsuarioSchema, Country, State, City
from flask import request, Response
import os
from strgen import StringGenerator
import hashlib
from flask_jwt_extended import create_access_token, decode_token, jwt_required, get_jwt_identity
from datetime import datetime

usuaro_schema = UsuarioSchema()

class VistaLocations(Resource):

    #@jwt_required()
    def get(self):

        co = Country.query.all()
        response = []
        if co:
            for i in co:
                st = State.query.filter_by(countryId=i.id).all()
                st_response = []
                if st:
                    for j in st:
                        ci = City.query.filter_by(stateId=j.id).all()
                        ci_response = []
                        if ci:
                            for k in ci:
                                ci_response.append({
                                    'id': k.id,
                                    'name': k.name,
                                    'code': k.code
                                })
                        st_response.append({
                            'id': j.id,
                            'name': j.name,
                            'code': j.code,
                            'cities': ci_response
                        })
                response.append({
                    'id': i.id,
                    'name': i.name,
                    'code': i.code,
                    'states': st_response
                })
        return response, 200
