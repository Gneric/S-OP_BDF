from src.api.hasura_queries.visuals import *

def getVisualBD():
    return db_last_id()

def get_db_historico():
    return requestVisualBD()

def getPrepareSummary(filters):
    return requestPrepareSummary(filters)

def getSimulationUnits():
    return demand_simulation_units()

def getSimmulationNetSales():
    return demand_simulation_netsales()

def getDemandSimulationDB():
    return demand_simulation_db()

def getFCSimulation():
    return fc_simulation()

def getGraphDataset():
    return graph_dataset()

def request_info_cobertura(data):
    try:
        res = request_cobertura(data)
        if res:
            return { 'result': res }
        else:
            return { 'error': 'error al retornar informacion' }, 400
    except:
        return { 'error': 'error haciendo la peticion de informacion' }, 400