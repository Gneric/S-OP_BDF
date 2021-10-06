from api.utils.functions import checkUser, signUser
from flask_restful import Resource
from flask import request
import json


class SignIn(Resource):
    def post(self):
        username = request.json.get('username', '')
        mail = request.json.get('mail', '')
        phone = request.json.get('phone', '')
        password = request.json.get('password', '')
        result = signUser(username, mail, phone, password)
        return result, 200

