import os
from flask import Flask, Response
from modelos.modelos import db
from vistas.vistas import VistasLogIn, VistaSignIn, VistaUsuario, VistaUsuarioSesion
from vistas.employees import VistaEmployee
from vistas.companies import VistaCompany
from vistas.technical_resources import VistaTechnicalResource
from vistas.professional_sector import VistaProfessionalSector
from vistas.language import VistaLanguage
from vistas.locations import VistaLocationCountries, VistaLocationStates, VistaLocationCities
from vistas.combo_box_options import VistaTypesIdentification, VistaGenders, VistaEducationLevels, VistaUserTypes
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from modelos.populate_db import populate_database

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///test.db")
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JWT_SECRET_KEY'] = 'secret_key'
application.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
CORS(application)

app_context = application.app_context()
app_context.push()

db.init_app(application)
db.create_all()

api = Api(application)
api.add_resource(VistaSignIn, '/users')
api.add_resource(VistasLogIn, '/users/auth')
api.add_resource(VistaUsuario, '/users/me')

api.add_resource(VistaEmployee, '/users/employee/<id_employee>')
api.add_resource(VistaCompany, '/users/company/<id_company>')
api.add_resource(VistaTechnicalResource, '/users/technical_resource/<id_tr>')

api.add_resource(VistaProfessionalSector, '/users/professional_sector')
api.add_resource(VistaLanguage, '/users/language')
api.add_resource(VistaLocationCountries, '/users/location/countries')
api.add_resource(VistaLocationStates, '/users/location/states/<int:id_country>')
api.add_resource(VistaLocationCities, '/users/location/cities/<int:id_state>')

api.add_resource(VistaTypesIdentification, '/users/types_documents')
api.add_resource(VistaGenders, '/users/genders')
api.add_resource(VistaEducationLevels, '/users/education_levels')
api.add_resource(VistaUserTypes, '/users/user_types')
api.add_resource(VistaUsuarioSesion, '/users/user_session')

# Alimentar base de datos con valores por defecto
populate_database()

jwt = JWTManager(application)

@jwt.unauthorized_loader
def missing_token(callback):
    return Response(status=401)

@jwt.expired_token_loader
def missing_token(jwt_header, jwt_payload):
    return Response(status=401)

@jwt.invalid_token_loader
def invalid_token(callback):
    return Response(status=401)

@application.route("/users/ping")
def index():
    return "pong-pong",200

if __name__ == "__main__":
    application.run(host = "0.0.0.0")
