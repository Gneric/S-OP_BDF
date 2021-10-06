from os import error
import requests
import json
import sys
hasura_endpoint = 'https://graph.sop.strategio.cloud/v1/graphql'
headers = {'Content-Type': 'application/json','x-hasura-admin-secret': 'x5cHTWnDb7N2vh3eJZYzamgsUXBVkw'}
area_by_table = {
    "Maestro_baseline" : { "area_id" : 1, "area_name" : "Supply"},
    "Maestro_launch" : { "area_id" : 2, "area_name" : "Marketing"},
    "Maestro_promo" : { "area_id" : 3, "area_name" : "Ventas"},
    "Maestro_valorizacion" : { "area_id" : 4, "area_name" : "Finanzas"},
    "Maestro_Shoppers" : { "area_id" : 5, "area_name" : "Shoppers"},
}

def getSizebyColumnName(size_list, name):
    try:
        values_list = [ x['size'] if x['name']==name else 'NULL' for x in size_list]
        value = list(filter(lambda a: a != 'NULL', values_list))[0]
        return value
    except:
        return 0

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
        Maestro_Shoppers(distinct_on: id, where: {id: {_eq: $id}}) {
            id
        }
        }
        """
        res_insert = queryHasura(query, {"id" : period})
        print(res_insert)
        result = []
        for file in res_insert["data"]:
            if len(res_insert["data"][file]) > 0:
                result.append({ "area_id" : area_by_table[file]["area_id"], "area_name" : area_by_table[file]["area_name"], "file_id" : res_insert["data"][file][0]["id"], "data" : [ {"file_id" : res_insert["data"][file][0]["id"], "mes": period[0:4]+"-"+period[4:]} ] })
            else:
                result.append({ "area_id" : area_by_table[file]["area_id"], "area_name" : area_by_table[file]["area_name"], "file_id" : "", "data": {"file_id": "", "mes": ""}})
        return result
    except:
        print("error on requestIDbyPeriod")
        print(sys.exc_info()[1])
        return ""

def checkUser(email):
    try:
        query = """
            query MyQuery($email: String) {
                Users(where: {isEnabled: {_eq: 1}, mail: {_eq: $email}}) {
                    userID
                    userName
                    profileImageUrl
                    mail
                    phone
                    UserType {
                        userTypeName
                    }
                }
            }
        """
        res_insert = queryHasura(query, {"email" : email})
        print(res_insert)
        result = res_insert["data"]["Users"][0]
        if result["userID"] == 1:
            user = {
                "id": result["userID"],
                "fullName" : result["userName"],
                "username" : result["userName"],
                "avatar": result["profileImageUrl"],
                "email": result["mail"],
                "role": result["UserType"]["userTypeName"],
                "ability" : [{ "action": "manage", "subject": "all" }]
            }
        else:
            user = {
                "id": result["userID"],
                "fullName" : result["userName"],
                "username" : result["userName"],
                "avatar": result["profileImageUrl"],
                "email": result["mail"],
                "role": result["UserType"]["userTypeName"],
                "ability" : [{ "action": "read", "subject": "Auth" }, { "action": "read", "subject": "Ventas" }]
            }
        return user
    except:
        ""
def checkPassword(email):
    try:
        query = """
            query MyQuery($email: String) {
                Users(where: {isEnabled: {_eq: 1}, mail: {_eq: $email}}) {
                    hash_password
                }
            }
        """
        res_insert = queryHasura(query, {"email" : email})
        print(res_insert)
        result = res_insert["data"]["Users"][0]
        return result
    except:
        ""

def insertUser(user):
    try:
        query = """
        mutation MyMutation($user: [Users_insert_input!] = {}) {
            insert_Users(objects: $user) {
                returning {
                    userName
                }
            }
        }
        """
        res_insert = queryHasura(query, {"user" : user})
        print(res_insert)
        result = res_insert["data"]["insert_Users"]["returning"][0]
        return result
    except:
        print(sys.exc_info()[1])
        return ""
        

#######################
###### BASELINE #######
#######################
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
        if len(res_select["data"]["Maestro_baseline"]) < 1:
            return "No existen datos para los parametros igresados"

        size_list = [{'name':'clasificacion','size':120},{'name':'nart','size':170},{'name':'descripcion','size':500}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_baseline"][0].keys()]
        result = {
            "columns" : colum_list,
            "rows" : res_select["data"]["Maestro_baseline"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""
def deleteDataBaseline(id):
    try:
        query = """
        mutation MyMutation($id: String) {
            delete_Maestro_baseline(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_baseline"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

#######################
####### LAUNCH ########
#######################
def sendDataLaunch(data):
    # SendInsert
    query = """
    mutation MyMutation($objects: [Maestro_launch_insert_input!] = {}) {
        insert_Maestro_launch(objects: $objects, on_conflict: {constraint: Maestro_launch_pkey, update_columns: cantidad}) {
            returning {
                id
            }
        }
    }
    """
    res_insert = queryHasura(query, {"objects" : data})
    result = { "file_id" : res_insert["data"]["insert_Maestro_launch"]["returning"][0]["id"], "area_name" : area_by_table["Maestro_launch"]["area_name"] }
    return result
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

    if len(res_select["data"]["Maestro_launch"]) < 1:
        return "No existen datos para los parametros igresados"

    size_list = [{'name':'clasificacion','size':120},{'name':'nart','size':170},{'name':'descripcion','size':500}]
    colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_launch"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_launch"]
    }
    return result
def deleteDataLaunch(id):
    try:
        query = """
        mutation MyMutation($id: String) {
            delete_Maestro_launch(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_launch"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

#######################
###### PROMOCION ######
#######################
def sendDataPromo(data):
    # SendInsert
    query = """
    mutation MyMutation($objects: [Maestro_promo_insert_input!] = {}) {
        insert_Maestro_promo(objects: $objects, on_conflict: {constraint: Maestro_promo_pkey, update_columns: cantidad}) {
            returning {
                id
            }
        }
    }

    """
    res_insert = queryHasura(query, {"objects" : data})
    result = { "file_id" : res_insert["data"]["insert_Maestro_promo"]["returning"][0]["id"], "area_name" : area_by_table["Maestro_promo"]["area_name"] }
    return result
def requestDataPromo(id):
    # Request data
    query = """
    query MyQuery($id: String) {
        Maestro_promo(where: {id: {_eq: $id}}) {
            id
            clasificacion
            tipo_promo
            canal
            application_form
            nart
            descripcion
            year
            month
            cantidad
        }
    }
    """
    res_select = queryHasura(query, {"id" : id })

    if len(res_select["data"]["Maestro_promo"]) < 1:
        return "No existen datos para los parametros igresados"

    size_list = [{'name':'clasificacion','size':120},{'name':'nart','size':170},{'name':'descripcion','size':500}]
    colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_promo"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_promo"]
    }
    return result
def deleteDataPromo(id):
    try:
        query = """
        mutation MyMutation($id: String) {
            delete_Maestro_promo(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_promo"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

#######################
#### VALORIZACION #####
#######################
def sendDataValorizacion(data):
    # SendInsert
    query = """
    mutation MyMutation($objects: [Maestro_valorizacion_insert_input!] = {}) {
        insert_Maestro_valorizacion(objects: $objects, on_conflict: {constraint: Maestro_valorizacion_pkey, update_columns: cantidad}) {
            returning {
                id
            }
        }
    }
    """
    res_insert = queryHasura(query, {"objects" : data})
    result = { "file_id" : res_insert["data"]["insert_Maestro_valorizacion"]["returning"][0]["id"], "area_name" : area_by_table["Maestro_valorizacion"]["area_name"] }
    return result
def requestDataValorizacion(id):
    # Request data
    query = """
    query MyQuery($id: String) {
        Maestro_valorizacion(where: {id: {_eq: $id}}) {
            id
            clasificacion
            nart
            descripcion
            year
            month
            value
            cantidad
        }
    }
    """
    res_select = queryHasura(query, {"id" : id })
    if len(res_select["data"]["Maestro_valorizacion"]) < 1:
        return "No existen datos para los parametros igresados"

    size_list = [{'name':'clasificacion','size':120},{'name':'nart','size':170},{'name':'descripcion','size':500}]
    colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_valorizacion"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_valorizacion"]
    }
    return result
def deleteDataValorizacion(id):
    try:
        query = """
        mutation MyMutation($id: String){
            delete_Maestro_valorizacion(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_valorizacion"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""
#######################
###### SHOPPER ######
#######################
def sendDataShoppers(data):
    # SendInsert
    query = """
    mutation MyMutation($objects: [Maestro_Shoppers_insert_input!] = {}) {
        insert_Maestro_Shoppers(objects: $objects, on_conflict: {constraint: Maestro_Shoppers_pkey, update_columns: cantidad}) {
            returning {
            id
            }
        }
    }
    """
    res_insert = queryHasura(query, {"objects" : data})
    result = { "file_id" : res_insert["data"]["insert_Maestro_promo"]["returning"][0]["id"], "area_name" : area_by_table["Maestro_promo"]["area_name"] }
    return result
def requestDataShoppers(id):
    # Request data
    query = """
    query MyQuery($id: String) {
        Maestro_Shoppers(where: {id: {_eq: $id}}) {
            id
            clasificacion
            tipo_promo
            canal
            application_form
            nart
            descripcion
            year
            month
            cantidad
        }
    }
    """
    res_select = queryHasura(query, {"id" : id })

    if len(res_select["data"]["Maestro_Shoppers"]) < 1:
        return "No existen datos para los parametros igresados"

    size_list = [{'name':'clasificacion','size':120},{'name':'nart','size':170},{'name':'descripcion','size':500}]
    colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_Shoppers"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_Shoppers"]
    }
    return result
def deleteDataShoppers(id):
    try:
        query = """
        mutation MyMutation($id: String) {
            delete_Maestro_Shoppers(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_Shoppers"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""
