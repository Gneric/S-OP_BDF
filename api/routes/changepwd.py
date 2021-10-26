from flask_jwt_extended.view_decorators import jwt_required
from api.utils.functions import pwdChange
from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity
import sys

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
            if current_user == user_id or current_user == 1:
                return pwdChange(user_id, pwd, new_pwd)
            else:
                return { 'error': "No tiene permisos para hacer cambios en este usuario"}, 401
        except:
            print(sys.exc_info()[1])
            return { 'error' : "error en lectura de variables" }, 400