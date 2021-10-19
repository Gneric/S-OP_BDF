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
        print(res_insert)
        
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
    print('Entering checkUser')
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
        search_permissions(args: {email: $email}) {
            action
            subject
            conditions
        }
        }
        """
        res_insert = queryHasura(query, {"email" : email})
        result = res_insert["data"]["Users"][0]
        permissions = res_insert["data"]["search_permissions"]
        abilities = [ { "action": i['action'], "subject": i['subject'], "conditions": i['conditions'] } if i['conditions'] else { "action": i['action'], "subject": i['subject'] } for i in permissions ]
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
            print('Entering if id exists')
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
            permissions = [ { "permissionID": i['permissionID'], "action": i['action'], "subject": i['subject'], 'isEnabled': i['isEnabled'], "condition": i['condition'] } if i['condition'] else { "permissionID": i['permissionID'], "action": i['action'], "subject": i['subject'], 'isEnabled': i['isEnabled'] } for i in abilities ]
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
            print('Entering if id doenst exist')
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
                    UserType {
                        userTypeName
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
