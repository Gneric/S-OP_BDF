from api.utils.functions import getData
from flask import request
from flask_restful import Resource
import sys

class GetData(Resource):
    def post(self):
        id = request.json['file_id']
        area_id = request.json['area_id']

        if id == "" or area_id == "":
            return 'No se encontro parametros de id y/o area', 400
        
        else:
            try:
                res = getData(id, int(area_id))
                if res == "":
                    return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400
                return { "result" : res }, 200
            except:
                return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400