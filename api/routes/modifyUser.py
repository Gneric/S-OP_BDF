from flask_jwt_extended.view_decorators import jwt_required
from api.utils.functions import modUser
from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity
import sys

class ModifyUser(Resource):
    @jwt_required()
    def post(self):
        try:
            payload = get_jwt_identity()
            current_user = payload["current_id"]
            data = request.json.get('data','')
            print(data)
            user = {
                "userID" : data['userID'], 
                "profileImageUrl" : data['profileImageUrl'],
                "userName" : data['userName'],
                "name" : data['name'],
                "mail" : data['mail'],
                "phone": data['phone'],
                "isEnabled": data['isEnabled'],
                "role" : data['role']
            }
            permissions = data['permissions']
            if current_user == 1 or current_user == user['userID']:
                return modUser(user, permissions)
            else:
                return {"error": "correo o contraseña incorrecto"}, 401
        except:
            print(sys.exc_info()[1])
            return { 'error' : "error en lectura de variables" }, 400