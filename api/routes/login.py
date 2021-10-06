from api.utils.functions import logUser
from flask_restful import Resource
from flask import request
import json, jwt, datetime, sys
key = "secret_key"
refresh_key = "secret_refresh_key"

class LogIn(Resource):
    def post(self):
        try:
            email = request.json.get('email', '')
            password = request.json.get('password', '')
            user = logUser(email, password)
            #token = jwt.encode({"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, key, algorithm="HS256")
            #refresh_token = jwt.encode({"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, refresh_key, algorithm="HS256")
            #decoded = jwt.decode(token, key, algorithms="HS256")
            #user["accessToken"] = token
            #user["refreshToken"] = refresh_token
            #print(f"{datetime.datetime.fromtimestamp(decoded['exp'])=}")
            return { 'userData' : user }, 200
        except:
            print(sys.exc_info()[1])
            return { 'email' : "correo o contraseña incorrecto" }