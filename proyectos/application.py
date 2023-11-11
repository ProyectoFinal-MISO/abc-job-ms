import os
from flask import Flask, Response
from modelos.modelos import db
from modelos.populate_db import populate_database

from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") is not None else 'postgresql://postgres:root@localhost/abc_proyectos_2'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(application)

app_context = application.app_context()
app_context.push()

db.init_app(application)
db.create_all()

api = Api(application)

jwt = JWTManager(application)

# Alimentar base de datos con valores por defecto
populate_database()

@application.route("/projects/ping")
def index():
    return "pong-pong",200

if __name__ == "__main__":
    application.run(host = "0.0.0.0")
