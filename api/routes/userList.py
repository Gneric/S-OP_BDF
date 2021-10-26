from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request

from api.utils.functions import userInfo


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