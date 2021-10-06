from api.utils.functions import logUser
from flask_restful import Resource
from flask import request
import json


class LogIn(Resource):
    def post(self):
        username = request.json.get('username', '')
        password = request.json.get('password', '')
        user = logUser(username, password)
        return { 'userData' : user }, 200

