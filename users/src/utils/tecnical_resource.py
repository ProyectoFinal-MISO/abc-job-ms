from datetime import datetime

from flask import request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from flask_restful import Resource
# from strgen import StringGenerator
import hashlib

from src.model.user import User, db, TecnicalResource, ProfessionalExperience, AcademicInformation, AditionalInformation

def TecnicalResourceCreate(userId, user_data):

    try:
        personal_data = user_data['personalInformation']
        academic_data = user_data['academicInformation']
        professional_data = user_data['professionalExperience']
        aditional_data = user_data['aditionalInformation']

        new_tecnical_resource = TecnicalResource(
            name = personal_data.get('name', None),
            lastName = personal_data.get('lastName', None),
            typeIdentification = personal_data.get('typeIdentification', None),
            identification = personal_data.get('identification', None),
            birthDate = personal_data.get('birthDate', None),
            genre = personal_data.get('genre', None),
            phoneNumber = personal_data.get('phoneNumber', None),
            mobileNumber = personal_data.get('mobileNumber', None),
            city = personal_data.get('city', None),
            nationality = personal_data.get('nationality', None),
            address = personal_data.get('address', None),
            userId = userId
        )
        db.session.add(new_tecnical_resource)
        db.session.commit()

        new_academic_info = AcademicInformationCreate(new_tecnical_resource.id, academic_data)
        new_proffesional_experience = ProfessionalExperienceCreate(new_tecnical_resource.id, professional_data)
        new_aditional_info = AditionalInformationCreate(new_tecnical_resource.id, aditional_data)


        if new_academic_info[1] != 201 or new_proffesional_experience[1] != 201 or new_aditional_info[1] != 201:
            return Response(status=400)

        print(new_academic_info[0])

        return {
            "id": new_tecnical_resource.id,
            "userId": f"{new_tecnical_resource.userId}",
            "academicInformationIds": f"{new_academic_info[0]['ids']}",
            "professionalExperienceIds": f"{new_proffesional_experience[0]['ids']}",
            "aditionalInformationId": f"{new_aditional_info[0]['id']}"
        }, 201

    except Exception as e:
        return {
            "Error": e
        }, 400


def AcademicInformationCreate(tecnical_resource_id, academic_info):
    ids = []
    for academic in academic_info:
        new_academic_info = AcademicInformation(
            tecnicalResourceId = tecnical_resource_id,
            schoolName = academic.get('schoolName', None),
            educationLevel = academic.get('educationLevel', None),
            professionalSector = academic.get('professionalSector', None),
            startDate = academic.get('startDate', None),
            endDate = academic.get('endDate', None),
        )
        db.session.add(new_academic_info)
        db.session.commit()
        ids.append(new_academic_info.id)

    return {
        "ids": ids
    }, 201

def ProfessionalExperienceCreate(tecnical_resource_id, professional_data):
    ids = []
    for professional in professional_data:
        new_proffesional_experience = ProfessionalExperience(
            tecnicalResourceId = tecnical_resource_id,
            startDate = professional.get('startDate', None),
            endDate = professional.get('endDate', None),
            titleJob = professional.get('titleJob', None),
            companyName = professional.get('companyName', None),
            details = professional.get('details', None),
        )
        db.session.add(new_proffesional_experience)
        db.session.commit()
        ids.append(new_proffesional_experience.id)

    return {
        "ids": ids
    }, 201

def AditionalInformationCreate(tecnical_resource_id, aditional_data):
    new_aditional_info = AditionalInformation(
        tecnicalResourceId = tecnical_resource_id,
        driverLicense = aditional_data.get('driverLicense', None),
        transferAvailability = aditional_data.get('transferAvailability', None),
        vehicule = aditional_data.get('vehicule', None),
    )
    db.session.add(new_aditional_info)
    db.session.commit()

    print(new_aditional_info)

    return {
        "id": new_aditional_info.id
    }, 201
