from flask_restful import Resource
from modelos.modelos import TypeIdentification, Genre, EducationLevel, UserType

class VistaTypesIdentification(Resource):
    def get(self):
        options = [type.name for type in TypeIdentification]
        return options, 200

class VistaGenders(Resource):
    def get(self):
        options = [genre.name for genre in Genre]
        return options, 200

class VistaEducationLevels(Resource):
    def get(self):
        options = [level.name for level in EducationLevel]
        return options, 200

class VistaUserTypes(Resource):
    def get(self):
        options = [type.name for type in UserType]
        return options, 200
