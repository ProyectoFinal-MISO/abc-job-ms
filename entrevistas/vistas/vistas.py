from flask import Response, request, jsonify
from flask_restful import Resource
from psycopg2 import IntegrityError
from datetime import datetime
import os
import requests

from modelos.modelos import MeetSchema, GuestSchema, db, Guest, Meet

meet_schema = MeetSchema()
guest_schema = GuestSchema()

class VistaMeets(Resource):
    def post(self):
        try:
            token_response = validar_token()
            print(str(token_response))
            if token_response.status_code != 200:
                return {
                    "mensaje": "Expired session"
                }, token_response.status_code
            else:
                user = token_response.json()
                user_id = user.get('userId', None)
                user_type = user.get('userType', None)

                if user_id == None or user_type == None:
                    return {
                        "mensaje": "incomplete user"
                    }, 400              
                  
                if user_type != "EMPLOYEE":
                    return {
                        "mensaje": "Insufficient permits"
                    }, 400
                
                if not request.is_json:
                    return Response(status=400)
                
                response_json = request.get_json()
                required_params = ['tittle', 'description', 'start_date', 'end_date', 'place', 'guests']
                if not all(param in response_json for param in required_params):
                    return {"mensaje": "Missing required parameters"}, 400
                
                new_meet = Meet(
                    tittle = response_json['tittle'],
                    description = response_json['description'],
                    start_date = datetime.strptime(response_json['start_date'], "%Y-%m-%d %H:%M").date(),
                    end_date = datetime.strptime(response_json['end_date'], "%Y-%m-%d %H:%M").date(),
                    place = response_json['place'],
                    id_employee = user_id
                )
                db.session.add(new_meet)
                db.session.commit()

                for guest in list(set(response_json['guests'])):
                    guest_data = validar_invitado(guest)
                    if guest_data[0]:
                        new_guest = Guest(
                            id_user = guest,
                            name_user = guest_data[1],
                            email_user = guest_data[2],
                            type_user = guest_data[3],
                            id_meet = new_meet.id
                        )
                        db.session.add(new_guest)
                    else:
                        db.session.rollback()
                        db.session.delete(new_meet)
                        db.session.commit()
                        return {
                            "mensaje": "Invalid guest"
                        }, 400
                db.session.commit()
                return meet_schema.dump(new_meet), 201
            
        except IntegrityError as e:
            return {"mensaje": f"Database integrity error: {str(e)}"}, 412

        except Exception as e:
            return {"mensaje": f"An unexpected error occurred: {str(e)}"}, 500
        
    def get(self):
        token_response = validar_token()
        print(str(token_response))
        if token_response.status_code != 200:
            return {
                "mensaje": "Expired session"
            }, token_response.status_code
        else:
            user = token_response.json()
            user_type = user.get('userType', None)
            user_id = user.get('userId', 0)
            if user_type == "EMPLOYEE":                
                meets = Meet.query.filter((Meet.id_employee == user_id)).all()
            elif user_type == "COMPANY" or user_type == "PERSON":
                meets = db.session.query(Meet).join(Guest).filter(Guest.id_user == user_id).all()
            else:
                meets = Meet.query.all()
            return [meet_schema.dump(ca) for ca in meets], 200
        
class VistaMeet(Resource):
    def put(self, id_meet):
        try:
            token_response = validar_token()
            print(str(token_response))
            if token_response.status_code != 200:
                return {
                    "mensaje": "Expired session"
                }, token_response.status_code
            else:
                user = token_response.json()
                user_id = user.get('userId', None)
                user_type = user.get('userType', None)

                if user_id == None or user_type == None:
                    return {
                        "mensaje": "Incomplete user"
                    }, 400           
                meet:Meet = Meet.query.get(id_meet)                
                if not meet:
                    return {
                        "mensaje": "There is not a meet with that id"
                    }, 400            
                if user_type != "EMPLOYEE" or meet.id_employee != user_id:
                    return {
                        "mensaje": "Insufficient permits"
                    }, 400
                request_json = request.get_json()
                required_params = ['tittle', 'description', 'start_date', 'end_date', 'place']
                if not all(param in request_json for param in required_params):
                    return {"mensaje": "Missing required parameters"}, 400
                
                meet.tittle = request_json['tittle']
                meet.description = request_json['description']
                meet.start_date = datetime.strptime(request_json['start_date'], "%Y-%m-%d %H:%M").date()
                meet.end_date = datetime.strptime(request_json['end_date'], "%Y-%m-%d %H:%M").date()
                meet.place = request_json['place']
                db.session.commit()

                return meet_schema.dump(meet), 201                

        except IntegrityError as e:
            return {"mensaje": f"Database integrity error: {str(e)}"}, 412

        except Exception as e:
            return {"mensaje": f"An unexpected error occurred: {str(e)}"}, 500

class VistaGuest(Resource):
    def post(self, id_meet, id_user_guest):
        try:
            token_response = validar_token()
            print(str(token_response))
            if token_response.status_code != 200:
                return {
                    "mensaje": "Expired session"
                }, token_response.status_code
            else:
                user = token_response.json()
                user_id = user.get('userId', None)
                user_type = user.get('userType', None)
                if user_id == None or user_type == None:
                    return {
                        "mensaje": "incomplete user"
                    }, 400              
                meet:Meet = Meet.query.get(id_meet)                
                if not meet:
                    return {
                        "mensaje":"There is not a meet with that id"
                    }, 404            
                if user_type != "EMPLOYEE" or meet.id_employee != user_id:
                    return {
                        "mensaje": "Insufficient permits"
                    }, 400
                for i in meet.guests:
                   if i.id_user == id_user_guest:
                        return {
                            "mensaje":"There alredy exist a guest with that id in the meet"
                        }, 400  
                guest_data = validar_invitado(id_user_guest)
                if guest_data[0]:
                    new_guest = Guest(
                        id_user = id_user_guest,
                        name_user = guest_data[1],
                        email_user = guest_data[2],
                        type_user = guest_data[3],
                        id_meet = id_meet
                    )
                    db.session.add(new_guest)
                else:
                    return {
                        "mensaje": "Invalid guest"
                    }, 400
                db.session.commit()
                return meet_schema.dump(meet)

        except IntegrityError as e:
            return {"mensaje": f"Database integrity error: {str(e)}"}, 412

        except Exception as e:
            return {"mensaje": f"An unexpected error occurred: {str(e)}"}, 500
        
    def delete(self, id_meet, id_user_guest):
        try:
            token_response = validar_token()
            print(str(token_response))
            if token_response.status_code != 200:
                return {
                    "mensaje": "Expired session"
                }, token_response.status_code
            else:
                user = token_response.json()
                user_id = user.get('userId', None)
                user_type = user.get('userType', None)
                if user_id == None or user_type == None:
                    return {
                        "mensaje": "incomplete user"
                    }, 400              
                meet:Meet = Meet.query.get(id_meet)                
                if not meet:
                    return {
                        "mensaje":"There is not a meet with that id"
                    }, 404            
                if user_type != "EMPLOYEE" or meet.id_employee != user_id:
                    return {
                        "mensaje": "Insufficient permits"
                    }, 400
                guest = None
                for i in meet.guests:
                   if i.id_user == id_user_guest:
                        guest = i
                if not guest:
                    return {
                        "mensaje":"There is not a guest with that id in taht meet"
                    }, 404  
                else:
                    db.session.delete(guest)
                    db.session.commit()                
                    return Response(status=204)
                   
        except IntegrityError as e:
            return {"mensaje": f"Database integrity error: {str(e)}"}, 412

        except Exception as e:
            return {"mensaje": f"An unexpected error occurred: {str(e)}"}, 500

class VistaConfirmar(Resource):
    def put(self, flow, id_guest):
        try:
            token_response = validar_token()
            print(str(token_response))
            if token_response.status_code != 200:
                return {
                    "mensaje": "Expired session"
                }, token_response.status_code
            else:
                user = token_response.json()
                user_id = user.get('userId', None)
                user_type = user.get('userType', None)
                request_json = request.get_json()
                guest:Guest = Guest.query.get(id_guest)
                if flow == 'confirmar':
                    if guest.id_user != user_id:
                        return {
                            "mensaje": "Insufficient permits"
                        }, 400
                    if request_json.get('confirmar', None) == None:
                        return {
                            "mensaje": "There is not a propertie confirmar"
                        }, 400
                    guest.is_confirm = request_json['confirmar']
                    db.session.commit()
                    return guest_schema.dump(guest)
                if flow == 'calificar':
                    if user_type != 'EMPLOYEE':
                        return {
                            "mensaje": "Insufficient permits"
                        }, 400
                    if request_json.get('score', None) == None:
                        return {
                            "mensaje": "There is not a propertie confirmar"
                        }, 400
                    guest.score = request_json['score']
                    db.session.commit()
                    return guest_schema.dump(guest)
                return {
                    "mensaje": "Bad flow"
                }, 400

        except IntegrityError as e:
            return {"mensaje": f"Database integrity error: {str(e)}"}, 412

        except Exception as e:
            return {"mensaje": f"An unexpected error occurred: {str(e)}"}, 500

def validar_token():
    url = f"{os.getenv('USERS_PATH')}/users/user_session"
    headers = {'Authorization' : request.headers.get('Authorization')}
    return requests.get(url, headers=headers)

def validar_invitado(id):
    url = f"{os.getenv('USERS_PATH')}/users/validate/{id}"
    headers = {'Authorization' : request.headers.get('Authorization')}
    response =  requests.get(url, headers=headers)
    if response.status_code != 200:
        return [False]
    json = response.json()
    userType = json.get('userType', None)
    name = json.get('name', None)
    email = json.get('email', None)
    type_u = json.get('userType', None)
    if userType == "PERSON" or userType == "COMPANY":
        return True, name, email, type_u
    else:
        return False, name, email, type_u