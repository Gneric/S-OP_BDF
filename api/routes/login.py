from api.utils.functions import logUser, generate_token
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
import sys

class LogIn(Resource):
    def post(self):
        try:
            print('Log in method')
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            user = logUser(email, password)
            if user == None:
                return {"error": "correo o contraseña incorrecto"}, 401
            payload = generate_token(user)
            token = create_access_token(identity=payload)
            refresh_token = create_refresh_token(identity=payload)
            return { 'userData' : user, "accessToken": token, "refreshToken": refresh_token }
        except:
            print(sys.exc_info()[1])
            return { 'error' : "correo o contraseña incorrecto" }, 400