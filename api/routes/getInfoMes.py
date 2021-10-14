from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.functions import checkInfoMonth
from flask import request
from flask_restful import Resource


class GetInfoMes(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"{current_user=}")
        year = str(request.json['year'])
        month = str(request.json['month'])

        if year == "" or month == "":
            return 'No se encontro parametros de year y month', 400
        else:
            try:
                res = checkInfoMonth(year, month)
                return res
            except:
                return "Error buscando data del mes", 400