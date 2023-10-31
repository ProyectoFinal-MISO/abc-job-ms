import json
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from modelos.modelos import Country, State, City
from vistas.locations import VistaLocationCountries, VistaLocationStates, VistaLocationCities


class TestVistaLocations:

    @patch('vistas.locations.Country.query.all')
    def test_get_locations_country(self, mock_country_query):
        # Mock data
        country = Country(name='Colombia', code='CO')
        state = State(name='Antioquia', code='ANT', countryId=1)
        city = City(name='Medellin', code='MDE', stateId=1)
        state.cities = [city]
        country.states = [state]
        mock_country_query.return_value = [country]

        # Call the endpoint
        response, status_code = VistaLocationCountries().get()
        assert status_code == 200

    @patch('vistas.locations.State.query.all')
    def test_get_locations_state(self, mock_country_query):
        # Mock data
        country = Country(name='Colombia', code='CO')
        state = State(name='Antioquia', code='ANT', countryId=1)
        city = City(name='Medellin', code='MDE', stateId=1)
        state.cities = [city]
        country.states = [state]
        mock_country_query.return_value = [country]

        # Call the endpoint
        response, status_code = VistaLocationStates().get(1)
        assert status_code == 200

    @patch('vistas.locations.City.query.all')
    def test_get_locations_city(self, mock_country_query):
        # Mock data
        country = Country(name='Colombia', code='CO')
        state = State(name='Antioquia', code='ANT', countryId=1)
        city = City(name='Medellin', code='MDE', stateId=1)
        state.cities = [city]
        country.states = [state]
        mock_country_query.return_value = [country]

        # Call the endpoint
        response, status_code = VistaLocationCities().get(1)
        assert status_code == 200
