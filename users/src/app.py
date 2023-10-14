import os
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.model.user import db

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.view.user import VistaPing, VistaSignUp, VistaLogIn, VistaUserInfo

# Initialize Flask
app = Flask(__name__)
# Configura la URL de la base de datos PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") is not None else 'postgresql://postgres:root@localhost/abc_users_2'

app.config["JWT_SECRET_KEY"] = 'users_s4cret_ke1'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=200)
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(VistaPing, "/users/ping")
api.add_resource(VistaSignUp, "/users/")
api.add_resource(VistaLogIn, "/users/auth")
api.add_resource(VistaUserInfo, "/users/me")

cors = CORS(app)
app_context = app.app_context();
app_context.push()
db.init_app(app)
db.create_all()
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
