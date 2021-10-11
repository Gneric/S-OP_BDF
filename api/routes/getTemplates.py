from api.utils.functions import cleanDataFolder, getTemplates
from flask import request
from flask import send_from_directory, abort
from flask_restful import Resource
from os.path import join
from os import getcwd
import sys

class GetTemplates(Resource):
    def post(self):
        try:
            year = str(request.json['year'])
            month = str(request.json['month'])
            area_id = int(request.json['area_id'])
            cleanDataFolder()
            res = getTemplates(year, month, area_id)
            if res == "":
                return "Error creando template", 400
            else:
                data_path = join(getcwd(),'api','data')
                try:
                    result = send_from_directory(
                        data_path, res, as_attachment=True
                    )
                    result.headers['filename'] = res
                    cleanDataFolder()
                    return result
                except FileNotFoundError:
                    abort(404)
        except:
            return f"Error buscando data del mes, {sys.exc_info()[1]}", 400