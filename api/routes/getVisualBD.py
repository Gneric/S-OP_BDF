from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.functions import getVisualBD
from flask import request
from flask_restful import Resource
import sys

class GetVisualBD(Resource):
    # @jwt_required()
    def post(self):
        # current_user = get_jwt_identity()
        # print(f"{current_user=}")
        try:
            res = getVisualBD()
            if res == "":
                return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400
            return { "result" : res }, 200
        except:
            return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400