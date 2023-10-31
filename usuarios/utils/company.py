from flask import Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

from modelos.modelos import Usuario, db, Company

def CompanyCreate(userId = None, user_data = None):

    try:
        company_data = user_data['personalInformation']

        new_company = Company(
            name = company_data.get('name', None),
            typeIdentification = company_data.get('typeIdentification', None),
            identification = company_data.get('identification', None),
            phoneNumber = company_data.get('phoneNumber', None),
            mobileNumber = company_data.get('mobileNumber', None),
            city = company_data.get('city', None),
            state = company_data.get('state', None),
            country = company_data.get('country', None),
            address = company_data.get('address', None),
            photo = company_data.get('photo', None),
            userId = userId
        )
        db.session.add(new_company)
        db.session.commit()

        return {
            "id": new_company.id,
            "companyId": f"{new_company.userId}"
        }, 201

    except Exception as e:
        db.session.rollback()
        return {
            "Error": e
        }, 400
