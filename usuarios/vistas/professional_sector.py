from flask_restful import Resource
from modelos.modelos import ProfessionalSector

class VistaProfessionalSector(Resource):

    def get(self):
        ai = ProfessionalSector.query.all()
        response = []
        if ai:
            for i in ai:
                response.append({
                    'id': i.id,
                    'name': i.name,
                    'code': i.code
                })
        return response, 200
