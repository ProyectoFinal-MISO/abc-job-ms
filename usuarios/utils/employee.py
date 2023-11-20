
from psycopg2 import IntegrityError

from modelos.modelos import Usuario, db, Employee

def EmployeeCreate(userId=None, user_data=None):
    try:
        personal_data = user_data.get('personalInformation', {})

        required_params = ['name', 'lastName', 'typeIdentification', 'identification', 'phoneNumber', 'mobileNumber', 'city', 'state', 'country', 'address']
        if not all(param in personal_data for param in required_params):
            return {"mensaje": "Missing required parameters"}, 400

        identification = personal_data.get('identification')
        existing_employee = Employee.query.filter_by(identification=identification).first()
        if existing_employee:
            return {"mensaje": f"An employee with identification {identification} already exists"}, 412

        new_employee = Employee(
            name=personal_data['name'],
            lastName=personal_data['lastName'],
            typeIdentification=personal_data['typeIdentification'],
            identification=personal_data['identification'],
            phoneNumber=personal_data['phoneNumber'],
            mobileNumber=personal_data['mobileNumber'],
            state=personal_data['state'],
            city=personal_data['city'],
            country=personal_data['country'],
            address=personal_data['address'],
            photo=personal_data.get('photo'),
            userId=userId
        )

        db.session.add(new_employee)
        db.session.commit()

        return {
            "id": new_employee.id,
            "employeeId": str(new_employee.userId)
        }, 201

    except IntegrityError as e:
        db.session.rollback()
        return {"mensaje": f"Database integrity error: {str(e)}"}, 500

    except Exception as e:
        db.session.rollback()
        return {"mensaje": f"An unexpected error occurred: {str(e)}"}, 500
