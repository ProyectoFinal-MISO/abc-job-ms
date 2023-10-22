from flask import Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

from modelos.modelos import Usuario, db, Employee

def EmployeeCreate(userId = None, user_data = None):

    try:
        personal_data = user_data['personalInformation']

        new_employee = Employee(
            name = personal_data.get('name', None),
            lastName = personal_data.get('lastName', None),
            typeIdentification = personal_data.get('typeIdentification', None),
            identification = personal_data.get('identification', None),
            phoneNumber = personal_data.get('phoneNumber', None),
            mobileNumber = personal_data.get('mobileNumber', None),
            city = personal_data.get('city', None),
            state = personal_data.get('state', None),
            country = personal_data.get('country', None),
            address = personal_data.get('address', None),
            userId = userId
        )
        db.session.add(new_employee)
        db.session.commit()

        return {
            "id": new_employee.id,
            "employeeId": f"{new_employee.userId}"
        }, 201

    except Exception as e:
        return {
            "Error": e
        }, 400
