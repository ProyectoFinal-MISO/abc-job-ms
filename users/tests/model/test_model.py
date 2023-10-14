import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.user import db, User, TecnicalResource, UserType, TypeIdentification, Genre, AditionalInformation, ProfessionalExperience, AcademicInformation, EducationLevel, ProfessionalSector
from src import app

@pytest.fixture(scope = 'module')
def new_user():
    now = datetime.now(timezone.utc)
    user = User(
        email = 'test@test.com',
        password=b'password',
        userType=UserType.PERSON,
        salt = 'salt',
        token = 'token',
        expireAt = now,
        createdAt = now
    )
    return user

@pytest.fixture(scope = 'module')
def new_tecnical_resource():
    tecnical_resource = TecnicalResource(
        name = 'John',
        lastName = 'Doe',
        typeIdentification=TypeIdentification.CC,
        identification = '123456789',
        age=30,
        genre=Genre.MALE,
        phoneNumber = '555-555-5555',
        mobileNumber = '555-555-5555',
        city = 'Anytown',
        nationality = 'USA',
        address = '123 Main St.',
        userId=1
    )
    return tecnical_resource

@pytest.fixture(scope = 'module')
def new_professional_experience():
    professional_experience = ProfessionalExperience(
        tecnicalResourceId = 1,
        startDate = datetime.now(timezone.utc),
        endDate = datetime.now(timezone.utc),
        titleJob = 'Software Engineer',
        companyName = 'Acme Inc.',
        details = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    )
    return professional_experience

@pytest.fixture(scope = 'module')
def new_aditional_information():
    aditional_information = AditionalInformation(
        tecnicalResourceId = 1,
        driverLicense = 'abcdefg',
        transferAvailability = True,
        vehicule = '12345'
    )
    return aditional_information

@pytest.fixture(scope = 'module')
def new_academic_information():
    aditional_information = AcademicInformation(
        tecnicalResourceId = 1,
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




def test_user_model(new_user):
    # Add the object to the database
    u = User(new_user.email,
         new_user.password,
         new_user.userType,
         new_user.salt,
         new_user.token,
         new_user.expireAt,
         new_user.createdAt)

    # Check that the retrieved object matches the original object
    assert u.password == b'password'
    assert u.userType == UserType.PERSON
    assert u.salt == 'salt'
    assert u.token == 'token'

def test_tecnical_resource_model(new_tecnical_resource):
    # Add the object to the database
    tr = TecnicalResource(new_tecnical_resource.name,
                     new_tecnical_resource.lastName,
                     new_tecnical_resource.typeIdentification,
                     new_tecnical_resource.identification,
                     new_tecnical_resource.age,
                     new_tecnical_resource.genre,
                     new_tecnical_resource.phoneNumber,
                     new_tecnical_resource.mobileNumber,
                     new_tecnical_resource.city,
                     new_tecnical_resource.nationality,
                     new_tecnical_resource.address,
                     new_tecnical_resource.userId)

    # Check that the retrieved object matches the original object
    assert tr.lastName == 'Doe'
    assert tr.typeIdentification == TypeIdentification.CC
    assert tr.genre == Genre.MALE
    assert tr.phoneNumber == '555-555-5555'
    assert tr.mobileNumber == '555-555-5555'
    assert tr.city == 'Anytown'
    assert tr.nationality == 'USA'
    assert tr.address == '123 Main St.'
    assert tr.userId == 1

def test_professional_experience_model(new_professional_experience):
    # Add the object to the database
    pe = ProfessionalExperience(new_professional_experience.tecnicalResourceId,
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
    ai = AcademicInformation(new_academic_information.tecnicalResourceId,
                        new_academic_information.schoolName,
                        new_academic_information.educationLevel,
                        new_academic_information.professionalSector,
                        new_academic_information.startDate,
                        new_academic_information.endDate)

    # Check that the retrieved object matches the original object
    assert ai.tecnicalResourceId == 1
    assert ai.schoolName == 'Anytown University'
    assert ai.educationLevel == EducationLevel.COLLEGE

def test_aditional_information(new_aditional_information):
    # Add the object to the database
    ai = AditionalInformation(new_aditional_information.tecnicalResourceId,
                         new_aditional_information.driverLicense,
                         new_aditional_information.transferAvailability,
                         new_aditional_information.vehicule)

    # Check that the retrieved object matches the original object
    assert ai.driverLicense == 'abcdefg'
    assert ai.transferAvailability == True
    assert ai.vehicule == '12345'

def test_professional_sector(new_professional_sector):
    # Add the object to the database
    ps = ProfessionalSector(new_professional_sector.name, new_professional_sector.code)

    # Check that the retrieved object matches the original object
    assert ps.code == 'SE'
