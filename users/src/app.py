import os
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.model.user import db

from src.view.user import VistaPing, VistaSignUp, VistaLogIn, VistaUserInfo
from src.view.tecnical_resource import VistaTecnicalResourcePing #, VistaCreateTecnicalResource, VistaGetTecnicalResource, VistaUpdateTecnicalResource, VistaDeleteTecnicalResource

# Initialize Flask
app = Flask(__name__)
# Configura la URL de la base de datos PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") is not None else 'postgresql://postgres:root@localhost/abc_users'

app.config["JWT_SECRET_KEY"] = 'users_s4cret_ke1'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=200)
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(VistaPing, "/users/ping")
api.add_resource(VistaSignUp, "/users/")
api.add_resource(VistaLogIn, "/users/auth")
api.add_resource(VistaUserInfo, "/users/me")

## tecnical_resource
api.add_resource(VistaTecnicalResourcePing, "/tecnical_resource/ping")
# api.add_resource(VistaCreateTecnicalResource, "/tecnical_resource/")
# api.add_resource(VistaGetTecnicalResource, "/tecnical_resource/<int:id>")
# api.add_resource(VistaUpdateTecnicalResource, "/tecnical_resource/<int:id>")
# api.add_resource(VistaDeleteTecnicalResource, "/tecnical_resource/<int:id>")
## end tecnical_resource

cors = CORS(app)
app_context = app.app_context();
app_context.push()
db.init_app(app)
db.create_all()
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
