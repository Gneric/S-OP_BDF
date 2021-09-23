from os import error
import requests
import json
hasura_endpoint = 'https://graph.sop.strategio.cloud/v1/graphql'
headers = {'Content-Type': 'application/json','x-hasura-admin-secret': 'x5cHTWnDb7N2vh3eJZYzamgsUXBVkw'}
area_by_table = {
    "Maestro_baseline" : { "area_id" : 1, "area_name" : "Supply"},
    "Maestro_launch" : { "area_id" : 2, "area_name" : "Marketing"},
    "Maestro_promo" : { "area_id" : 3, "area_name" : "Ventas"},
    "Maestro_valorizacion" : { "area_id" : 4, "area_name" : "Finanzas"},
}

def queryHasura(query, variables = ""):
    if variables == "":
        result = requests.post(hasura_endpoint, json={'query': query}, headers=headers)
    else:
        result = requests.post(hasura_endpoint, json={'query': query, 'variables': variables}, headers=headers)

    if result.status_code == 200:
        #print(json.dumps(result.json(), indent=4))
        return result.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(requests.status_code, query))

def requestIDbyPeriod(period):
    try:
        query = """
        query MyQuery($id: String) {
        Maestro_baseline(distinct_on: id, where: {id: {_eq: $id}}) {
            id
        }
        Maestro_launch(distinct_on: id, where: {id: {_eq: $id}}) {
            id
        }
        Maestro_promo(distinct_on: id, where: {id: {_eq: $id}}) {
            id
        }
        Maestro_valorizacion(distinct_on: id, where: {id: {_eq: $id}}) {
            id
        }
        }
        """
        res_insert = queryHasura(query, {"id" : period})
        print(res_insert)
        result = []
        for file in res_insert["data"]:
            if len(res_insert["data"][file]) > 0:
                result.append({ "area_id" : area_by_table[file]["area_id"], "area_name" : area_by_table[file]["area_name"], "file_id" : res_insert["data"][file][0]["id"] })
            else:
                result.append({ "area_id" : area_by_table[file]["area_id"], "area_name" : area_by_table[file]["area_name"], "file_id" : "" })
        return result
    except:
        print("error on requestIDbyPeriod")
        return ""

def sendDataBaseline(data):
    try:
        # SendInsert
        query = """
        mutation MyMutation($objects: [Maestro_baseline_insert_input!]!) {
            insert_Maestro_baseline(objects: $objects, on_conflict: {constraint: Maestro_baseline_pkey1, update_columns: cantidad}) {
                returning {
                    id
                }
            }
        }
        """
        res_insert = queryHasura(query, {"objects" : data})
        result = { "file_id" : res_insert["data"]["insert_Maestro_baseline"]["returning"][0]["id"], "area_name" : area_by_table["Maestro_baseline"]["area_name"] }
        return result
    except:
        return ""
    
def requestDataBaseline(id):
    try:
        query = """
        query MyQuery($id: String) {
            Maestro_baseline(where: {id: {_eq: $id}}) {
                id
                clasificacion
                nart
                descripcion
                year
                month
                cantidad
            }
        }
        """
        res_select = queryHasura(query, {"id" : id })
        colum_list = [ { 'prop' : i } for i in res_select["data"]["Maestro_baseline"][0].keys()]
        result = {
            "columns" : colum_list,
            "rows" : res_select["data"]["Maestro_baseline"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""


def sendDataLaunch(data):
    # SendInsert
    query = """
    mutation MyMutation($objects: [Maestro_launch_insert_input!] = {}) {
        insert_Maestro_launch(objects: $objects, on_conflict: {constraint: Maestro_launch_pkey, update_columns: cantidad}) {
            affected_rows
        }
    }
    """
    res_insert = queryHasura(query, {"objects" : data})
    return res_insert

def requestDataLaunch(id):
    # Request data
    query = """
    query MyQuery($id: String) {
        Maestro_launch(where: {id: {_eq: $id}}) {
            id
            clasificacion
            canal
            nart
            descripcion
            year
            month
            cantidad
        }
    }
    """
    res_select = queryHasura(query, {"id", id})
    colum_list = [ { 'prop' : i } for i in res_select["data"]["Maestro_launch"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_launch"]
    }
    return result


def sendDataPromo(data):
    # SendInsert
    query = """
    mutation insert_Maestro_promo($sqlData: [Maestro_promo_insert_input!]!) {
        insert_Maestro_promo(objects: $sqlData) {
            affected_rows
        }
    }
    """
    res_insert = queryHasura(query, {"sqlData" : data})
    return res_insert

def requestDataPromo(id):
    # Request data
    query = """
    query Maestro_promo {
        Maestro_promo {
            id
            created_at
            updated_at
        }
    }
    """
    res_select = queryHasura(query)
    colum_list = [ { 'prop' : i } for i in res_select["data"]["Maestro_promo"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_promo"]
    }
    return result

def sendDataValorizacion(data):
    # SendInsert
    query = """
    mutation insert_Maestro_valorizacion($sqlData: [Maestro_valorizacion_insert_input!]!) {
        insert_Maestro_valorizacion(objects: $sqlData) {
            affected_rows
        }
    }
    """
    res_insert = queryHasura(query, {"sqlData" : data})
    return res_insert

def requestDataValorizacion(id):
    # Request data
    query = """
    query Maestro_valorizacion {
        Maestro_valorizacion {
            id
            created_at
            updated_at
        }
    }
    """
    res_select = queryHasura(query)
    colum_list = [ { 'prop' : i } for i in res_select["data"]["Maestro_valorizacion"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_valorizacion"]
    }
    return result