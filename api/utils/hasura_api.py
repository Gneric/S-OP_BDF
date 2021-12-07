from datetime import datetime, timedelta
import pandas as pd
from os import error
from pandas.core.indexes.base import Index
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
    "Maestro_Shopper" : { "area_id" : 5, "area_name" : "Shopper"},
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
        return result.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(requests.status_code, query))

def requestIDbyPeriod(period):
    try:
        query = """
        query MyQuery($id: String) {
            Maestro_baseline(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
            Maestro_launch(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
            Maestro_promo(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
            Maestro_valorizacion(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
            Maestro_Shopper(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
        }
        """
        res_insert = queryHasura(query, {"id" : period[:3]})
        
        result = []
        
        for file in res_insert["data"]:
            data = []
            file_id = ""
            if len(res_insert["data"][file]) > 0:
                for mes in res_insert["data"][file]:
                    if mes["id"] == period:
                        file_id = period
                for mes in res_insert["data"][file]:
                    if mes["id"] != period:
                        data.append({"file_id" : mes["id"], "mes": mes["id"][0:4]+"-"+mes["id"][4:]})
                result.append({ "area_id" : area_by_table[file]["area_id"], "area_name" : area_by_table[file]["area_name"], "file_id" : file_id, "data" : data })
            else:
                result.append({ "area_id" : area_by_table[file]["area_id"], "area_name" : area_by_table[file]["area_name"], "file_id" : "", "data": []})
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
            role
        }
        search_permissions(args: {email: $email}, where: {isEnabled: {_eq: 1}}) {
            action
            subject
            condition
        }
        }
        """
        res_insert = queryHasura(query, {"email" : email})
        result = res_insert["data"]["Users"][0]
        permissions = res_insert["data"]["search_permissions"]
        abilities = [ { "action": i['action'], "subject": i['subject'], "conditions": i['condition'] } if i['condition'] else { "action": i['action'], "subject": i['subject'] } for i in permissions ]
        user = {
            "id": result["userID"],
            "fullName" : result["userName"],
            "username" : result["userName"],
            "avatar": result["profileImageUrl"],
            "email": result["mail"],
            "role": result["role"],
            "ability" : abilities
        }
        return user
    except:
        print(sys.exc_info()[1])
        ""
def checkPassword(email):
    try:
        query = """
            query MyQuery($email: String) {
                Users(where: {mail: {_eq: $email}}) {
                    hash_password
                }
            }
        """
        res_insert = queryHasura(query, {"email" : email})
        result = res_insert["data"]["Users"][0]
        return result
    except:
        ""
def checkMailExists(email):
    try:
        query = """
        query MyQuery($mail: String) {
        Users(where: {mail: {_eq: $mail}}) {
        userName
        }
        }
        """
        res_insert = queryHasura(query, {"email" : email})
        result = res_insert["data"]["Users"]
        if len(result) > 0:
            return result[0]
        else:
            return ""
    except:
        ""
def checkPasswordByID(id):
    try:
        query = """
            query MyQuery($id: Int) {
                Users(where: {isEnabled: {_eq: 1}, userID: {_eq: $id}}) {
                    hash_password
                }
            }
        """
        res_insert = queryHasura(query, {"id" : id})
        result = res_insert["data"]["Users"][0]
        return result
    except:
        ""

def changepw(user_id, new_pwd):
    try:
        query = """
        mutation MyMutation($id: Int, $hash_password: String) {
            update_Users(where: {userID: {_eq: $id}}, _set: {hash_password: $hash_password}) {
                affected_rows
            }
        }
        """
        res_insert = queryHasura(query, {"id" : user_id, 'hash_password': new_pwd})
        result = res_insert["data"]["update_Users"]["affected_rows"]
        return result
    except:
        ""
def getPermissions(action):
    try:
        query = """
        query MyQuery($actions: [String!] = "") {
        Permissions(order_by: {permissionID: asc}, where: {action: {_in: $actions}}) {
            permissionID
            action
            subject
            conditions
            isBlocked
        }
        }
        """
        res = queryHasura(query, {'actions': action})
        return res['data']['Permissions']
    except:
        print(sys.exc_info()[1])
        return ""

def updatePermissionByList(permissions):
    try:
        query = """
        mutation MyMutation($objects: [Permissions_insert_input!] = {}) {
        insert_Permissions(objects: $objects, on_conflict: {constraint: Permissions_pkey, update_columns: isBlocked}) {
            affected_rows
        }
        }
        """
        res = queryHasura(query, {'objects': permissions})
        return res['data']['insert_Permissions']['affected_rows']
    except:
        print(sys.exc_info()[1])
        return ""

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
        result = res_insert['data']['insert_Users']['returning'][0]['userName']
        return result
    except:
        print(sys.exc_info()[1])
        print('except InsertUser')
        return ""
        
def checkPermissions(id):
    try:
        query = """
        query MyQuery($id: Int) {
        search_permissions_id(args: {id: $id}) {
            action
            subject
            conditions
        }
        }
        """
        res = queryHasura(query, {"id" : id})
        permissions = res["data"]["search_permissions_id"]
        return permissions
    except:
        print(sys.exc_info()[1])
        return []

def listUsers(id):
    try:
        if id:
            query = """
            query MyQuery($id: Int) {
            Users(where: {userID: {_eq: $id}}) {
                userID
                profileImageUrl
                userName
                name
                mail
                phone
                isEnabled
                role
            }
            search_permissions_id_edit(args: {id: $id}, where: {permissionID: {_gt: 3}}) {
                permissionID
                action
                subject
                condition
                isEnabled
            }
            }
            """
            res = queryHasura(query, { "id": id })
            data = res["data"]["Users"][0]
            abilities = res["data"]["search_permissions_id_edit"]
            permissions = [ { "permissionID": i['permissionID'], "action": i['action'], "subject": i['subject'], 'isEnabled': i['isEnabled'], "conditions": i['condition'] } if i['condition'] else { "permissionID": i['permissionID'], "action": i['action'], "subject": i['subject'], 'isEnabled': i['isEnabled'] } for i in abilities ]
            user = {
                "userID": data['userID'],
                "profileImageUrl": data['profileImageUrl'],
                "userName": data['userName'],
                "name": data['name'],
                "mail": data['mail'],
                "phone": data['phone'],
                "isEnabled": data['isEnabled'],
                "role" : data['role'],
                "permissions" : permissions
            }
            return user
        else:
            query = """
            query MyQuery {
                Users {
                        userID
                        profileImageUrl
                        userName
                        name
                        mail
                        isEnabled
                        role
                    }
                }
            """
            res = queryHasura(query)
            users = res["data"]["Users"]
            total = len(users)
            res = []
            for u in users:
                res.append({'userID': u['userID'],'profileImageUrl': u['profileImageUrl'], 'userName': u['userName'], 'name':u['name'], 'mail':u['mail'], 'isEnabled':u['isEnabled'], 'role': u['role'] })
            return { 'users' : res, 'total': total }
    except:
        print(sys.exc_info()[1])
        return []
def ListUsers():
    try:
        query = """
        query MyQuery {
            Users {
                    use
                    userName
                    name
                    mail
                    isEnabled
                    role
                }
            }
        }
        """
        res = queryHasura(query)
        users = res["data"]["Users"]
        return users
    except:
        print(sys.exc_info()[1])
        return []
def modifyUser(userData, permissions):
    try:
        query = """
        mutation MyMutation($permissions: [UserPermissions_insert_input!] = {}, $userData: [Users_insert_input!] = {}) {
        insert_Users(objects: $userData, on_conflict: {constraint: Users_mail_key, update_columns: [mail, userName, name, role, isEnabled]}) {
            affected_rows
        }
        insert_UserPermissions(objects: $permissions, on_conflict: {constraint: UserRoles_pkey, update_columns: isEnabled}) {
            affected_rows
        }
        }
        """
        res = queryHasura(query, {'permissions': permissions, 'userData': userData })
        return res
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

        size_list = [{'name':'clasificacion','size':120}, {'name':'descripcion','size':500},{'name':'nart','size':200}]
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
    try:
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
        res_select = queryHasura(query, {"id" : id })
        if len(res_select["data"]["Maestro_launch"]) < 1:
            return "No existen datos para los parametros igresados"

        size_list = [{'name':'clasificacion','size':120} ,{'name':'canal','size':100},{'name':'descripcion','size':500},{'name':'nart','size':200}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_launch"][0].keys()]
        result = {
            "columns" : colum_list,
            "rows" : res_select["data"]["Maestro_launch"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""
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

    size_list = [{'name':'clasificacion','size':120}, {'name':'canal','size':100},{'name':'application_form','size':120}, {'name':'descripcion','size':500},{'name':'nart','size':200}]
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

    size_list = [{'name':'clasificacion','size':120} , {'name':'descripcion','size':500},{'name':'nart','size':200}]
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
    mutation MyMutation($objects: [Maestro_Shopper_insert_input!] = {}) {
        insert_Maestro_Shopper(objects: $objects, on_conflict: {constraint: Maestro_Shoppers_pkey, update_columns: cantidad}) {
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
        Maestro_Shopper(where: {id: {_eq: $id}}) {
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

    if len(res_select["data"]["Maestro_Shopper"]) < 1:
        return "No existen datos para los parametros igresados"

    size_list = [{'name':'clasificacion','size':120},{'name':'nart','size':170},{'name':'descripcion','size':500}]
    colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_Shoppers"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_Shopper"]
    }
    return result
def deleteDataShoppers(id):
    try:
        query = """
        mutation MyMutation($id: String) {
            delete_Maestro_Shopper(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_Shopper"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""
def requestVisualBD():
    try:
        query = """
        query BD_syop {
            rows: BD_SOP(order_by: {month: asc, year: asc}, where: {}) {
            id
            clasificacion
            BPU
            nart
            nartdesc
            SPGR
            spgrdesc
            year
            month
            BrandCategory
            ApplicationForm
            units
            netsales   
            }
        }
        """
        res = queryHasura(query)
        columns = [{"name": "id","prop": "id","size": 120},{"name": "clasificacion","prop": "clasificacion","size": 200},{"name": "BPU","prop": "BPU","size": 200},{"name": "nart","prop": "nart","size": 200},{"name": "nartdesc","prop": "nartdesc","size": 500},
                   {"name": "SPGR","prop": "SPGR","size": 200},{"name": "spgrdesc","prop": "spgrdesc","size": 500},{"name": "year","prop": "year","size": 120},{"name": "month","prop": "month","size": 120},{"name": "BrandCategory","prop": "BrandCategory","size": 200},
                   {"name": "ApplicationForm","prop": "ApplicationForm","size": 200},{"name": "units","prop": "units","size": 200},{"name": "netsales","prop": "netsales","size": 200}]
        result = {
            "columns" : columns,
            "rows" : res["data"]["rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

def requestPrepareSummary(id):
    try:
        query = """
        query BD_Prepare_Summary($id:String) {
        rows: BD_Prepare_Summary(where: {id:{_eq:$id}}) {
            input
            nart
            descripcion
            year
            mes
            units
            netsales 
        }
        }
        """
        res = queryHasura(query, { 'id' : id })
        result = {"rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""


def demand_simulation_units():
    try:
        query = """
        query unitsxBPU {
        rows: BD_unitsxBPUView {
            year
            BPU
            month
            totmesxbpu
            totq1xbpu
            totq2xbpu
            totq3xbpu
            totq4xbpu
            totanoxbpu
            totano
        }
        }
        """
        res = queryHasura(query)
        size_list = [{'name':'year','size':150},{'name':'BPU','size':250},{'name':'month','size':150},{'name':'totmesxbpu','size':150},{'name':'totq1xbpu','size':150},{'name':'totq2xbpu','size':150},{'name':'totq3xbpu','size':150},{'name':'totq4xbpu','size':150},{'name':'totanoxbpu','size':150},{'name':'totano','size':150}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res["data"]["rows"][0].keys()]
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""


def demand_simulation_netsales():
    try:
        query = """
        query unitsxBPU {
        rows: BD_netsalesxBPUView {
            year
            BPU
            month
            totmesxbpu
            totq1xbpu
            totq2xbpu
            totq3xbpu
            totq4xbpu
            totanoxbpu
            totano
        }
        }
        """
        res = queryHasura(query)
        size_list = [{'name':'year','size':150},{'name':'BPU','size':250},{'name':'month','size':150},{'name':'totmesxbpu','size':150},{'name':'totq1xbpu','size':150},{'name':'totq2xbpu','size':150},{'name':'totq3xbpu','size':150},{'name':'totq4xbpu','size':150},{'name':'totanoxbpu','size':150},{'name':'totano','size':150}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res["data"]["rows"][0].keys()]
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""


def demand_simulation_db():
    try:
        query = """
        query DemandSimulation {
        rows: BD_DemandSimulation {    
            BPU
            year
            month
            quarter
            units
            netsales
        }
        }
        """
        res = queryHasura(query)
        size_list = [{'name':'BPU','size':250},{'name':'year','size':150},{'name':'month','size':150},{'name':'quarter','size':150},{'name':'units','size':150},{'name':'netsales','size':150}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res["data"]["rows"][0].keys()]
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""


def fc_simulation():
    try:
        query = """
        query FC_Simulation {
        rows: FC_Simulation {    
            clasificacion
            year
            enero
            febrero
            marzo
            abril
            mayo
            junio
            julio
            agosto
            septiembre
            octubre
            noviembre
            diciembre
        }
        }
        """
        res = queryHasura(query)
        size_list = [{'name':'clasificacion','size':200},{'name':'year','size':120},{'name':'enero','size':200},{'name':'febrero','size':200},{'name':'marzo','size':200},{'name':'abril','size':200},{'name':'mayo','size':200},{'name':'junio','size':200},{'name':'julio','size':200},{'name':'agosto','size':200},{'name':'septiembre','size':200},{'name':'octubre','size':200},{'name':'noviembre','size':200},{'name':'diciembre','size':200}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res["data"]["rows"][0].keys()]
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""

def db_last_id():
    try:
        query = """
        query BD_LastID {
            rows: BD_LastID(order_by: {month: asc, year: asc}, where: {}) {
                id
                clasificacion
                BPU
                nart
                nartdesc
                SPGR
                spgrdesc
                year
                month
                BrandCategory
                ApplicationForm
                units
                netsales
            }
        }
        """
        res = queryHasura(query)
        size_list = [
            {'name':'id','size':120},{'name':'clasificacion','size':200},{'name':'BPU','size':200},{'name':'nart','size':200},{'name':'nartdesc','size':500},{'name':'SPGR','size':200},{'name':'spgrdesc','size':500},
            {'name':'year','size':120},{'name':'month','size':120},{'name':'BrandCategory','size':200},{'name':'ApplicationForm','size':200},{'name':'units','size':200},{'name':'netsales','size':200}
        ]
        colum_list = []
        for col in res["data"]["rows"][0].keys():
            if col == 'units':
                colum_list.append({'name':col,'prop':col,'size':getSizebyColumnName(size_list,col),'autoSize':True,'sortable':True,'readonly':False})
            elif col not in [x['name'] for x in size_list]:
                colum_list.append({'name': col,'prop': col,'autoSize':True,'sortable':True,'readonly':True})
            else:
                colum_list.append({'name':col,'prop':col,'size':getSizebyColumnName(size_list,col),'autoSize':True,'sortable':True,'readonly':True})
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""


def addRow(row):
    try:
        table_name = row['clasificacion']
        if table_name == 'BASELINE':
            query = """mutation MyMutation($objects: [Maestro_baseline_insert_input!]!) { insert_Maestro_baseline(objects: $objects) {affected_rows}} """
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_baseline']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0
        elif table_name == 'LAUNCH':
            query = """mutation MyMutation($objects: [Maestro_launch_insert_input!]!) {insert_Maestro_launch(objects: $objects) {affected_rows }}"""
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_launch']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0   
        elif table_name == 'PROMO':
            query = """mutation MyMutation($objects: [Maestro_promo_insert_input!]!) {insert_Maestro_promo(objects: $objects) {affected_rows}}"""
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_promo']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0
        elif table_name == 'SHOPPER':
            query = """mutation MyMutation($objects: [Maestro_Shopper_insert_input!]!) {insert_Maestro_Shopper(objects: $objects) {affected_rows}}"""
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_Shopper']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0   
        elif table_name == 'VALORIZACION':
            query = """mutation MyMutation($objects: [Maestro_valorizacion_insert_input!]!) {insert_Maestro_valorizacion(objects: $objects) {affected_rows}}"""
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_valorizacion']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0
    except SyntaxError as err:
        print(f' Error addRow {err}')
        return 0


def updateInputTable(table_name, rows):
    try:
        if table_name == 'BASELINE':
            rows_affected = 0
            for row in rows:
                query = """ 
                mutation MyMutation($id:String, $nart: String, $year: numeric, $month: numeric, $cantidad: numeric) {
                update_Maestro_baseline(where: {id: {_eq: $id}, nart: {_eq: $nart}, year: {_eq: $year}, month: {_eq: $month}}, _set: {cantidad: $cantidad}) {affected_rows}}
                """
                res = queryHasura(query, { 'id': row['id'], 'nart': row['nart'], 'year': row['year'], 'month': row['month'], 'cantidad': row['cantidad']})
                rows_affected += res['data']['update_Maestro_baseline']['affected_rows']
            return rows_affected
        elif table_name == 'LAUNCH':
            rows_affected = 0
            for row in rows:
                query = """ 
                mutation MyMutation($id:String, $nart: String, $year: numeric, $month: numeric, $cantidad: numeric) {
                update_Maestro_launch(where: {id: {_eq: $id}, nart: {_eq: $nart}, year: {_eq: $year}, month: {_eq: $month}}, _set: {cantidad: $cantidad}) {affected_rows}} 
                """
                res = queryHasura(query, { 'id': row['id'], 'nart': row['nart'], 'year': row['year'], 'month': row['month'], 'cantidad': row['cantidad']})
                rows_affected += res['data']['update_Maestro_launch']['affected_rows']
            return rows_affected
        elif table_name == 'PROMO':
            rows_affected = 0
            for row in rows:
                query = """ 
                mutation MyMutation($id: String, $nart: String = "", $year: numeric = "",$month: numeric = "", $cantidad: numeric = "") {
                update_Maestro_promo(where: {id: {_eq: $id}, nart: {_eq: $nart}, year: {_eq: $year}, month: {_eq: $month}, cantidad: {_eq: $cantidad}}) {affected_rows}}
                """
                res = queryHasura(query, { 'id': row['id'], 'nart': row['nart'], 'year': row['year'], 'month': row['month'], 'cantidad': row['cantidad']})
                rows_affected += res['data']['update_Maestro_promo']['affected_rows']
            return rows_affected
        elif table_name == 'SHOPPER':
            rows_affected = 0
            for row in rows:
                query = """ 
                mutation MyMutation($id: String = "", $nart: String = "", $year: numeric = "", $month: numeric = "", $cantidad: numeric = "") {
                update_Maestro_Shopper(where: {id: {_eq: $id}, nart: {_eq: $nart}, year: {_eq: $year}, month: {_eq: $month}, cantidad: {_eq: $cantidad}}) {affected_rows}}
                """
                res = queryHasura(query, { 'id': row['id'], 'nart': row['nart'], 'year': row['year'], 'month': row['month'], 'cantidad': row['cantidad']})
                rows_affected += res['data']['update_Maestro_Shopper']['affected_rows']
            return rows_affected
        # elif table_name == 'VALORIZACION':
        #     rows_affected = 0
        #     for row in rows:
        #         query = """ 
        #         mutation MyMutation($id: String = "", $clasificacion: String = "", $nart: String = "", $desc: String = "", $year: numeric = "", $month: numeric = "", $value: String = "", $cantidad: numeric = "") {
        #         update_Maestro_valorizacion(where: {id: {_eq: $id}, clasificacion: {_eq: $clasificacion}, nart: {_eq: $nart}, descripcion: {_eq: $desc}, year: {_eq: $year}, month: {_eq: $month}, value: {_eq: $value}, cantidad: {_eq: $cantidad}}) {affected_rows}}
        #         """
        #         res = queryHasura(query, { 'id': row['id'], 'clasificacion': row['clasificacion'], 'nart': row['nart'], 'desc': row['descripcion'], 'year': row['year'], 'month': row['month'], 'cantidad': row['cantidad']})
        #         rows_affected += res['data']['update_Maestro_launch']['affected_rows']
        #     return rows_affected
    except SyntaxError as err:
        print(err)
        return 0

def graph_dataset():
    try:
        query = """
        query
        {
            Grafico_de_Barras_SellIn(order_by:{
                month: desc,
                year: desc
            }) {
                year,
                month,
                sum,
                clasificacion
            }
            Grafico_de_Tendencia_Sellout(order_by:{
                month: desc,
                year: desc
            }) {
                year,
                month,
                sum
            }
        }
        """
        res = queryHasura(query)
        datasets = []
        data = res["data"]
        datos_fijos = { 'REALES': {
                            '2019': {'backgroundColor':'#77aaff','stack':'Stack 0', 'label': "Sell in 2019"},
                            '2020':{'backgroundColor':"#3366ff",'stack':'Stack 1','label': "Sell in 2020"}, 
                            '2021':{'backgroundColor':"#3366ff",'stack':'Stack 2', 'label': "Sell in 2021"}},               
                        'BASELINE':{'backgroundColor': "red",'stack': 'Stack 2', 'label': "Baseline"},
                        'SHOPPER':{'backgroundColor': "green",'stack': 'Stack 2', 'label': "Shopper"},
                        'LAUNCH':{'backgroundColor': "yellow", 'stack': 'Stack 2', 'label': "Launch"},
                        'PROMO': {'backgroundColor': "purple", 'stack': 'Stack 2', 'label': "Promo"},
                        'SELLOUT':{'type': 'line', 'label': "Sell Out 2021"}    }
        sellin = data['Grafico_de_Barras_SellIn']
        sellout = sorted(data['Grafico_de_Tendencia_Sellout'], key=lambda i: i['month'])

        year = f'{datetime.now().strftime("%Y")}'
        month1 = f'{datetime.now().strftime("%m")}'
        month2 = f'{(datetime.now().replace(day=1) - timedelta(days=1)).strftime("%m")}'

        def fillMonths(array):
            month_range = [ i for i in range(12)]
            array_range = []
            for m in month_range:
                try:
                    if array[m]['month']-1 in month_range:
                        array_range.append(array[m]['sum'])
                except:
                        array_range.append(0)
            return array_range

        for input in datos_fijos:
            if input == 'REALES':
                years = list(set([ str(x['year']) for x in sellin if x['clasificacion'] == "REALES"]))
                for k in datos_fijos['REALES']:
                    dataset = datos_fijos['REALES'][k]
                    if k in years:
                        data = [ { 'sum':x['sum'], 'year':x['year'], 'month':x['month'] } for x in sorted(sellin, key=lambda i: i['month']) if x['clasificacion'] == "REALES" and x['year'] == int(k) ]
                        filled_data = fillMonths(data)
                        dataset['data'] = filled_data
                    else:
                        dataset['data'] = [0] * 12
                    datasets.append(dataset)
            else:
                if input == 'SELLOUT':
                    dataset = datos_fijos[input]
                    data = [ { 'sum':x['sum'], 'year':x['year'], 'month':x['month'] } for x in sellout if x['year'] == int(year)]
                    filled_data = fillMonths(data)
                    dataset['data'] = filled_data
                elif input != '':
                    data = sorted([{ 'sum': i['sum'], 'year':i['year'], 'month':i['month']} for i in sellin if i["clasificacion"] == input and i["year"] == int(year) and str(i["month"]) in [month1, month2]], key=lambda i: i['month'])
                    dataset = datos_fijos[input]
                    dataset['data'] = fillMonths(data)
                else:
                    dataset = datos_fijos[input]
                    dataset['data'] = [0] * 12
                datasets.append(dataset)
        return datasets
    except SystemError as err:
        print(err)
        return ""
    except:
        print(sys.exc_info())
        return ""

def request_action_test(numbers):
    try:
        return { 'sum': sum(numbers) }, 200
    except:
        return { 'error': 'error sumando numeros' }, 400

def sendDataForecast(data):
    # SendInsert
    query = """
    mutation MyMutation($objects: [Forecast_insert_input!] = {}) {
    insert_Forecast(objects: $objects, on_conflict: {constraint: Forecast_pkey, update_columns: [r_o, mso, net_sales]}) {
        affected_rows
    }
    }
    """
    res_insert = queryHasura(query, {"objects" : data})
    result = { "file_id" : res_insert["data"]["insert_Forecast"]["affected_rows"], "area_name" : "Forecast" }
    return result

def requestinfo_db_main(clasificacion, year, month):
    try:
        query = """
        query MyQuery($clasificacion: String, $year: Int, $month: Int) {
        DB_Main(where: {clasificacion: {_eq: $clasificacion}, year: {_eq: $year}, month: {_eq: $month}}) {
            id
            clasificacion
            bpu
            brand_category
            application_form
            year
            month
            promo_spgr
            units
            netsales
            ajuste_netsales
            comentario
        }
        }
        """
        res_insert = queryHasura(query, {"clasificacion": clasificacion, "year": year, "month": month})
        print(res_insert)
        result = { 'result': res_insert["data"]["DB_Main"]}
        return result
    except:
        print(sys.exc_info())
        return 0

def update_db_main_table(data):
    try:
        query = """
        mutation MyMutation($objects: [DB_Main_insert_input!] = {}) {
        insert_DB_Main(objects: $objects, on_conflict: {constraint: DB_Main_pkey, update_columns: [netsales, ajuste_netsales]}) {
            affected_rows
        }
        }
        """
        res = queryHasura(query, {'objects': data})
        #print('(update_db_main_table) : ', res)
        return res
    except:
        print(sys.exc_info())
        return 0
