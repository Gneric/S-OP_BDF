from os import getcwd
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import send_from_directory
from api.utils.dataLoader import createFileProductosOtros
from api.utils.functions import *
from flask_restful import Resource
from flask import request
import flask

class GetProductosSinClasificar(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        cleanDataFolder()
        try:
            res = createFileProductosOtros()
            if res:
                data_path = join(getcwd(),'api','data')
                #result = send_from_directory(data_path, res, as_attachment=True, environ=request.environ)
                result = flask.send_from_directory(data_path, res, as_attachment=True)
                result.headers['filename'] = res
                return result
            else:
                return { 'error': 'error en la generacion del archivo ProductosSinClasificar' }, 400
        except:
            return { 'error': 'error al obtener datos de productos otros' }, 400