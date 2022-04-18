from src.api.hasura_queries.timeline import *


def getInfoTimeline(permissionID, timelineID):
    try:
        res = requestinfo_timeline(permissionID, timelineID)
        if res:
            return res
        else:
            return { 'error': 'error en la busqueda de informacion' }, 400
    except:
        return { 'error': 'error en la busqueda de informacion' }, 400

def setInfoTimeline(data):
    try:
        res = request_setinfo_timeline(data)
        if res:
            return res
        else:
            return { 'error': 'error en el retorno de informacion' }, 400
    except:
        return { 'error': 'error en la busqueda de informacion' }, 400