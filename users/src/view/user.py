from datetime import datetime

from flask import request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from flask_restful import Resource
# from strgen import StringGenerator
import hashlib

from src.model.user import User, db, TecnicalResource
from src.utils.utils import hash_new_password, get_datetime_iso_format, is_correct_password, get_expiration_datetime

from src.utils.tecnical_resource import TecnicalResourceCreate

class VistaPing(Resource):
    def get(self):
        return "Pong"


class VistaSignUp(Resource):
    def post(self):
        if not request.is_json:
            return Response(status=400)

        parse_json = request.get_json()
        if parse_json.get('email', None) and parse_json.get('userType', None) and parse_json.get('password', None):
            users = User.query.filter((User.email==f"{parse_json.get('email', None)}")).count()
            tr = TecnicalResource.query.filter((TecnicalResource.identification==f"{parse_json['personalInformation'].get('identification', None)}")).count()

            # TODO: Validar que no exista un usuario con el mismo email o identificacion
            if users > 0:
                return {
                    "Email": "Email already exists"
                }, 412
            if tr > 0:
                return {
                    "Identification": "Identification already exists"
                }, 412
            else:
                # example of json request body for this endpoint (userType can be PERSON or COMPANY):
                # {
                #     "email": "test@test.com",
                #     "userType": "PERSON",
                #     "password": "test"
                #     "personalInformation": {
                #        "...": "...",
                #     },
                #     "academicInformation": {
                #        ["...": "..."],
                #        ["...": "..."],
                #     },
                #     "professionalExperience": {
                #        ["...": "..."],
                #        ["...": "..."],
                #     },
                #     "aditionalInformation": {
                #        ["...": "..."]
                #     }
                # }

                try:
                    salt = "abc" # StringGenerator("[\l\d]{15}").render_list(1)
                    password = salt[0] + parse_json.get('password', None)
                    password = hashlib.sha256(password.encode()).hexdigest()
                    userType = parse_json.get('userType', None)
                    new_user = User(
                        email = parse_json.get('email', None),
                        userType = userType,
                        password = b'password',
                        salt = salt[0],
                        token='abc',
                        expireAt=get_datetime_iso_format(datetime.now()),
                        createdAt=get_datetime_iso_format(datetime.now())
                    )
                    db.session.add(new_user)
                    db.session.commit()

                    # Llamado funciones para el guardado de la informacion del usuario segun el tipo de usuario
                    if userType == "PERSON":
                        new_tecnical_resource = TecnicalResourceCreate(new_user.id, parse_json)

                    return {
                        "id": new_user.id,
                        "createdAt": f"{new_user.createdAt}",
                        "tecnical_resource": new_tecnical_resource[0]
                    }, 201
                except Exception as e:
                    return Response(status=400)
        else:
            return Response(status=400)


class VistaLogIn(Resource):
    def post(self):
        try:
            email = request.json["email"]
            password = request.json["password"]
        except:
            return "", 400
        if email is None or password is None:
            return "", 400
        user = User.query.filter(User.email == email).first()
        if user is not None:
            salt = user.salt
            pw_hash = user.password
            if is_correct_password(salt, pw_hash, password):
                token = create_access_token(identity=user.id)
                expiration_date = get_expiration_datetime()
                return {"id": user.id, "token": token, "expireAt": expiration_date}, 200
            else:
                return "", 422
        else:
            return "", 404


class VistaUserInfo(Resource):
    def get(self):
        try:
            verify_jwt_in_request(optional=True)
        except:
            return "", 401
        jwt_header = get_jwt()
        if jwt_header == {}:
            return "", 400
        id_user = get_jwt_identity()
        if id_user is None:
            return "", 401
        user = User.query.filter(User.id == id_user).first()
        return {"id": id_user, "email": user.email, "userType": user.userType}, 200
