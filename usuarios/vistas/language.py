from flask_restful import Resource
from modelos.modelos import db, Usuario, UsuarioSchema, Languages
from flask import request, Response
import os
from strgen import StringGenerator
import hashlib
from flask_jwt_extended import create_access_token, decode_token, jwt_required, get_jwt_identity
from datetime import datetime

usuaro_schema = UsuarioSchema()

class VistaLanguage(Resource):

    def get(self):

        ai = Languages.query.all()
        response = []
        if ai:
            for i in ai:
                response.append({
                    'id': i.id,
                    'name': i.name,
                    'code': i.code
                })
        return response, 200
