import os
from flask import Flask, Response
from vistas.vistas import VistaConfirmar, VistaGuest, VistaMeet, VistaMeets
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

api.add_resource(VistaMeets, '/interviews')
api.add_resource(VistaMeet, '/interviews/<int:id_meet>')
api.add_resource(VistaGuest, '/interviews/<int:id_meet>/usuario/<int:id_user_guest>')
api.add_resource(VistaConfirmar, '/interviews/<string:flow>/<int:id_guest>')

@application.route("/interviews/ping")
def index():
    return "pong-pong",200

if __name__ == "__main__":
    application.run(host = "0.0.0.0")
    