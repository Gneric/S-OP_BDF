from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import get_jwt_identity
from api.utils.functions import createUser, userInfo, pwdChange, modUser
from flask_restful import Resource
from flask import request
import sys

class UserList(Resource):
    @jwt_required()
    def post(self):
        if 1 == 1:
            current_user = get_jwt_identity()
            print(f"{current_user=}")
            if request.json == None or 'id' not in request.json.keys():
                res = userInfo("")
            else:
                res = userInfo(request.json['id'])
            return res
        else:
            return 'Resource not found', 400

class CreateUser(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            print(f"{current_user=}")
            data = request.json.get('data', '')
            new_user = {
                "username": data['username'],
                "password": data['password'],
                "confirm_password": data['confirm_password'],
                "name": data['name'],
                "mail": data['mail'],
                "phone": data['phone'],
                "isEnabled": data['isEnabled'],
                "role": data['role']
            }
            if data['password'] != data['confirm_password']:
                return { 'error', 'las contraseñas no coinciden' }, 400
            res = createUser(new_user)
            return res
        except:
            return { 'error', 'error en lectura de variables' }, 400

class ChangePassword(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            user_id = request.json.get('user_id','')
            pwd = request.json.get('old_password','')
            new_pwd = request.json.get('new_password','')
            if current_user == 1:
                confirm_pwd = ""
            else:
                confirm_pwd = request.json.get('confirm_password', '')
                if confirm_pwd != new_pwd:
                    return { 'error': 'los campos de nueva contraseña no coinciden'}, 400
            if current_user == str(user_id) or current_user == "1":
                return pwdChange(user_id, pwd, new_pwd)
            else:
                return { 'error': "No tiene permisos para hacer cambios en este usuario"}, 401
        except:
            print(sys.exc_info()[1])
            return { 'error' : "error en lectura de variables" }, 400

class ModifyUser(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            data = request.json.get('data','')
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
            if current_user == "1" or current_user == str(user['userID']):
                return modUser(user, permissions)
            else:
                return {"error": "correo o contraseña incorrecto"}, 401
        except:
            print(sys.exc_info()[1])
            return { 'error' : "error en lectura de variables" }, 400