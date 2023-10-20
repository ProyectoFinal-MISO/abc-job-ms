from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
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

class TypeIdentification(enum.Enum):
    CC = 1
    NIT = 2
    CE = 3
    PASSPORT = 4

class Usuario(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    userType = db.Column(db.Enum(UserType))
    salt = db.Column(db.String(100))
    token = db.Column(db.String(500))
    expireAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, username, email, password, userType, salt):
        self.username = username
        self.email = email
        self.password = password
        self.userType = userType
        self.salt = salt

class TecnicalResource(db.Model):
    __tablename__ = 'tecnical_resource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    typeIdentification = db.Column(db.Enum(TypeIdentification))
    identification = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.Enum(Genre))
    phoneNumber = db.Column(db.String(50), nullable=False)
    mobileNumber = db.Column(db.String(50), nullable=False)
    city = db.Column(db.Integer, db.ForeignKey('cities.id'))
    state = db.Column(db.Integer, db.ForeignKey('states.id'))
    country = db.Column(db.Integer, db.ForeignKey('countries.id'))
    address = db.Column(db.String(50), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, lastName, typeIdentification, identification, age, genre, phoneNumber, mobileNumber, city, state, country, address, userId):
        self.name = name
        self.lastName = lastName
        self.typeIdentification = typeIdentification
        self.identification = identification
        self.age = age
        self.genre = genre
        self.phoneNumber = phoneNumber
        self.mobileNumber = mobileNumber
        self.city = city
        self.state = state
        self.country = country
        self.address = address
        self.userId = userId

class AcademicInformation(db.Model):
    __tablename__ = 'academic_information'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    schoolName = db.Column(db.String(50), nullable=False)
    educationLevel = db.Column(db.Enum(EducationLevel))
    professionalSector = db.Column(db.Integer, db.ForeignKey('professional_sector.id'))
    startDate = db.Column(DateTime(timezone=True))
    endDate = db.Column(DateTime(timezone=True))

    def __init__(self, tecnicalResourceId, schoolName, educationLevel, professionalSector, startDate, endDate):
        self.tecnicalResourceId = tecnicalResourceId
        self.schoolName = schoolName
        self.educationLevel = educationLevel
        self.professionalSector = professionalSector
        self.startDate = startDate
        self.endDate = endDate

class ProfessionalSector(db.Model):
    __tablename__ = 'professional_sector'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name, code):
        self.name = name
        self.code = code

class Languages(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name, code):
        self.name = name
        self.code = code

class ProfessionalExperience(db.Model):
    __tablename__ = 'professional_experience'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    startDate = db.Column(DateTime(timezone=True))
    endDate = db.Column(DateTime(timezone=True))
    titleJob = db.Column(db.String(50), nullable=False)
    companyName = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(250), nullable=False)

    def __init__(self, tecnicalResourceId, startDate, endDate, titleJob, companyName, details):
        self.tecnicalResourceId = tecnicalResourceId
        self.startDate = startDate
        self.endDate = endDate
        self.titleJob = titleJob
        self.companyName = companyName
        self.details = details

class AditionalInformation(db.Model):
    __tablename__ = 'aditional_information'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    driverLicense = db.Column(db.String(50), nullable=False)
    transferAvailability = db.Column(db.Boolean, nullable=False)
    vehicule = db.Column(db.String(50), nullable=False)

    def __init__(self, tecnicalResourceId, driverLicense, transferAvailability, vehicule):
        self.tecnicalResourceId = tecnicalResourceId
        self.driverLicense = driverLicense
        self.transferAvailability = transferAvailability
        self.vehicule = vehicule

class TecnicalResourceProgrammingLanguages(db.Model):
    __tablename__ = 'technical_resource_programming_languages'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, tecnicalResourceId, name, score):
        self.tecnicalResourceId = tecnicalResourceId
        self.name = name
        self.score = score

class TecnicalResourceLanguages(db.Model):
    __tablename__ = 'tecnical_resource_languages'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    language = db.Column(db.Integer, db.ForeignKey('languages.id'))
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, tecnicalResourceId, language, score):
        self.tecnicalResourceId = tecnicalResourceId
        self.language = language
        self.score = score

class TecnicalResourcePersonalSkills(db.Model):
    __tablename__ = 'tecnical_resource_personal_skills'
    id = db.Column(db.Integer, primary_key=True)
    tecnicalResourceId = db.Column(db.Integer, db.ForeignKey('tecnical_resource.id'))
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, tecnicalResourceId, name, score):
        self.tecnicalResourceId = tecnicalResourceId
        self.name = name
        self.score = score

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name, code):
        self.name = name
        self.code = code

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    countryId = db.Column(db.Integer, db.ForeignKey('countries.id'))

    def __init__(self, name, code, countryId):
        self.name = name
        self.code = code
        self. countryId = countryId

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    stateId = db.Column(db.Integer, db.ForeignKey('states.id'))

    def __init__(self, name, code, stateId):
        self.name = name
        self.code = code
        self.stateId = stateId

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class TecnicalResourceSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = TecnicalResource
         include_relationships = False
         load_instance = True

class AcademicInformationSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = AcademicInformation
         include_relationships = False
         load_instance = True

class ProfessionalSectorSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = ProfessionalSector
         include_relationships = False
         load_instance = True

class LanguagesSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Languages
         include_relationships = False
         load_instance = True

class ProfessionalExperienceSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = ProfessionalExperience
         include_relationships = False
         load_instance = True

class AditionalInformationSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = AditionalInformation
         include_relationships = False
         load_instance = True

class TecnicalResourceProgrammingLanguagesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TecnicalResourceProgrammingLanguages
        include_relationships = True
        load_instance = True

class TecnicalResourceLanguagesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TecnicalResourceLanguages
        include_relationships = True
        load_instance = True

class TecnicalResourcePersonalSkillsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TecnicalResourcePersonalSkills
        include_relationships = True
        load_instance = True

class CountrySchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Country
         include_relationships = False
         load_instance = True

class StateSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = State
         include_relationships = False
         load_instance = True

class CitySchema(SQLAlchemyAutoSchema):
    class Meta:
         model = City
         include_relationships = False
         load_instance = True
