from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

class Welcome(Resource):
    @jwt_required()
    def get(self):
        if 1 == 1:
            current_user = get_jwt_identity()
            home_json = { "Bienvenido": "" }, 200
            return home_json
        else:
            return 'Resource not found', 400