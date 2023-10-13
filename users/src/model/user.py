import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
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

class TypeIdentification(enum.Enum):
    CC = 1
    NIT = 2
    CE = 3
    PASSPORT = 4

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.LargeBinary)
    userType = db.Column(db.Enum(UserType))
    salt = db.Column(db.String(100))
    token = db.Column(db.String(500))
    expireAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, id, username, password, userType, salt, token, expireAt, createdAt):
        self.id = id
        self.username = username
        self.password = password
        self.userType = userType
        self.salt = salt
        self.token = token
        self.expireAt = expireAt
        self.createdAt = createdAt

class TecnicalResource(db.Model):
    __tablename__ = 'tecnical_resource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    lastName = db.Column(db.String(50), unique=True, nullable=False)
    typeIdentification = db.Column(db.Enum(TypeIdentification))
    identification = db.Column(db.String(50), unique=True, nullable=False)
    birthDate = db.Column(DateTime(timezone=True))
    genre = db.Column(db.Enum(Genre))
    phoneNumber = db.Column(db.String(50), unique=True, nullable=False)
    mobileNumber = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(50), unique=True, nullable=False)
    nationality = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(50), unique=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, id, name, lastName, typeIdentification, identification, birthDate, genre, phoneNumber, mobileNumber, city, nationality, address, userId):
        self.id = id
        self.name = name
        self.lastName = lastName
        self.typeIdentification = typeIdentification
        self.identification = identification
        self.birthDate = birthDate
        self.genre = genre
        self.phoneNumber = phoneNumber
        self.mobileNumber = mobileNumber
        self.city = city
        self.nationality = nationality
        self.address = address
        self.userId = userId

class AcademicInformation(db.Model):
    __tablename__ = 'academic_information'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    educationLevel = db.Column(db.Enum(EducationLevel))
    professionalSector = db.Column(db.Integer, db.ForeignKey('professional_sector.id'))
    startDate = db.Column(DateTime(timezone=True))
    endDate = db.Column(DateTime(timezone=True))

    def __init__(self, id, tecnicalResourceId, educationLevel, professionalSector, startDate, endDate):
        self.id = id
        self.tecnicalResourceId = tecnicalResourceId
        self.educationLevel = educationLevel
        self.professionalSector = professionalSector
        self.startDate = startDate
        self.endDate = endDate

class ProfessionalSector(db.Model):
    __tablename__ = 'professional_sector'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, id, name, code):
        self.id = id
        self.name = name
        self.code = code

class ProfessionalExperience(db.Model):
    __tablename__ = 'professional_experience'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    professionalSector = db.Column(db.Integer, db.ForeignKey('professional_sector.id'))
    startDate = db.Column(DateTime(timezone=True))
    endDate = db.Column(DateTime(timezone=True))
    titleJob = db.Column(db.String(50), unique=True, nullable=False)
    companyName = db.Column(db.String(50), unique=True, nullable=False)
    details = db.Column(db.String(250), unique=True, nullable=False)

    def __init__(self, id, tecnicalResourceId, professionalSector, startDate, endDate, titleJob, companyName, details):
        self.id = id
        self.tecnicalResourceId = tecnicalResourceId
        self.professionalSector = professionalSector
        self.startDate = startDate
        self.endDate = endDate
        self.titleJob = titleJob
        self.companyName = companyName
        self.details = details

class AditionalInformation(db.Model):
    __tablename__ = 'aditional_information'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    driverLicense = db.Column(db.String(50), unique=True, nullable=False)
    transferAvailability = db.Column(db.Boolean, unique=True, nullable=False)
    vehicule = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, id, tecnicalResourceId, driverLicense, transferAvailability, vehicule):
        self.id = id
        self.tecnicalResourceId = tecnicalResourceId
        self.driverLicense = driverLicense
        self.transferAvailability = transferAvailability
        self.vehicule = vehicule


class UserShema(SQLAlchemyAutoSchema):
    class Meta:
         model = User
         include_relationships = False
         load_instance = True

class TecnicalResourceShema(SQLAlchemyAutoSchema):
    class Meta:
         model = TecnicalResource
         include_relationships = False
         load_instance = True

class AcademicInformationShema(SQLAlchemyAutoSchema):
    class Meta:
         model = AcademicInformation
         include_relationships = False
         load_instance = True

class ProfessionalSectorShema(SQLAlchemyAutoSchema):
    class Meta:
         model = ProfessionalSector
         include_relationships = False
         load_instance = True

class ProfessionalExperienceShema(SQLAlchemyAutoSchema):
    class Meta:
         model = ProfessionalExperience
         include_relationships = False
         load_instance = True

class AditionalInformationShema(SQLAlchemyAutoSchema):
    class Meta:
         model = AditionalInformation
         include_relationships = False
         load_instance = True
