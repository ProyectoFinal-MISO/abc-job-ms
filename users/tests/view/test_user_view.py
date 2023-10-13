

def setUp():
    pass
def test_ping(client):
    response = client.get("/users/ping")
    assert response.json == "Pong"


# def test_sign_up(client):
#     response = client.post("/users/", json={
#         "username": "jose",
#         "email": "j.garay@uniandes.edu.co",
#         "password": "joseluis"
#     })
#     assert response.status_code == 201

# def test_sign_in(client):
#     client.post("/users/", json={
#         "username": "luis",
#         "email": "jgaray@uniandes.edu.co",
#         "password": "joseluis"
#     })
#     response = client.post("/users/auth", json={
#             "username": "luis",
#             "password": "joseluis"
#         }
#     )
#     assert response.status_code == 200

# def test_users_me(client):
#     client.post("/users/", json={
#         "username": "garay",
#         "email": "garay@uniandes.edu.co",
#         "password": "joseluis"
#     })
#     response = client.post("/users/auth", json={
#         "username": "garay",
#         "password": "joseluis"
#     })
#     token = response.json["token"]
#     final_response = client.get("/users/me", headers={"Authorization": "Bearer "+token})
#     assert final_response.status_code == 200

# def test_users_me_no_token(client):
#     response = client.get("/users/me")
#     assert response.status_code == 400


