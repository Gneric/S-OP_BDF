from flask_jwt_extended.view_decorators import jwt_required
from api.utils.functions import logUser
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
import sys

class ModifyUser(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            user = {
                "userID" : request.json.get('userID',''),
                "profileImageUrl" : request.json.get('profileImageUrl',''),
                "userName" : request.json.get('userName',''),
                "name" : request.json.get('name',''),
                "mail" : request.json.get('mail',''),
                "phone": request.json.get('phone',''),
                "isEnabled": request.json.get('isEnabled',''),
                "role" : request.json.get('role',''),
                "permissions" : request.json.get('permissions','')
            }
            if user == None:
                return {"msg": "Bad username or password"}, 401
            token = create_access_token(identity=user['id'])
            refresh_token = create_refresh_token(identity=user['id'])
            return { 'userData' : user, "accessToken": token, "refreshToken": refresh_token }
        except:
            print(sys.exc_info()[1])
            return { 'error' : "correo o contraseña incorrecto" }, 400