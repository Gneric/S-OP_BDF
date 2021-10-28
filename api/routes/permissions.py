from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request

from api.utils.functions import getPermissionbyActions

class GetPermissions(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            print(f"{current_user=}")
            action = request.json.get('action', None)
            if current_user != 1:
                return { 'error': 'el usuario no tiene permisos para esta accion' }, 400
            else:
                res = getPermissionbyActions(action)
                return { 'result' : res }, 200
        except:
            return {'error':'error en lectura de varibales'},400

class UpdatePermissions(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            print(f"{current_user=}")
            permissions = request.json.get('data', None)
            if current_user != 1:
                return { 'error': 'el usuario no tiene permisos para esta accion' }, 400
            else:
                res = updatePermissions(permissions)
        except:
            return {'error':'error en lectura de varibales'},400


