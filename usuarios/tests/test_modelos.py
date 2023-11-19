import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.modelos import db, Usuario, Languages, TechnicalResource, TechnicalResourceProgrammingLanguages, UserType, TypeIdentification, Genre, AditionalInformation, ProfessionalExperience, AcademicInformation, EducationLevel, ProfessionalSector, TechnicalResourceLanguages, TechnicalResourcePersonalSkills, Country, State, City, Employee, Company
from application import application as app
from utils.utils import generate_string_random

@pytest.fixture(scope = 'module')
def new_user():
    user = Usuario(
        email = 'test@test.com',
        username='test',
        password=b'password',
        userType=UserType.PERSON,
        salt = 'salt',
    )
    return user

@pytest.fixture(scope = 'module')
def new_tecnical_resource():
    tecnical_resource = TechnicalResource(
        name = 'John',
        lastName = 'Doe',
        typeIdentification=TypeIdentification.CC,
        identification = '123456789' + generate_string_random(5),
        birthdate=datetime.now(timezone.utc),
        genre=Genre.MALE,
        phoneNumber = '555-555-5555',
        mobileNumber = '555-555-5555',
        city = 1,
        state = 1,
        country=1,
        address = '123 Main St.',
        photo = "//",
        userId=1
    )
    return tecnical_resource

@pytest.fixture(scope = 'module')
def new_professional_experience():
    professional_experience = ProfessionalExperience(
        technicalResourceId = 1,
        startDate = datetime.now(timezone.utc),
        endDate = datetime.now(timezone.utc),
        titleJob = 'Software Engineer',
        companyName = 'Acme Inc.',
        details = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    )
    return professional_experience

@pytest.fixture(scope = 'module')
def new_additional_information():
    aditional_information = AditionalInformation(
        technicalResourceId = 1,
        driverLicense = 'abcdefg',
        transferAvailability = True,
        vehicule = '12345'
    )
    return aditional_information

@pytest.fixture(scope = 'module')
def new_academic_information():
    aditional_information = AcademicInformation(
        technicalResourceId = 1,
        educationLevel = EducationLevel.COLLEGE,
        professionalSector = 1,
        schoolName = 'Anytown University',
        startDate = datetime.now(timezone.utc),
        endDate = datetime.now(timezone.utc)
    )
    return aditional_information

@pytest.fixture(scope = 'module')
def new_professional_sector():
    professional_sector = ProfessionalSector(
        name = 'Software Engineer',
        code = 'SE'
    )
    return professional_sector

@pytest.fixture(scope = 'module')
def new_language():
    language = Languages(
        name = 'Italian',
        code = 'ITA'
    )
    return language

@pytest.fixture(scope = 'module')
def new_technical_resource_programming_languages():
    technical_resource_programming_languages = TechnicalResourceProgrammingLanguages(
        technicalResourceId = 1,
        name='Python',
        score=5
    )
    return technical_resource_programming_languages

@pytest.fixture(scope = 'module')
def new_technical_resource_languages():
    technical_resource_languages = TechnicalResourceLanguages(
        technicalResourceId = 1,
        language=1,
        score=5
    )
    return technical_resource_languages

@pytest.fixture(scope = 'module')
def new_technical_resource_personal_skills():
    technical_resource_personal_skills = TechnicalResourcePersonalSkills(
        technicalResourceId = 1,
        name='Escuchar',
        score=5
    )
    return technical_resource_personal_skills

@pytest.fixture(scope = 'module')
def new_country():
    country = Country(
        name = 'Colombia',
        code = 'CO'
    )
    return country

@pytest.fixture(scope = 'module')
def new_state():
    state = State(
        name = 'Antioquia',
        code = 'ANT',
        countryId = 1
    )
    return state

@pytest.fixture(scope = 'module')
def new_city():
    city = City(
        name = 'Medellin',
        code = 'MED',
        stateId = 1
    )
    return city

@pytest.fixture(scope = 'module')
def new_employee():
    employee = Employee(
        name = 'John',
        lastName = 'Doe',
        typeIdentification=TypeIdentification.CC,
        identification = '123456789' + generate_string_random(5),
        phoneNumber='555-555-5555',
        mobileNumber='555-555-5555',
        city = 1,
        state = 1,
        country=1,
        address = '123 Main St.',
        photo = "//",
        userId=1
    )
    return employee

@pytest.fixture(scope = 'module')
def new_company():
    company = Company(
        name = 'Acme Inc.',
        typeIdentification=TypeIdentification.NIT,
        identification = '123456789' + generate_string_random(5),
        phoneNumber='555-555-5555',
        mobileNumber='555-555-5555',
        city = 1,
        state = 1,
        country=1,
        address = '123 Main St.',
        photo = "//",
        userId=1
    )
    return company

def test_user_model(new_user):
    # Add the object to the database
    u = Usuario(new_user.email,
            new_user.username,
            new_user.password,
            new_user.userType,
            new_user.salt
            )

    # Check that the retrieved object matches the original object
    assert u.password == b'password'
    assert u.userType == UserType.PERSON
    assert u.salt == 'salt'

def test_tecnical_resource_model(new_tecnical_resource):
    # Add the object to the database
    tr = TechnicalResource(new_tecnical_resource.name,
                     new_tecnical_resource.lastName,
                     new_tecnical_resource.typeIdentification,
                     new_tecnical_resource.identification,
                     new_tecnical_resource.birthdate,
                     new_tecnical_resource.genre,
                     new_tecnical_resource.phoneNumber,
                     new_tecnical_resource.mobileNumber,
                     new_tecnical_resource.city,
                     new_tecnical_resource.state,
                     new_tecnical_resource.country,
                     new_tecnical_resource.address,
                     new_tecnical_resource.photo,
                     new_tecnical_resource.userId
                    )

    # Check that the retrieved object matches the original object
    assert tr.lastName == 'Doe'
    assert tr.typeIdentification == TypeIdentification.CC
    assert tr.genre == Genre.MALE
    assert tr.phoneNumber == '555-555-5555'
    assert tr.mobileNumber == '555-555-5555'
    assert tr.address == '123 Main St.'
    assert tr.photo == "//"
    assert tr.userId == 1

def test_professional_experience_model(new_professional_experience):
    # Add the object to the database
    pe = ProfessionalExperience(new_professional_experience.technicalResourceId,
                           new_professional_experience.startDate,
                           new_professional_experience.endDate,
                           new_professional_experience.titleJob,
                           new_professional_experience.companyName,
                           new_professional_experience.details)

    # Check that the retrieved object matches the original object
    assert pe.titleJob == 'Software Engineer'
    assert pe.details == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'


def test_academic_information(new_academic_information):
    # Add the object to the database
    ai = AcademicInformation(new_academic_information.technicalResourceId,
                        new_academic_information.schoolName,
                        new_academic_information.educationLevel,
                        new_academic_information.professionalSector,
                        new_academic_information.startDate,
                        new_academic_information.endDate)

    # Check that the retrieved object matches the original object
    assert ai.technicalResourceId == 1
    assert ai.schoolName == 'Anytown University'
    assert ai.educationLevel == EducationLevel.COLLEGE

def test_additional_information(new_additional_information):
    # Add the object to the database
    ai = AditionalInformation(new_additional_information.technicalResourceId,
                         new_additional_information.driverLicense,
                         new_additional_information.transferAvailability,
                         new_additional_information.vehicule)

    # Check that the retrieved object matches the original object
    assert ai.driverLicense == 'abcdefg'
    assert ai.transferAvailability == True

def test_professional_sector(new_professional_sector):
    # Add the object to the database
    ps = ProfessionalSector(new_professional_sector.name, new_professional_sector.code)

    # Check that the retrieved object matches the original object
    assert ps.code == 'SE'

def test_language(new_language):
    # Add the object to the database
    l = Languages(new_language.name, new_language.code)

    # Check that the retrieved object matches the original object
    assert l.code == 'ITA'
    assert l.name == 'Italian'

def test_technical_resource_programming_languages(new_technical_resource_programming_languages):
    # Add the object to the database
    trpl = TechnicalResourceProgrammingLanguages(new_technical_resource_programming_languages.technicalResourceId,
                                                 new_technical_resource_programming_languages.name,
                                                 new_technical_resource_programming_languages.score)

    # Check that the retrieved object matches the original object
    assert trpl.technicalResourceId == 1
    assert trpl.name == 'Python'
    assert trpl.score == 5

def test_technical_resource_languages(new_technical_resource_languages):
    # Add the object to the database
    trl = TechnicalResourceLanguages(new_technical_resource_languages.technicalResourceId,
                                                 new_technical_resource_languages.language,
                                                 new_technical_resource_languages.score)

    # Check that the retrieved object matches the original object
    assert trl.technicalResourceId == 1
    assert trl.score == 5

def test_technical_resource_personal_skills(new_technical_resource_personal_skills):
    # Add the object to the database
    trps = TechnicalResourcePersonalSkills(new_technical_resource_personal_skills.technicalResourceId,
                                                 new_technical_resource_personal_skills.name,
                                                 new_technical_resource_personal_skills.score)

    # Check that the retrieved object matches the original object
    assert trps.technicalResourceId == 1
    assert trps.name == 'Escuchar'
    assert trps.score == 5

def test_country(new_country):
    # Add the object to the database
    c = Country(new_country.name, new_country.code)

    # Check that the retrieved object matches the original object
    assert c.code == 'CO'
    assert c.name == 'Colombia'

def test_state(new_state):
    # Add the object to the database
    s = State(new_state.name, new_state.code, new_state.countryId)

    # Check that the retrieved object matches the original object
    assert s.code == 'ANT'
    assert s.name == 'Antioquia'
    assert s.countryId == 1

def test_city(new_city):
    # Add the object to the database
    c = City(new_city.name, new_city.code, new_city.stateId)

    # Check that the retrieved object matches the original object
    assert c.code == 'MED'
    assert c.name == 'Medellin'
    assert c.stateId == 1

def test_employee(new_employee):
    # Add the object to the database
    e = Employee(new_employee.name,
                 new_employee.lastName,
                 new_employee.typeIdentification,
                 new_employee.identification,
                 new_employee.phoneNumber,
                 new_employee.mobileNumber,
                 new_employee.city,
                 new_employee.state,
                 new_employee.country,
                 new_employee.address,
                 new_employee.photo,
                 new_employee.userId)

    # Check that the retrieved object matches the original object
    assert e.name == 'John'
    assert e.lastName == 'Doe'
    assert e.typeIdentification == TypeIdentification.CC
    assert e.phoneNumber == '555-555-5555'
    assert e.mobileNumber == '555-555-5555'
    assert e.address == '123 Main St.'
    assert e.photo == "//"
    assert e.userId == 1

def test_company(new_company):
    # Add the object to the database
    c = Company(new_company.name,
                 new_company.typeIdentification,
                 new_company.identification,
                 new_company.phoneNumber,
                 new_company.mobileNumber,
                 new_company.city,
                 new_company.state,
                 new_company.country,
                 new_company.address,
                 new_company.photo,
                 new_company.userId)

    # Check that the retrieved object matches the original object
    assert c.name == 'Acme Inc.'
    assert c.typeIdentification == TypeIdentification.NIT
    assert c.phoneNumber == '555-555-5555'
    assert c.mobileNumber == '555-555-5555'
    assert c.address == '123 Main St.'
    assert c.photo == "//"
    assert c.userId == 1
