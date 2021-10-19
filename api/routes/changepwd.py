from flask_jwt_extended.view_decorators import jwt_required
from api.utils.functions import logUser, modUser, pwdChange
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
import sys

class ChangePassword(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            user_id = request.json.get('user_id','')
            pwd = request.json.get('password','')
            new_pwd = request.json.get('new_password','')
            if current_user == user_id:
                return pwdChange(user_id, pwd, new_pwd)
            else:
                return {"msg": "No tiene permisos para hacer cambios en este usuario"}, 401
        except:
            print(sys.exc_info()[1])
            return { 'error' : "correo o contraseña incorrecto" }, 400