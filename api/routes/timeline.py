from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request

from api.utils.functions import getInfoTimeline, setInfoTimeline


class GetInfoTimeline(Resource):
    @jwt_required()
    def post(self):
        data = request.json.get('data', {})
        if data:
            return getInfoTimeline(data['permissionID'], data['timelineID'])
        else: 
            return { 'error': 'No se encontro "data"' }, 400

class SetInfoTimeline(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data', {})
        if data:
            return setInfoTimeline(data, current_user)
        else:
            return { 'error', 'No se enncontro "data"' }, 400