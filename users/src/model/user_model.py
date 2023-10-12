import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func
import enum

db = SQLAlchemy()

class UserType(enum.Enum):
    PERSON = 1
    COMPANY = 2
    EMPLOYEE = 3

class Genre(enum.Enum):
    MALE = 1
    FEMALE = 1
    OTHER = 3

class EducationLevel(enum.Enum):
    PRIMARY_SCHOOL = 1
    COLLEGE = 2
    PROFESSIONAL = 3
    MASTER = 4

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.LargeBinary)
    userType = db.Column(db.Enum(UserType))

class TecnicalResource(db.Model):
    __tablename__ = 'tecnical_resource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    lastName = db.Column(db.String(50), unique=True, nullable=False)
    # idType = db.Column(db.String(50), unique=True, nullable=False)
    identification = db.Column(db.String(50), unique=True, nullable=False)
    birthDate = db.Column(DateTime(timezone=True))
    genre = db.Column(db.String(50), unique=True, nullable=False)
    phoneNumber = db.Column(db.String(50), unique=True, nullable=False)
    mobileNumber = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(50), unique=True, nullable=False)
    nationality = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(50), unique=True, nullable=False)

class AcademicInformation(db.Model):
    __tablename__ = 'academic_information'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    EducationLevel = db.Column(db.Enum(EducationLevel))
    ProfessionalSector = db.Column(db.Integer, db.ForeignKey('professional_sector.id'))
    startDate = db.Column(DateTime(timezone=True))
    endDate = db.Column(DateTime(timezone=True))

class ProfessionalSector(db.Model):
    __tablename__ = 'professional_sector'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

class ProfessionalExperience(db.Model):
    __tablename__ = 'professional_experience'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    ProfessionalSector = db.Column(db.Integer, db.ForeignKey('professional_sector.id'))
    startDate = db.Column(DateTime(timezone=True))
    endDate = db.Column(DateTime(timezone=True))
    titleJob = db.Column(db.String(50), unique=True, nullable=False)
    companyName = db.Column(db.String(50), unique=True, nullable=False)
    details = db.Column(db.String(250), unique=True, nullable=False)
