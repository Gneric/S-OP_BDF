from os import getcwd
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.dataLoader import createFileProductosOtros
from api.utils.functions import *
from flask_restful import Resource
from flask import abort, request, send_from_directory
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


class GetTransitoNart(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        nart = request.json.get('nart','')
        try:
            return get_transito_nart(nart)
        except:
            return { 'error': 'error al obtener datos del nart ingresado' }, 400

class UpsertComparacionSOP(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data','')
        try:
            return upsert_comparacion_sop(data, current_user)
        except:
            return { 'error': 'error al retornar peticion de actualizacion' }, 400

class GetDBSOP(Resource):
    @jwt_required()
    def post(self):
        cleanDataFolder()
        current_user = get_jwt_identity()
        data = request.json.get('data','')
        filename = request_db_main(data['id'])
        if filename == "":
            return { 'error': 'error al obtener datos para dbmain' }, 400
        data_path = join(getcwd(),'api','data')
        try:
            result = send_from_directory(
                data_path, filename, as_attachment=True, environ=request.environ
            )
            result.headers['filename'] = filename
            return result
        except FileNotFoundError:
            abort(404)

class SetCurrency(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data','')
        try:
            return upsert_conversion_moneda(data, current_user)
        except:
            return { 'error': 'error al retornar peticion de ingreso/actualizacion de valor EUR' }, 400

class GetCurrency(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            return get_conversion_moneda()
        except:
            return { 'error': 'error al retornar peticion de ingreso/actualizacion de valor EUR' }, 400

class SaveRiskOPS(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data','')
        try:
            return save_risk_ops(data)
        except:
            return { 'error': 'error al retornar peticion de ingreso/actualizacion de risk ops' }, 400