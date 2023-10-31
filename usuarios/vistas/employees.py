from flask_restful import Resource
from modelos.modelos import db, Employee
from flask import request, Response
from flask_jwt_extended import jwt_required

class VistaEmployee(Resource):

    @jwt_required()
    def get(self, id_employee):

        try:
            id_employee = int(id_employee)
        except ValueError:
            return {'message': 'Employee id is not integer'}, 400

        employee = Employee.query.filter_by(id=id_employee).first()

        if employee:
            return {
                'id': employee.id,
                'name': employee.name,
                'lastName': employee.lastName,
                # TODO: retornar el tipo de identificacion
                #'typeIdentification': employee.typeIdentification,
                'identification': employee.identification,
                'phoneNumber': employee.phoneNumber,
                'mobileNumber': employee.mobileNumber,
                'city': employee.city,
                'state': employee.state,
                'country': employee.country,
                'address': employee.address,
                'photo': employee.photo,
                'userId': employee.userId,
            }, 200
        else:
            return {'message': 'Employee not exist'}, 404

    @jwt_required()
    def delete(self, id_employee):

        try:
            id_employee = int(id_employee)
        except ValueError:
            return {'message': 'Employee id is not integer'}, 400

        employee = Employee.query.filter_by(id=id_employee).first()
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return {'message': 'Employee deleted'}, 200
        else:
            return {'message': 'Employee not exist'}, 404

    @jwt_required()
    def put(self, id_employee):

        if not request.is_json:
            return Response(status=400)
        parse_json = request.get_json()
        if parse_json.get('name', None) and parse_json.get('lastName', None) and parse_json.get('typeIdentification', None) and parse_json.get('identification', None) and parse_json.get('phoneNumber', None) and parse_json.get('mobileNumber', None) and parse_json.get('city', None) and parse_json.get('state', None) and parse_json.get('country', None) and parse_json.get('address', None):
            try:
                id_employee = int(id_employee)
            except ValueError:
                return {'message': 'Employee id is not integer'}, 400

            employee = Employee.query.filter_by(id=id_employee).first()
            if employee:
                employee.name = parse_json.get('name', None)
                employee.lastName = parse_json.get('lastName', None)
                employee.typeIdentification = parse_json.get('typeIdentification', None)
                employee.identification = parse_json.get('identification', None)
                employee.phoneNumber = parse_json.get('phoneNumber', None)
                employee.mobileNumber = parse_json.get('mobileNumber', None)
                employee.city = parse_json.get('city', None)
                employee.state = parse_json.get('state', None)
                employee.country = parse_json.get('country', None)
                employee.address = parse_json.get('address', None)
                employee.photo = parse_json.get('photo', None)
                db.session.commit()
                return {'message': 'Employee was updated'}, 200
            else:
                return {'message': 'Employee not exist'}, 404
        else:
            return {'message': 'Field is missing'}, 400


