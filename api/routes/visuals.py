from flask_jwt_extended.internal_utils import custom_verification_for_token
from api.utils.functions import get_db_historico, getDemandSimulationDB, getFCSimulation, getPrepareSummary, getSimmulationNetSales, getSimulationUnits, getVisualBD
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from flask_restful import Resource
import sys

class GetVisualBD(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"{current_user=}")
        try:
            res = getVisualBD()
            if res == "":
                return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400
            return { "result" : res }, 200
        except:
            return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400

class GetBDHistorico(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"{current_user=}")
        try:
            res = get_db_historico()
            if res == "":
                return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400
            return { "result" : res }, 200
        except:
            return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400

class PrepareSummary(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        id = request.json.get('id', '')
        print(f"{current_user=}")
        try:
            res = getPrepareSummary(id)
            if res == "":
                return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400
            return { "result" : res }, 200
        except:
            return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400

class UnitsxBPU(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"{current_user=}")
        try:
            res = getSimulationUnits()
            if res == "":
                return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400
            return { "result" : res }, 200
        except:
            return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400

class NetSalesxPBU(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"{current_user=}")
        try:
            res = getSimmulationNetSales()
            if res == "":
                return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400
            return { "result" : res }, 200
        except:
            return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400

class DemandSimulation(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"{current_user=}")
        try:
            res = getDemandSimulationDB()
            if res == "":
                return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400
            return { "result" : res }, 200
        except:
            return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400

class FCSimulation(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"{current_user=}")
        try:
            res = getFCSimulation()
            if res == "":
                return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400
            return { "result" : res }, 200
        except:
            return f"Error intentando obtener datos, {sys.exc_info()[0]}", 400