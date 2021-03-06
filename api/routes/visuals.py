from api.utils.functions import get_db_historico, getDemandSimulationDB, getFCSimulation, getGraphDataset, getPrepareSummary, getSimmulationNetSales, getSimulationUnits, getVisualBD, request_info_cobertura
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from flask_restful import Resource
import sys

class GetVisualBD(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            res = getVisualBD()
            if res == "":
                return { 'error': "Error intentando obtener datos" } , 400
            return { "result" : res }, 200
        except:
            return { 'error': "Error intentando obtener datos" } , 400

class GetBDHistorico(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            res = get_db_historico()
            if res == "":
                return { 'error': "Error intentando obtener datos" } , 400
            return { "result" : res }, 200
        except:
            return { 'error': "Error intentando obtener datos" } , 400

class PrepareSummary(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        filters = request.json.get('filters', '')
        try:
            res = getPrepareSummary(filters)
            if res == "":
                return { 'error': "Error intentando obtener datos" } , 400
            return { "result" : res }, 200
        except:
            print(sys.exc_info())
            return { 'error': "Error intentando obtener datos" } , 400

class UnitsxBPU(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            res = getSimulationUnits()
            if res == "":
                return { 'error': "Error intentando obtener datos" } , 400
            return { "result" : res }, 200
        except:
            return { 'error': "Error intentando obtener datos" } , 400

class NetSalesxPBU(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            res = getSimmulationNetSales()
            if res == "":
                return { 'error': "Error intentando obtener datos" } , 400
            return { "result" : res }, 200
        except:
            return { 'error': "Error intentando obtener datos" } , 400

class DemandSimulation(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            res = getDemandSimulationDB()
            if res == "":
                return { 'error': "Error intentando obtener datos" } , 400
            return { "result" : res }, 200
        except:
            return { 'error': "Error intentando obtener datos" } , 400

class FCSimulation(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            res = getFCSimulation()
            if res == "":
                return { 'error': "Error intentando obtener datos" } , 400
            return { "result" : res }, 200
        except:
            return { 'error': "Error intentando obtener datos" } , 400

class GraphDataset(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            res = getGraphDataset()
            if res == "":
                return { 'error': "Error intentando obtener datos" } , 400
            return { "result" : res }, 200
        except:
            return { 'error': "Error intentando obtener datos" } , 400

class GetCobertura(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data','')
        if data == "":
            return { 'error': 'no se encontraron los parametros de busqueda' }, 400
        try:
            res = request_info_cobertura(data)
            return res
        except:
            return { 'error': 'error haciendo la peticion de informacion' }, 400