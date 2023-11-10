from flask_restful import Resource
from modelos.modelos import db, Usuario, TechnicalResource, Company, Employee, UserType
from utils.technical_resource import TechnicalResourceCreate
from utils.company import CompanyCreate
from utils.employee import EmployeeCreate
from flask import request, Response, jsonify
from strgen import StringGenerator
import hashlib
from flask_jwt_extended import create_access_token, decode_token, jwt_required, get_jwt_identity
from datetime import datetime
import json

class VistaSignIn(Resource):
    def post(self):
        if not request.is_json:
            return Response(status=400)
        parse_json = request.get_json()
        if parse_json.get('username', None) and parse_json.get('email', None) and parse_json.get('password', None):
            usuarios = Usuario.query.filter((Usuario.username==f"{parse_json.get('username', None)}") | (Usuario.email==f"{parse_json.get('email', None)}")).count()
            if usuarios > 0:
                return {
                    "mensaje": "Email or username already exists"
                }, 412
            tr = TechnicalResource.query.filter((TechnicalResource.identification==f"{parse_json['personalInformation'].get('identification', None)}")).count()
            if tr > 0:
                return {
                    "mensaje": "Identification already exists"
                }, 412

            salt = StringGenerator("[\l\d]{15}").render_list(1)
            password = salt[0] + parse_json.get('password', None)
            password = hashlib.sha256(password.encode()).hexdigest()
            userType = parse_json.get('userType', None)
            nuevo_usuario = Usuario(
                username = parse_json.get('username', None),
                email = parse_json.get('email', None),
                password = password,
                userType = userType,
                salt = salt[0]
            )
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Llamado funciones para el guardado de la informacion del usuario segun el tipo de usuario
            if userType == "PERSON":
                response = TechnicalResourceCreate(nuevo_usuario.id, parse_json)
            if userType == "EMPLOYEE":
                response = EmployeeCreate(nuevo_usuario.id, parse_json)
            if userType == "COMPANY":
                response = CompanyCreate(nuevo_usuario.id, parse_json)

            return {
                "id": nuevo_usuario.id,
                "createdAt": f"{nuevo_usuario.createdAt}",
                "data": response[0]
            }, 201

        else:
            return Response(status=400)

class VistasLogIn(Resource):
    def post (self):
        error_message = {"mensaje":"Wrong email or password"}
        response = jsonify(error_message)
        response.status_code = 404
        if not request.is_json:
            return Response(status=400)
        parse_json = request.get_json()
        if parse_json.get('username', None) and parse_json.get('password', None):
            usuario = Usuario.query.filter_by(username=parse_json.get('username', None)).all()
            if usuario:
                salt = usuario[0].salt
                password = salt + parse_json.get('password', None)
                password = hashlib.sha256(password.encode()).hexdigest()
                if password == usuario[0].password:
                    token = usuario[0].token
                    expireAt = usuario[0].expireAt
                    if (not token) or expireAt <= datetime.now():
                        additional_claims = {"id": f"{usuario[0].id}"}
                        token = create_access_token(usuario[0].id, additional_claims=additional_claims)
                        expireAt = datetime.fromtimestamp((decode_token(token).get('exp')))
                        usuario[0].token = token
                        usuario[0].expireAt = expireAt
                        db.session.commit()
                    return {
                        "id":usuario[0].id,
                        "token":f"{token}",
                        "expireAt":f"{expireAt}"
                    }, 200
                else:
                    return response
            else:
               return response
        else:
            return Response(status=400)

class VistaUsuario(Resource):
    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        usuario = Usuario.query.get(id)
        return {
            "id":usuario.id,
            "username":f"{usuario.username}",
            "email":f"{usuario.email}"
        }, 200
    
class VistaUsuarioSesion(Resource):
    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        usuario = Usuario.query.get(id)
        if usuario:            
            if usuario.userType == UserType.PERSON:
                obj = TechnicalResource.query.filter_by(userId=id).first()
                if obj:
                    return {
                        'id': obj.id,
                        'userId': obj.userId,
                        'userType': usuario.userType.name,
                        'name': obj.name,
                        'username': usuario.username
                    }, 200
                else:
                    return {'mensaje': 'technical resource not exist'}, 404
            elif usuario.userType == UserType.COMPANY:
                obj = Company.query.filter_by(userId=id).first()
                if obj:
                    return {
                        'id': obj.id,
                        'userId': obj.userId,
                        'userType': usuario.userType.name,
                        'name': obj.name,
                        'username': usuario.username
                    }, 200
                else:
                    return {'mensaje': 'company not exist'}, 404
            else:
                obj = Employee.query.filter_by(userId=id).first()
                if obj:
                    return {
                        'id': obj.id,
                        'userId': obj.userId,
                        'userType': usuario.userType.name,
                        'name': obj.name,
                        'username': usuario.username
                    }, 200 
                else:
                    return {'mensaje': 'employee not exist'}, 404
        else:
            return {'mensaje': 'User not exist'}, 404
