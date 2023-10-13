import pytest
import datetime

from src.model.user import User, TecnicalResource, UserType, TypeIdentification, Genre, AditionalInformation, ProfessionalExperience, AcademicInformation, EducationLevel, ProfessionalSector

@pytest.fixture(scope = 'module')
def new_user():
    user = User(
        id = 1,
        username = 'johndoe',
        password=b'password',
        userType=UserType.PERSON,
        salt = 'salt',
        token = 'token',
        expireAt=datetime.datetime.now(),
        createdAt=datetime.datetime.now()
    )
    return user

@pytest.fixture(scope = 'module')
def new_tecnical_resource():
    tecnical_resource = TecnicalResource(
        id = 1,
        name = 'John',
        lastName = 'Doe',
        typeIdentification=TypeIdentification.CC,
        identification = '123456789',
        birthDate=datetime.datetime.now(),
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
        id = 1,
        tecnicalResourceId = 1,
        professionalSector = 1,
        startDate = '2020-01-01',
        endDate = '2021-01-01',
        titleJob = 'Software Engineer',
        companyName = 'Acme Inc.',
        details = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    )
    return professional_experience

@pytest.fixture(scope = 'module')
def new_aditional_information():
    aditional_information = AditionalInformation(
        id = 1,
        tecnicalResourceId = 1,
        driverLicense = 'abcdefg',
        transferAvailability = 'abcdefg',
        vehicule = '12345'
    )
    return aditional_information

@pytest.fixture(scope = 'module')
def new_academic_information():
    aditional_information = AcademicInformation(
        id = 1,
        tecnicalResourceId = 1,
        educationLevel = EducationLevel.PROFESSIONAL,
        professionalSector = 1,
        startDate = datetime.datetime.now(),
        endDate = datetime.datetime.now()
    )
    return aditional_information

@pytest.fixture(scope = 'module')
def new_professional_sector():
    professional_sector = ProfessionalSector(
        id = 1,
        name = 'Software Engineer',
        code = 'SE'
    )
    return professional_sector




def test_user_model(new_user):
    # Add the object to the database
    User(new_user.id, new_user.username, new_user.password, new_user.userType, new_user.salt, new_user.token, new_user.expireAt, new_user.createdAt)

    # Retrieve the object from the database
    result = User.query.filter_by(username = 'johndoe').first()

    # Check that the retrieved object matches the original object
    assert result.password == b'password'
    assert result.userType == UserType.PERSON
    assert result.salt == 'salt'
    assert result.token == 'token'

def test_tecnical_resource_model(new_tecnical_resource):
    # Add the object to the database
    TecnicalResource(new_tecnical_resource.id, new_tecnical_resource.name, new_tecnical_resource.lastName, new_tecnical_resource.typeIdentification,
                     new_tecnical_resource.identification, new_tecnical_resource.birthDate, new_tecnical_resource.genre, new_tecnical_resource.phoneNumber, new_tecnical_resource.mobileNumber,
                     new_tecnical_resource.city, new_tecnical_resource.nationality, new_tecnical_resource.address, new_tecnical_resource.userId)

    # Retrieve the object from the database
    result = TecnicalResource.query.filter_by(name = 'John').first()

    # Check that the retrieved object matches the original object
    assert result.lastName == 'Doe'
    assert result.typeIdentification == TypeIdentification.CC
    assert result.identification == '123456789'
    assert result.genre == Genre.MALE
    assert result.phoneNumber == '555-555-5555'
    assert result.mobileNumber == '555-555-5555'
    assert result.city == 'Anytown'
    assert result.nationality == 'USA'
    assert result.address == '123 Main St.'
    assert result.userId == 1

def test_professional_experience_model(new_professional_experience):
    # Add the object to the database
    ProfessionalExperience(new_professional_experience.id, new_professional_experience.tecnicalResourceId, new_professional_experience.professionalSector, new_professional_experience.startDate, new_professional_experience.endDate, new_professional_experience.titleJob, new_professional_experience.companyName, new_professional_experience.details)

    # Retrieve the object from the database
    result = ProfessionalExperience.query.filter_by(company_name = 'Acme Inc.').first()

    # Check that the retrieved object matches the original object
    assert result.job_title == 'Software Engineer'
    assert result.start_date == '2020-01-01'
    assert result.end_date == '2021-01-01'

def test_academic_information(new_academic_information):
    # Add the object to the database
    AcademicInformation(new_academic_information.id, new_academic_information.tecnicalResourceId, new_academic_information.educationLevel, new_academic_information.professionalSector, new_academic_information.startDate, new_academic_information.endDate)

    # Retrieve the object from the database
    result = AcademicInformation.query.filter_by(company_name = 'Acme Inc.').first()

    # Check that the retrieved object matches the original object
    assert result.tecnicalResourceId == 1
    assert result.educationLevel == EducationLevel.PROFESSIONAL
    assert result.professionalSector == 1
    assert result.startDate == datetime.datetime.now()
    assert result.endDate == datetime.datetime.now()

def test_aditional_information(new_aditional_information):
    # Add the object to the database
    AditionalInformation(new_aditional_information.id, new_aditional_information.tecnicalResourceId, new_aditional_information.driverLicense, new_aditional_information.transferAvailability, new_aditional_information.vehicule)

    # Retrieve the object from the database
    result = AditionalInformation.query.filter_by(tecnicalResourceId = 1).first()

    # Check that the retrieved object matches the original object
    assert result.driverLicense == 'abcdefg'
    assert result.transferAvailability == 'abcdefg'
    assert result.vehicule == '12345'

def test_professional_sector(new_professional_sector):
    # Add the object to the database
    ProfessionalSector(new_professional_sector.id, new_professional_sector.name, new_professional_sector.code)

    # Retrieve the object from the database
    result = ProfessionalSector.query.filter_by(name = 'Software Engineer').first()

    # Check that the retrieved object matches the original object
    assert result.code == 'SE'
