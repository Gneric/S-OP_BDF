from flask import jsonify
from flask_restful import Resource

class Welcome(Resource):
    def get(self):
        if 1 == 1:
            home_json = { "Bienvenido": "" }
            response = jsonify(home_json)
            return response
        else:
            return 'Resource not found', 400