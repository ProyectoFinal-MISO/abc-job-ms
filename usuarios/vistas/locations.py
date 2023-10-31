from flask_restful import Resource
from modelos.modelos import Country, State, City

class VistaLocationCountries(Resource):
    def get(self):
        co = Country.query.all()
        response = []
        if co:
            for i in co:
                response.append({
                    'id': i.id,
                    'name': i.name,
                    'code': i.code
                })
        return response, 200

class VistaLocationStates(Resource):
    def get(self, id_country):
        st = State.query.filter_by(countryId=id_country).all()
        st_response = []
        if st:
            for j in st:
                st_response.append({
                    'id': j.id,
                    'name': j.name,
                    'code': j.code
                })
        return st_response, 200

class VistaLocationCities(Resource):
    def get(self, id_state):
        ci = City.query.filter_by(stateId=id_state).all()
        ci_response = []
        if ci:
            for k in ci:
                ci_response.append({
                    'id': k.id,
                    'name': k.name,
                    'code': k.code
                })
        return ci_response, 200
