from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.functions import cleanDataFolder, getTemplates
from flask import request
from flask import send_from_directory, abort
from flask_restful import Resource
from os.path import join
from os import getcwd
import sys

class GetTemplates(Resource):
    @jwt_required()
    def post(self):
        try:
            payload = get_jwt_identity()
            current_user = payload["current_id"]
            print(f"{current_user=}")
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