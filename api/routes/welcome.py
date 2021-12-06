from casl import ability
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.casl.permissions import ability_for
from flask_restful import Resource
from flask import jsonify

class Welcome(Resource):
    @jwt_required()
    def get(self):
        if 1 == 1:
            current_user = get_jwt_identity()
            ability = ability_for(int(current_user))
            home_json = { "Bienvenido": "" }, 200
            return home_json
        else:
            return 'Resource not found', 400