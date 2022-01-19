from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request

from api.utils.functions import getInfoTimeline, setInfoTimeline


class GetInfoTimeline(Resource):
    @jwt_required()
    def get(self):
        data = request.json.get('data', {})
        if data:
            return getInfoTimeline(data['permissionID'], data['timelineID'])
        else: 
            return { 'error': 'No se encontro "data"' }, 400

class SetInfoTimeline(Resource):
    @jwt_required()
    def post(self):
        data = request.json.get('data', {})
        if data:
            return setInfoTimeline(data)
        else:
            return { 'error', 'No se enncontro "data"' }, 400