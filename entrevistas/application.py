import os
from flask import Flask, Response
from modelos.modelos import db
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///test.db")
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(application)

app_context = application.app_context()
app_context.push()

db.init_app(application)
db.create_all()

api = Api(application)

jwt = JWTManager(application)

@application.route("/interviews/ping")
def index():
    return "pong-pong",200

if __name__ == "__main__":
    application.run(host = "0.0.0.0")
    