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
            ability = ability_for(current_user)
            print(f"{current_user=}")
            print( ability.can('read', 'Auth') )
            print( ability.can('read', 'supply') )
            print( ability.can('read', 'Marketing') )
            print( ability.can('read', 'launch') )
            home_json = { "Bienvenido": "" }
            response = jsonify(home_json)
            return response
        else:
            return 'Resource not found', 400