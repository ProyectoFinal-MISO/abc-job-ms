from psycopg2 import IntegrityError

from modelos.modelos import Usuario, db, Company

def CompanyCreate(userId = None, user_data = None):

    try:
        company_data = user_data.get('personalInformation', {})

        required_params = ['name', 'typeIdentification', 'identification', 'phoneNumber', 'mobileNumber', 'city', 'state', 'country', 'address']
        if not all(param in company_data for param in required_params):
            return {"mensaje": "Missing required parameters"}, 400

        identification = company_data.get('identification')
        existing_employee = Company.query.filter_by(identification=identification).first()
        if existing_employee:
            return {"mensaje": f"An employee with identification {identification} already exists"}, 412

        new_employee = Company(
            name=company_data['name'],
            typeIdentification=company_data['typeIdentification'],
            identification=company_data['identification'],
            phoneNumber=company_data['phoneNumber'],
            mobileNumber=company_data['mobileNumber'],
            state=company_data['state'],
            city=company_data['city'],
            country=company_data['country'],
            address=company_data['address'],
            photo=company_data.get('photo'),
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
