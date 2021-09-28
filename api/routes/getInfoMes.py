from api.utils.functions import checkInfoMonth
from flask import request
from flask_restful import Resource


class GetInfoMes(Resource):
    def post(self):

        year = request.json['year']
        month = request.json['month']
        
        if year == "" or month == "":
            return 'No se encontro parametros de year y month', 400
        else:
            try:
                res = checkInfoMonth(year, month)
                return res
            except:
                return "Error buscando data del mes", 400