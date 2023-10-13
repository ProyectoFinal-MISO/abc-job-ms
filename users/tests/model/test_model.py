import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.user import User, TecnicalResource, UserType, TypeIdentification, Genre, AditionalInformation, ProfessionalExperience, AcademicInformation, EducationLevel, ProfessionalSector

@pytest.fixture(scope = 'module')
def new_user():
    now = datetime.now(timezone.utc)
    user = User(
        username = 'johndoe',
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
    now = datetime.now(timezone.utc)
    tecnical_resource = TecnicalResource(
        name = 'John',
        lastName = 'Doe',
        typeIdentification=TypeIdentification.CC,
        identification = '123456789',
        birthDate=now,
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
        professionalSector = 1,
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
        educationLevel = EducationLevel.PROFESSIONAL,
        professionalSector = 1,
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
    Session = sessionmaker(bind=create_engine('sqlite:///user_test.db'))
    session = Session()

    # Delete any existing object with the same username value
    session.query(User).filter_by(username='johndoe').delete()

    # Add the object to the database
    u = User(new_user.username,
         new_user.password,
         new_user.userType,
         new_user.salt,
         new_user.token,
         new_user.expireAt,
         new_user.createdAt)

    # Retrieve the object from the database
    session.add(u)
    session.commit()
    result = session.query(User).filter_by(username = 'johndoe').first()

    # Check that the retrieved object matches the original object
    assert result.password == b'password'
    assert result.userType == UserType.PERSON
    assert result.salt == 'salt'
    assert result.token == 'token'

def test_tecnical_resource_model(new_tecnical_resource):
    Session = sessionmaker(bind=create_engine('sqlite:///user_test.db'))
    session = Session()

    # Delete any existing object with the same driverLicense value
    session.query(TecnicalResource).filter_by(identification="123456789").delete()

    # Add the object to the database
    tr = TecnicalResource(new_tecnical_resource.name,
                     new_tecnical_resource.lastName,
                     new_tecnical_resource.typeIdentification,
                     new_tecnical_resource.identification,
                     new_tecnical_resource.birthDate,
                     new_tecnical_resource.genre,
                     new_tecnical_resource.phoneNumber,
                     new_tecnical_resource.mobileNumber,
                     new_tecnical_resource.city,
                     new_tecnical_resource.nationality,
                     new_tecnical_resource.address,
                     new_tecnical_resource.userId)

    # Retrieve the object from the database
    session.add(tr)
    session.commit()
    result = session.query(TecnicalResource).filter_by(identification = '123456789').first()

    # Check that the retrieved object matches the original object
    assert result.lastName == 'Doe'
    assert result.typeIdentification == TypeIdentification.CC
    assert result.genre == Genre.MALE
    assert result.phoneNumber == '555-555-5555'
    assert result.mobileNumber == '555-555-5555'
    assert result.city == 'Anytown'
    assert result.nationality == 'USA'
    assert result.address == '123 Main St.'
    assert result.userId == 1

def test_professional_experience_model(new_professional_experience):
    Session = sessionmaker(bind=create_engine('sqlite:///user_test.db'))
    session = Session()

    # Delete any existing object with the same driverLicense value
    session.query(ProfessionalExperience).filter_by(tecnicalResourceId=1).delete()

    # Add the object to the database
    pe = ProfessionalExperience(new_professional_experience.tecnicalResourceId,
                           new_professional_experience.professionalSector,
                           new_professional_experience.startDate,
                           new_professional_experience.endDate,
                           new_professional_experience.titleJob,
                           new_professional_experience.companyName,
                           new_professional_experience.details)

    # Retrieve the object from the database
    session.add(pe)
    session.commit()
    result = session.query(ProfessionalExperience).filter_by(companyName = 'Acme Inc.').first()

    # Check that the retrieved object matches the original object
    assert result.titleJob == 'Software Engineer'
    assert result.details == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'


def test_academic_information(new_academic_information):
    Session = sessionmaker(bind=create_engine('sqlite:///user_test.db'))
    session = Session()

    # Add the object to the database
    ai = AcademicInformation(new_academic_information.tecnicalResourceId,
                        new_academic_information.educationLevel,
                        new_academic_information.professionalSector,
                        new_academic_information.startDate,
                        new_academic_information.endDate)

    # Retrieve the object from the database
    session.add(ai)
    session.commit()
    result = session.query(AcademicInformation).filter_by(tecnicalResourceId = 1).first()

    # Check that the retrieved object matches the original object
    assert result.tecnicalResourceId == 1
    assert result.educationLevel == EducationLevel.PROFESSIONAL
    assert result.professionalSector == 1

def test_aditional_information(new_aditional_information):
    Session = sessionmaker(bind=create_engine('sqlite:///user_test.db'))
    session = Session()

    # Delete any existing object with the same driverLicense value
    session.query(AditionalInformation).filter_by(driverLicense='abcdefg').delete()

    # Add the object to the database
    ai = AditionalInformation(new_aditional_information.tecnicalResourceId,
                         new_aditional_information.driverLicense,
                         new_aditional_information.transferAvailability,
                         new_aditional_information.vehicule)

    # Retrieve the object from the database
    session.add(ai)
    session.commit()
    result = session.query(AditionalInformation).filter_by(tecnicalResourceId = 1).first()

    # Check that the retrieved object matches the original object
    assert result.driverLicense == 'abcdefg'
    assert result.transferAvailability == True
    assert result.vehicule == '12345'

def test_professional_sector(new_professional_sector):
    Session = sessionmaker(bind=create_engine('sqlite:///user_test.db'))
    session = Session()

    # Delete any existing object with the same code value
    session.query(ProfessionalSector).filter_by(code='SE').delete()

    # Add the object to the database
    ps = ProfessionalSector(new_professional_sector.name, new_professional_sector.code)

    # Retrieve the object from the database
    session.add(ps)
    session.commit()
    result = session.query(ProfessionalSector).filter_by(name = 'Software Engineer').first()

    # Check that the retrieved object matches the original object
    assert result.code == 'SE'
