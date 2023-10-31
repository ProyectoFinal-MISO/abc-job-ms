from flask_restful import Resource
from modelos.modelos import Languages

class VistaLanguage(Resource):

    def get(self):

        ai = Languages.query.all()
        response = []
        if ai:
            for i in ai:
                response.append({
                    'id': i.id,
                    'name': i.name,
                    'code': i.code
                })
        return response, 200
