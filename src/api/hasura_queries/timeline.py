from src.api.hasura_queries.base_query import queryHasura

def requestinfo_timeline(permissionID, timelineID):
    try:
        query = """
        query MyQuery($permissionID: Int, $timelineID: Int) {
            Permissions(where: {permissionID: {_eq: $permissionID}}) {
                isBlocked
            }
            Timeline(where: {id: {_eq: $timelineID}}) {
                estado
            }
        }
        """
        res = queryHasura(query, {'permissionID': permissionID, 'timelineID': timelineID})
        if permissionID == 0:
            permissions = permissionID
        else:
            permissions = res['data']['Permissions'][0]['isBlocked']
        timeline = res['data']['Timeline'][0]['estado']
        return { 'isBlocked': permissions, 'estado': timeline }
    except:
        return {}

def request_setinfo_timeline(data):
    try:
        permission = data['permission']
        timeline = data['timeline']
        if permission['id'] == 0:
            query = """
            mutation MyMutation($estado: Int, $timelineID: Int) {
                update_Timeline(where: {id: {_eq: $timelineID}}, _set: {estado: $estado}) {
                    affected_rows
                }
            }
            """
            res = queryHasura(query, { 'estado': timeline['estado'], 'timelineID': timeline['id'] })
            rows = res['data']['update_Timeline']['affected_rows']
            if rows == 1:
                return { 'result' : 'ok' }
        elif timeline['id'] != 0:
            permissionID = permission['id']
            isBlocked = permission['isBlocked']
            timelineID = timeline['id']
            timelineStatus = timeline['estado']
            query = """
            mutation MyMutation($permissionID: Int, $isBlocked: Int, $estado: Int, $timelineID: Int) {
                update_Permissions(where: {permissionID: {_eq: $permissionID}}, _set: {isBlocked: $isBlocked}) {
                    affected_rows
                }
                update_Timeline(where: {id: {_eq: $timelineID}}, _set: {estado: $estado}) {
                    affected_rows
                }
            }
            """
            res = queryHasura(query, {'permissionID': permissionID, 'isBlocked': isBlocked, 'estado': timelineStatus, 'timelineID': timelineID })
            rows = res['data']['update_Permissions']['affected_rows'] + res['data']['update_Timeline']['affected_rows']
            if rows == 2:
                return { 'result' : 'ok' }
        else:
            return {}
    except:
        return {}