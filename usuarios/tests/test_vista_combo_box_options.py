import json
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from modelos.modelos import Country, State, City
from vistas.combo_box_options import VistaTypesIdentification, VistaGenders, VistaEducationLevels, VistaUserTypes

class TestVistaComboBoxOptions:

    def test_get_type_identification(self):
        # Call the endpoint
        response, status_code = VistaTypesIdentification().get()
        assert status_code == 200
        assert response[0] == "CC"

    def test_get_genre(self):
        # Call the endpoint
        response, status_code = VistaGenders().get()
        assert status_code == 200
        assert response[0] == "MALE"

    def test_get_education_level(self):
        # Call the endpoint
        response, status_code = VistaEducationLevels().get()
        assert status_code == 200
        assert response[0] == "PRIMARY_SCHOOL"

    def test_get_user_type(self):
        # Call the endpoint
        response, status_code = VistaUserTypes().get()
        assert status_code == 200
        assert response[0] == "PERSON"
