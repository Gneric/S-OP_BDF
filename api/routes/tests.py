import sys
from os import getcwd
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request

from api.utils.functions import getActionTest

class ActionTest(Resource):
    def post(self):
        try:
            #current_user = get_jwt_identity()
            numbers = request.json['input']['arg1']['numbers']
            print(f"{request.json['input']}")
            print(f"{request.json['input']['arg1']}")
            print(f"{request.json['input']['arg1']['numbers']}")
            res = getActionTest(numbers)
            return res
        except:
            return {'error':'error en lectura de varibales'}, 400