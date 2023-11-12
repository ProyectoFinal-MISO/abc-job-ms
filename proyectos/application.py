import os
from flask import Flask, Response
from modelos.modelos import db
from modelos.populate_db import populate_database
from vistas.vistas_project import VistaProjectCreate, VistaProject, VistaProjectList, VistaProjectListByCompanyId
from vistas.vistas_team import VistaTeamProjectCreate, VistaTeamProject, VistaTeamProjectList, VistaTeamProjectByProjectId
from vistas.vistas_member_team import VistaMembersTeamProjectCreate, VistaMembersTeamProject, VistaMembersTeamProjectList, VistaMembersTeamProjectByTeamId
from vistas.vistas_applicant import VistaApplicantsVacancyProject, VistaApplicantsVacancyProjectList, VistaApplicantsVacancyProjectByVacancyId
from vistas.vistas_vacancy import VistaVacancyProjectCreate, VistaVacancyProject

from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") is not None else 'postgresql://postgres:root@localhost/abc_proyectos_3'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(application)

app_context = application.app_context()
app_context.push()

db.init_app(application)
db.create_all()

api = Api(application)
api.add_resource(VistaProjectCreate, '/projects')
api.add_resource(VistaProject, '/projects/<int:id_project>')
api.add_resource(VistaProjectList, '/projects/list')
api.add_resource(VistaProjectListByCompanyId, '/projects/company/<int:id_company>')

api.add_resource(VistaTeamProjectCreate, '/teams')
api.add_resource(VistaTeamProject, '/teams/<int:id_team>')
api.add_resource(VistaTeamProjectList, '/teams/list')
api.add_resource(VistaTeamProjectByProjectId, '/teams/project/<int:id_project>')

api.add_resource(VistaMembersTeamProjectCreate, '/members')
api.add_resource(VistaMembersTeamProject, '/members/<int:id_member>')
api.add_resource(VistaMembersTeamProjectList, '/members/list')
api.add_resource(VistaMembersTeamProjectByTeamId, '/members/team/<int:id_team>')

#api.add_resource(VistaApplicantsVacancyProjectCreate, '/applicants')
api.add_resource(VistaApplicantsVacancyProject, '/applicants/<int:id_applicant>')
api.add_resource(VistaApplicantsVacancyProjectList, '/applicants/list')
api.add_resource(VistaApplicantsVacancyProjectByVacancyId, '/applicants/<int:id_vacancy>')

api.add_resource(VistaVacancyProjectCreate, '/vacancies')
api.add_resource(VistaVacancyProject, '/vacancies/<int:id_vacancy>')

jwt = JWTManager(application)

@application.route("/projects/ping")
def index():
    return "pong-pong",200

if __name__ == "__main__":
    application.run(host = "0.0.0.0")
