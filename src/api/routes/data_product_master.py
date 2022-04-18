from ntpath import join
import sys
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename, send_from_directory
from flask_restful import Resource, abort
from flask import request

from src.api.controllers.data_producto_master import *
from src.api.services.global_variables import allowed_extensions, checkFiles, cleanDataFolder

class UpdateProduct(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data','')
        if data:
            return request_update_product(data)
        else:
            return { 'error': 'error de lectura de variable data' }, 400

class UploadProduct(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        files = request.files.getlist('excel_file')
        cleanDataFolder()
        for f in files:
            if allowed_extensions(f.filename) == False:
                return { "error" : "extension del archivo adjunto no se encuentra en el listado de aprovados" }, 400
            else:
                f.save(join(DATA_PATH, secure_filename(f.filename)))
        if checkFiles() == 0:
            return { "error" : 'No files saved' }, 400
        else:                
            res = checkExcelProduct()
            cleanDataFolder()
            return res

class CloneProduct(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            cleanDataFolder()
            res = cloneMaestro()
            try:
                result = send_from_directory(
                    DATA_PATH, res, as_attachment=True, environ=request.environ
                )
                result.headers['filename'] = res
                return result
            except FileNotFoundError:
                    abort(404)
        except:
            print(sys.exc_info())
            return { 'error' : 'error en la creacion de archivo Maestro' }, 400            

class UpsertCategoryItem(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            data = request.json.get('data','')
            res = getUpsertCategory(data)
            return res
        except:
            print(sys.exc_info())
            return { 'error' : 'error en la insercion/actualizacion de maestro de categorias' }, 400


class DeleteCategoryItem(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            data = request.json.get('data','')
            res = delete_category_items(data)
            return res
        except:
            print(sys.exc_info())
            return { 'error' : 'error en la insercion/actualizacion de maestro de categorias' }, 400