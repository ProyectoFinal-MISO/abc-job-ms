from datetime import datetime

from flask import request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from flask_restful import Resource
# from strgen import StringGenerator
import hashlib

from src.model.user import User, db
from src.utils.utils import hash_new_password, get_datetime_iso_format, is_correct_password, get_expiration_datetime

class VistaPing(Resource):
    def get(self):
        return "Pong"


class VistaSignUp(Resource):
    def post(self):
        if not request.is_json:
            return Response(status=400)
        parse_json = request.get_json()
        if parse_json.get('username', None) and parse_json.get('userType', None) and parse_json.get('password', None):
            users = User.query.filter((User.username==f"{parse_json.get('username', None)}") | (User.userType==f"{parse_json.get('userType', None)}")).all()
            if len(users) > 0:
                return Response(status=412)
            else:
                salt = "assaasas" #StringGenerator("[\l\d]{15}").render_list(1)
                password = salt[0] + parse_json.get('password', None)
                password = hashlib.sha256(password.encode()).hexdigest()
                new_user = User(
                    username = parse_json.get('username', None),
                    userType = parse_json.get('userType', None),
                    password = password,
                    salt = salt[0]
                )
                db.session.add(new_user)
                db.session.commit()
                return {
                    "id": new_user.id,
                    "createdAt": f"{new_user.createdAt}"
                }, 201
        else:
            return Response(status=400)


class VistaLogIn(Resource):
    def post(self):
        try:
            username = request.json["username"]
            password = request.json["password"]
        except:
            return "", 400
        if username is None or password is None:
            return "", 400
        user = User.query.filter(User.username == username).first()
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
        return {"id": id_user, "username": user.username, "userType": user.userType}, 200
