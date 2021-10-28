from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import get_jwt_identity
from api.utils.functions import createUser
from flask_restful import Resource
from flask import request


class CreateUser(Resource):
    @jwt_required()
    def post(self):
        try:
            payload = get_jwt_identity()
            current_user = payload["current_id"]
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