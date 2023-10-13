from datetime import datetime

from flask import request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from flask_restful import Resource
# from strgen import StringGenerator
import hashlib

from src.model.user import User, db

class VistaTecnicalResourcePing(Resource):
    def get(self):
        return "Pong"
