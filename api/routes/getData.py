from api.utils.functions import getData
from flask import request
from flask_restful import Resource

class GetData(Resource):
    def post(self):
        id = request.json['file_id']
        area = request.json['area_id']
        if id == "" or area == "":
            return 'No se encontro parametros de id y area', 400
        else:
            try:
                res = getData(id, area)
                return { "result" : res }, 200
            except:
                return "Error intentando obtener datos", 400