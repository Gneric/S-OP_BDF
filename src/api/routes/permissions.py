from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request

from src.api.controllers.permissions import getPermissionbyActions, updatePermissions

class GetPermissions(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            action = request.json.get('action', None)
            if current_user != "1":
                return { 'error': 'el usuario no tiene permisos para esta accion' }, 400
            else:
                res = getPermissionbyActions(action)
                return res
        except:
            return {'error':'error en lectura de varibales'},400

class UpdatePermissions(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            permissions = request.json.get('data', None)
            if current_user != "1":
                return { 'error': 'el usuario no tiene permisos para esta accion' }, 400
            else:
                res = updatePermissions(permissions)
                return res
        except:
            return {'error':'error en lectura de varibales'},400


