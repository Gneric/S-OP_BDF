
import sys
from src.api.hasura_queries.users import getPermissions, updatePermissionByList


def getPermissionbyActions(action):
    try:
        permission_list = getPermissions(action)
        return  { 'result' : permission_list }, 200
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al retornar permisos" }, 400

def updatePermissions(permissions):
    try:
        rows_affected = updatePermissionByList(permissions)
        if rows_affected == "":
            return { "error" : "Error al actualizar permisos" }, 400
        else:
            return { 'result' : 'ok' }, 200
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al actualizar permisos" }, 400