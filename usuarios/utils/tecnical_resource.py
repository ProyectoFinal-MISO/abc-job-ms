from datetime import datetime

from flask import request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from flask_restful import Resource
# from strgen import StringGenerator
import hashlib

from modelos.modelos import Usuario, db, TecnicalResource, ProfessionalExperience, AcademicInformation, AditionalInformation, TecnicalResourceProgrammingLanguages, TecnicalResourceLanguages, TecnicalResourcePersonalSkills

def TecnicalResourceCreate(userId = None, user_data = None):

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
            age = personal_data.get('age', None),
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

        print(new_tecnical_resource)

        new_academic_info = AcademicInformationCreate(new_tecnical_resource.id, academic_data)
        new_proffesional_experience = ProfessionalExperienceCreate(new_tecnical_resource.id, professional_data)
        new_aditional_info = AditionalInformationCreate(new_tecnical_resource.id, aditional_data)

        tr_programming_languages = user_data['programmingLanguages']
        tr_languages = user_data['languages']
        tr_personal_skills = user_data['personalSkills']

        new_tr_programming_languages = TecnicalResourceProgrammingLanguagesCreate(new_tecnical_resource.id, tr_programming_languages)
        new_tr_languages = TecnicalResourceLanguagesCreate(new_tecnical_resource.id, tr_languages)
        new_tr_personal_skills = TecnicalResourcePersonalSkillsCreate(new_tecnical_resource.id, tr_personal_skills)


        if new_academic_info[1] != 201 or new_proffesional_experience[1] != 201 or new_aditional_info[1] != 201 or new_tr_programming_languages[1] != 201 or new_tr_languages[1] != 201 or new_tr_personal_skills[1] != 201:
            return Response(status=400)

        return {
            "id": new_tecnical_resource.id,
            "userId": f"{new_tecnical_resource.userId}",
            "academicInformationIds": f"{new_academic_info[0]['ids']}",
            "professionalExperienceIds": f"{new_proffesional_experience[0]['ids']}",
            "aditionalInformationId": f"{new_aditional_info[0]['id']}",
            "programmingLanguagesIds": f"{new_tr_programming_languages[0]['ids']}",
            "languagesIds": f"{new_tr_languages[0]['ids']}",
            "personalSkillsIds": f"{new_tr_personal_skills[0]['ids']}"
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

    return {
        "id": new_aditional_info.id
    }, 201

def TecnicalResourceProgrammingLanguagesCreate(tecnical_resource_id, tr_programming_languages):
    ids = []
    for programming_language in tr_programming_languages:
        new_tr_programming_languages = TecnicalResourceProgrammingLanguages(
            tecnicalResourceId = tecnical_resource_id,
            name = programming_language.get('name', None),
            score = programming_language.get('score', None),
        )
        db.session.add(new_tr_programming_languages)
        db.session.commit()
        ids.append(new_tr_programming_languages.id)

    return {
        "ids": ids
    }, 201

def TecnicalResourceLanguagesCreate(tecnical_resource_id, tr_languages):
    ids = []
    for language in tr_languages:
        new_tr_languages = TecnicalResourceLanguages(
            tecnicalResourceId = tecnical_resource_id,
            language = language.get('language', None),
            score = language.get('score', None),
        )
        db.session.add(new_tr_languages)
        db.session.commit()
        ids.append(new_tr_languages.id)

    return {
        "ids": ids
    }, 201

def TecnicalResourcePersonalSkillsCreate(tecnical_resource_id, tr_personal_skills):
    ids = []
    for personal_skill in tr_personal_skills:
        new_tr_personal_skills = TecnicalResourcePersonalSkills(
            tecnicalResourceId = tecnical_resource_id,
            name = personal_skill.get('name', None),
            score = personal_skill.get('score', None),
        )
        db.session.add(new_tr_personal_skills)
        db.session.commit()
        ids.append(new_tr_personal_skills.id)

    return {
        "ids": ids
    }, 201

def TecnicalResourceDelete(tecnical_resource_id):
    try:
        AcademicInformationDelete(tecnical_resource_id)
        ProfessionalExperienceDelete(tecnical_resource_id)
        AditionalInformationDelete(tecnical_resource_id)

        tecnical_resource = TecnicalResource.query.filter_by(id = tecnical_resource_id).first()
        if tecnical_resource is None:
            return Response(status=404)
        db.session.delete(tecnical_resource)
        db.session.commit()
        return Response(status=204)
    except Exception as e:
        return {
            "Error": e
        }, 400

def AcademicInformationDelete(tecnical_resource_id):
    try:
        academic_info = AcademicInformation.query.filter_by(tecnicalResourceId = tecnical_resource_id).all()
        for academic in academic_info:
            db.session.delete(academic)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def ProfessionalExperienceDelete(tecnical_resource_id):
    try:
        proffesional_experience = ProfessionalExperience.query.filter_by(tecnicalResourceId = tecnical_resource_id).all()
        for professional in proffesional_experience:
            db.session.delete(professional)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def TecnicalResourceProgrammingLanguagesDelete(tecnical_resource_id):
    try:
        tr_programming_languages = TecnicalResourceProgrammingLanguages.query.filter_by(tecnicalResourceId = tecnical_resource_id).all()
        for programming_language in tr_programming_languages:
            db.session.delete(programming_language)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def TecnicalResourceLanguagesDelete(tecnical_resource_id):
    try:
        tr_languages = TecnicalResourceLanguages.query.filter_by(tecnicalResourceId = tecnical_resource_id).all()
        for language in tr_languages:
            db.session.delete(language)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def TecnicalResourcePersonalSkillsDelete(tecnical_resource_id):
    try:
        tr_personal_skills = TecnicalResourcePersonalSkills.query.filter_by(tecnicalResourceId = tecnical_resource_id).all()
        for personal_skill in tr_personal_skills:
            db.session.delete(personal_skill)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def AditionalInformationDelete(tecnical_resource_id):
    try:
        aditional_info = AditionalInformation.query.filter_by(tecnicalResourceId = tecnical_resource_id).all()
        for aditional in aditional_info:
            db.session.delete(aditional)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)
