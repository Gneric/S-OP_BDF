from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.functions import *
from flask_restful import Resource
from flask import request

class GetInfoDB_Main(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data', '')
        if data == '':
            return { 'error': 'error en la lectura de data' }, 400
        res = getinfo_db_main(data)
        if res == 0:
            return { 'error': 'error al obtener datos' }, 400
        if res.get('error','') != '':
            return res, 200
        return res, 200

class UpdateDB_Main(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data', '')
        if data == '':
            return { 'error': 'error en la lectura de data' }, 400
        res = update_db_main(data)
        if res == 0:
            return { 'error': 'error actualizar data' }, 400
        insert_audit(7, 2, 0, 0, 0, 0, current_user)
        return { 'result' : 'ok' }, 200

class CargarDBMain(Resource):
    @jwt_required()
    def post(self):
        if request.json != None:
            id = request.json.get('id', '')
        else:
            id = ""
        current_user = get_jwt_identity()
        return request_cargar_db_main(id, current_user)  
        
class CerrarMesDBMain(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        return request_cerrar_mes(current_user)

class AddMultipleRows(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data', '')
        if data == '':
            return { 'error': 'error en la lectura de data' }, 400
        return add_multiple_rows(data, current_user)