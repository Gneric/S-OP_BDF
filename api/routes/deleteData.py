from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.functions import checkDeleteTable
from flask_restful import Resource
from flask import request


class DeleteData(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            print(f"{current_user=}")
            if 'year' in request.form.keys():
                year = str(request.form['year'])
            if 'month' in request.form.keys():
                month = str(request.form['month'])
            if 'area_id' in request.form.keys():
                area_id = request.form["area_id"]
            else:
                return 'No se encuentran todas las varaibles necesarias', 400
            res = checkDeleteTable(area_id, year, month)
            if res == "":
                return "Error eliminando data del mes", 400
            else:
                return { "result" : res }
        except:
            return "Error buscando data del mes", 400