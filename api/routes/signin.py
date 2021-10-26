from api.utils.functions import checkUser, createUser, signUser
from flask_restful import Resource
from flask import request
import json


class CreateUser(Resource):
    def post(self):
        try:
            data = request.json.get('data', '')
            new_user = {
                "username": data['userName'],
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
            return res, 200
        except:
            return { 'error', 'error en lectura de variables' }, 400

