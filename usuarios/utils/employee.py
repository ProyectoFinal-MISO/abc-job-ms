from flask import Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

from modelos.modelos import Usuario, db, Employee

def EmployeeCreate(userId = None, user_data = None):

    try:
        personal_data = user_data['personalInformation']

        name = personal_data.get('name', None)
        lastName = personal_data.get('lastName', None)
        typeIdentification = personal_data.get('typeIdentification', None)
        identification = personal_data.get('identification', None)
        phoneNumber = personal_data.get('phoneNumber', None)
        mobileNumber = personal_data.get('mobileNumber', None)
        city = personal_data.get('city', None)
        state = personal_data.get('state', None),
        country = personal_data.get('country', None)
        address = personal_data.get('address', None)
        photo = personal_data.get('photo', None)

        if (not name) or (not lastName) or (not typeIdentification) or (not identification) or (not phoneNumber) or (not mobileNumber) or (not city) or (not state) or (not country) or (not address):
            return {"mensaje": f"Missing parameter"}, 400

        if identification:
            employies = Employee.query.filter_by(identification=identification).all()
            if len(employies):
                return {"mensaje": f"Alredy exist a employee with the identification {identification}"}, 412


        new_employee = Employee(
            name = name,
            lastName = lastName,
            typeIdentification = typeIdentification,
            identification = identification,
            phoneNumber = phoneNumber,
            mobileNumber = mobileNumber,
            city = city,
            state = state,
            country = country,
            address = address,
            photo = photo,
            userId = userId
        )
        db.session.add(new_employee)
        db.session.commit()

        return {
            "id": new_employee.id,
            "employeeId": f"{new_employee.userId}"
        }, 201

    except Exception as e:
        db.session.rollback()
        return {
            "mensaje": f"{e}"
        }, 500
