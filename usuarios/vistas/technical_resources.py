from flask_restful import Resource
from modelos.modelos import db, TechnicalResource, AcademicInformation, ProfessionalExperience, TechnicalResourceProgrammingLanguages, TechnicalResourceLanguages, TechnicalResourcePersonalSkills, AditionalInformation
from flask import request, Response
from flask_jwt_extended import jwt_required

class VistaTechnicalResource(Resource):

    @jwt_required()
    def get(self, id_tr):
        try:
            id_tr = int(id_tr)
        except ValueError:
            return {'message': 'Technical resource id is not integer'}, 400

        tr = TechnicalResource.query.filter_by(id=id_tr).first()

        if tr:
            # Se consulta tablas adicionales para completar la informacion del recurso tecnico

            academic_information = AcademicInformationGet(tr.id)
            professional_experience = ProfessionalExperienceGet(tr.id)
            aditional_information = TechnicalResourceAditionalInfoGet(tr.id)
            programming_languages = ProgrammingLanguagesGet(tr.id)
            languages = LanguagesGet(tr.id)
            personal_skills = PersonalSkillsGet(tr.id)


            return {
                'id': tr.id,
                'name': tr.name,
                'lastName': tr.lastName,
                # TODO: retornar el tipo de identificacion
                #'typeIdentification': tr.typeIdentification,
                'identification': tr.identification,
                'birthdate': tr.birthdate,
                # TODO: retornar el genero
                # 'genre': tr.genre,
                'phoneNumber': tr.phoneNumber,
                'mobileNumber': tr.mobileNumber,
                'city': tr.city,
                'state': tr.state,
                'country': tr.country,
                'address': tr.address,
                'userId': tr.userId,
                'academicInformation': academic_information,
                'professionalExperience': professional_experience,
                'aditionalInformation': aditional_information,
                'programmingLanguages': programming_languages,
                'languages': languages,
                'personalSkills': personal_skills,
            }, 200
        else:
            return {'message': 'Technical resource not exist'}, 404

    @jwt_required()
    def delete(self, id_tr):
        try:
            id_tr = int(id_tr)
        except ValueError:
            return {'message': 'Technical resource id is not integer'}, 400

        tr = TechnicalResource.query.filter_by(id=id_tr).first()
        if tr:

            AcademicInformationDelete(id_tr)
            ProfessionalExperienceDelete(id_tr)
            AditionalInformationDelete(id_tr)
            ProgrammingLanguagesDelete(id_tr)
            LanguagesDelete(id_tr)
            PersonalSkillsDelete(id_tr)

            db.session.delete(tr)
            db.session.commit()
            return {'message': 'Technical resource deleted'}, 200
        else:
            return {'message': 'Technical resource not exist'}, 404

    @jwt_required()
    def put(self, id_tr):

        if not request.is_json:
            return Response(status=400)
        parse_json = request.get_json()
        if parse_json.get('name', None) and parse_json.get('lastName', None) and parse_json.get('typeIdentification', None) and parse_json.get('identification', None) and parse_json.get('phoneNumber', None) and parse_json.get('mobileNumber', None) and parse_json.get('city', None) and parse_json.get('state', None) and parse_json.get('country', None) and parse_json.get('address', None):
            try:
                id_tr = int(id_tr)
            except ValueError:
                return {'message': 'Technical resource id is not integer'}, 400

            tr = TechnicalResource.query.filter_by(id=id_tr).first()
            if tr:
                tr.name = parse_json.get('name', None)
                tr.lastName = parse_json.get('lastName', None)
                tr.typeIdentification = parse_json.get('typeIdentification', None)
                tr.identification = parse_json.get('identification', None)
                tr.birthdate = parse_json.get('birthdate', None)
                tr.genre = parse_json.get('genre', None)
                tr.phoneNumber = parse_json.get('phoneNumber', None)
                tr.mobileNumber = parse_json.get('mobileNumber', None)
                tr.city = parse_json.get('city', None)
                tr.state = parse_json.get('state', None)
                tr.country = parse_json.get('country', None)
                tr.address = parse_json.get('address', None)

                AcademicInformationUpdate(id_tr, parse_json.get('academicInformation', None))
                ProfessionalExperienceUpdate(id_tr, parse_json.get('professionalExperience', None))
                AditionalInformationUpdate(id_tr, parse_json.get('aditionalInformation', None))
                ProgrammingLanguagesUpdate(id_tr, parse_json.get('programmingLanguages', None))
                LanguagesUpdate(id_tr, parse_json.get('languages', None))
                PersonalSkillsUpdate(id_tr, parse_json.get('personalSkills', None))

                db.session.commit()
                return {'message': 'Technical resource was updated'}, 200
            else:
                return {'message': 'Technical resource not exist'}, 404
        else:
            return {'message': 'Field is missing'}, 400

def AcademicInformationGet(technical_resource_id):
    ai = AcademicInformation.query.filter_by(technicalResourceId=technical_resource_id).all()
    response = []
    if ai:
        for i in ai:
            response.append({
                'id': i.id,
                'schoolName': i.schoolName,
                'educationLevel': i.educationLevel,
                'professionalSector': i.professionalSector,
                'startDate': i.startDate.isoformat(),
                'endDate': i.endDate.isoformat(),
            })
    return response

def ProfessionalExperienceGet(technical_resource_id):
    ai = ProfessionalExperience.query.filter_by(technicalResourceId=technical_resource_id).all()
    response = []
    if ai:
        for i in ai:
            response.append({
                'id': i.id,
                'titleJob': i.titleJob,
                'companyName': i.companyName,
                'details': i.details,
                'startDate': i.startDate.isoformat(),
                'endDate': i.endDate.isoformat(),
            })
    return response

def ProgrammingLanguagesGet(technical_resource_id):
    pl = TechnicalResourceProgrammingLanguages.query.filter_by(technicalResourceId=technical_resource_id).all()
    response = []
    if pl:
        for i in pl:
            response.append({
                'id': i.id,
                'name': i.name,
                'score': i.score
            })
    return response

def LanguagesGet(technical_resource_id):
    l = TechnicalResourceLanguages.query.filter_by(technicalResourceId=technical_resource_id).all()
    response = []
    if l:
        for i in l:
            response.append({
                'id': i.id,
                'language': i.language,
                'score': i.score
            })
    return response

def PersonalSkillsGet(technical_resource_id):
    ps = TechnicalResourcePersonalSkills.query.filter_by(technicalResourceId=technical_resource_id).all()
    response = []
    if ps:
        for i in ps:
            response.append({
                'id': i.id,
                'name': i.name,
                'score': i.score
            })
    return response

def TechnicalResourceAditionalInfoGet(technical_resource_id):
    ai = AditionalInformation.query.filter_by(technicalResourceId=technical_resource_id).first()
    if ai:
        return {
            'id': ai.id,
            'driverLicense': ai.driverLicense,
            'transferAvailability': ai.transferAvailability,
            'vehicule': ai.vehicule
        }
    return {}



def AcademicInformationUpdate(technical_resource_id, academic_information):
    if academic_information:
        for ai in academic_information:
            if ai.get('id', None):
                academic = AcademicInformation.query.filter_by(id=ai['id']).first()
                if academic:
                    academic.schoolName = ai.get('schoolName', None)
                    academic.educationLevel = ai.get('educationLevel', None)
                    academic.professionalSector = ai.get('professionalSector', None)
                    academic.startDate = ai.get('startDate', None)
                    academic.endDate = ai.get('endDate', None)
                    db.session.commit()
            else:
                academic = AcademicInformation(
                    schoolName = ai.get('schoolName', None),
                    educationLevel = ai.get('educationLevel', None),
                    professionalSector = ai.get('professionalSector', None),
                    startDate = ai.get('startDate', None),
                    endDate = ai.get('endDate', None),
                    technicalResourceId = technical_resource_id
                )
                db.session.add(academic)
                db.session.commit()

def ProfessionalExperienceUpdate(technical_resource_id, professional_experience):
    if professional_experience:
        for pe in professional_experience:
            if pe.get('id', None):
                professional = ProfessionalExperience.query.filter_by(id=pe['id']).first()
                if professional:
                    professional.titleJob = pe.get('titleJob', None)
                    professional.companyName = pe.get('companyName', None)
                    professional.details = pe.get('details', None)
                    professional.startDate = pe.get('startDate', None)
                    professional.endDate = pe.get('endDate', None)
                    db.session.commit()
            else:
                professional = ProfessionalExperience(
                    titleJob = pe.get('titleJob', None),
                    companyName = pe.get('companyName', None),
                    details = pe.get('details', None),
                    startDate = pe.get('startDate', None),
                    endDate = pe.get('endDate', None),
                    technicalResourceId = technical_resource_id
                )
                db.session.add(professional)
                db.session.commit()

def AditionalInformationUpdate(technical_resource_id, aditional_information):
    if aditional_information:
        aditional = AditionalInformation.query.filter_by(technicalResourceId=technical_resource_id).first()
        if aditional:
            aditional.driverLicense = aditional_information.get('driverLicense', None)
            aditional.transferAvailability = aditional_information.get('transferAvailability', None)
            aditional.vehicule = aditional_information.get('vehicule', None)
            db.session.commit()
        else:
            aditional = AditionalInformation(
                driverLicense = aditional_information.get('driverLicense', None),
                transferAvailability = aditional_information.get('transferAvailability', None),
                vehicule = aditional_information.get('vehicule', None),
                technicalResourceId = technical_resource_id
            )
            db.session.add(aditional)
            db.session.commit()

def ProgrammingLanguagesUpdate(technical_resource_id, programming_languages):
    if programming_languages:
        for pl in programming_languages:
            if pl.get('id', None):
                programming_language = TechnicalResourceProgrammingLanguages.query.filter_by(id=pl['id']).first()
                if programming_language:
                    programming_language.name = pl.get('name', None)
                    programming_language.score = pl.get('score', None)
                    db.session.commit()
            else:
                programming_language = TechnicalResourceProgrammingLanguages(
                    name = pl.get('name', None),
                    score = pl.get('score', None),
                    technicalResourceId = technical_resource_id
                )
                db.session.add(programming_language)
                db.session.commit()

def LanguagesUpdate(technical_resource_id, languages):
    if languages:
        for l in languages:
            if l.get('id', None):
                language = TechnicalResourceLanguages.query.filter_by(id=l['id']).first()
                if language:
                    language.language = l.get('language', None)
                    language.score = l.get('score', None)
                    db.session.commit()
            else:
                language = TechnicalResourceLanguages(
                    language = l.get('language', None),
                    score = l.get('score', None),
                    technicalResourceId = technical_resource_id
                )
                db.session.add(language)
                db.session.commit()

def PersonalSkillsUpdate(technical_resource_id, personal_skills):
    if personal_skills:
        for ps in personal_skills:
            if ps.get('id', None):
                personal_skill = TechnicalResourcePersonalSkills.query.filter_by(id=ps['id']).first()
                if personal_skill:
                    personal_skill.name = ps.get('name', None)
                    personal_skill.score = ps.get('score', None)
                    db.session.commit()
            else:
                personal_skill = TechnicalResourcePersonalSkills(
                    name = ps.get('name', None),
                    score = ps.get('score', None),
                    technicalResourceId = technical_resource_id
                )
                db.session.add(personal_skill)
                db.session.commit()



def AcademicInformationDelete(technical_resource_id):
    try:
        academic_info = AcademicInformation.query.filter_by(technicalResourceId = technical_resource_id).all()
        for academic in academic_info:
            db.session.delete(academic)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def ProfessionalExperienceDelete(technical_resource_id):
    try:
        proffesional_experience = ProfessionalExperience.query.filter_by(technicalResourceId = technical_resource_id).all()
        for professional in proffesional_experience:
            db.session.delete(professional)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def ProgrammingLanguagesDelete(technical_resource_id):
    try:
        tr_programming_languages = TechnicalResourceLanguages.query.filter_by(technicalResourceId = technical_resource_id).all()
        for programming_language in tr_programming_languages:
            db.session.delete(programming_language)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def LanguagesDelete(technical_resource_id):
    try:
        tr_languages = TechnicalResourceLanguages.query.filter_by(technicalResourceId = technical_resource_id).all()
        for language in tr_languages:
            db.session.delete(language)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def PersonalSkillsDelete(technical_resource_id):
    try:
        tr_personal_skills = TechnicalResourcePersonalSkills.query.filter_by(technicalResourceId = technical_resource_id).all()
        for personal_skill in tr_personal_skills:
            db.session.delete(personal_skill)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)

def AditionalInformationDelete(technical_resource_id):
    try:
        aditional_info = AditionalInformation.query.filter_by(technicalResourceId = technical_resource_id).all()
        for aditional in aditional_info:
            db.session.delete(aditional)
            db.session.commit()
        return Response(status=204)
    except Exception as e:
        return Response(status=400)
