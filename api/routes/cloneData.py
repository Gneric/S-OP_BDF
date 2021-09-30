from api.utils.functions import cleanDataFolder, cloneData
from flask import request
from flask import send_from_directory, abort
from flask_restful import Resource
from os.path import join
from os import getcwd
import sys



class CloneData(Resource):
    def post(self):
        try:
            file_id = str(request.json['file_id'])
            area_id = int(request.json['area_id'])
            cleanDataFolder()
            res = cloneData(file_id, area_id)
            if res == "":
                return "Error clonando data del mes", 400
            else:
                data_path = join(getcwd(),'api','data')
                try:
                    return send_from_directory(
                        data_path, res, as_attachment=True
                    )
                except FileNotFoundError:
                    abort(404)
        except:
            return f"Error buscando data del mes, {sys.exc_info()[1]}", 400