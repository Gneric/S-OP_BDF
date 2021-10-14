from api.casl.permissions import ability_for
from api.utils.functions import logUser
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
            print(f"{user=}")
            if user == None:
                return {"msg": "Bad username or password"}, 401
            print('Creando tokens')
            token = create_access_token(identity=user['id'])
            refresh_token = create_refresh_token(identity=user['id'])
            return { 'userData' : user, "access_token": token, "refresh_token": refresh_token }
        except:
            print(sys.exc_info()[1])
            return { 'error' : "correo o contraseña incorrecto" }, 400