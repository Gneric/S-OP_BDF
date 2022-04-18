import sys

from src.api.hasura_queries.base_query import queryHasura

def checkMailExists(email):
    try:
        query = """
        query MyQuery($email: String) {
        Users(where: {mail: {_eq: $email}}) {
        userName
        }
        }
        """
        res_insert = queryHasura(query, {"email" : email})
        print(res_insert)
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
        print(res_insert)
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

def listUsers(data):
    q = "%"+data.get('q')+"%"
    sort = 'asc' if data['sortDesc'] == False else 'desc'
    variables = f"limit: {data['perPage']}, offset: {(data['page'] - 1)}, order_by: "+"{"+data['sortBy']+": "+sort+"}"
    try:
        query = """
        query MyQuery($ilike: String = "") {
        Users("""+variables+""", where: {_or: [{userName: {_ilike: $ilike}}, {name: {_ilike: $ilike}}, {mail: {_ilike: $ilike}}]}) {
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
        res = queryHasura(query, { 'ilike': q })
        users = res["data"]["Users"]
        query = "query MyQuery { Users { userID } }"
        res_total = queryHasura(query)
        total = len(res_total['data']['Users'])
        res = []
        for u in users:
            res.append({'userID': u['userID'],'profileImageUrl': u['profileImageUrl'], 'userName': u['userName'], 'name':u['name'], 'mail':u['mail'], 'isEnabled':u['isEnabled'], 'role': u['role'] })
        return { 'users' : res, 'total': total }
    except:
        print(sys.exc_info()[1])
        return []

def listUserbyID(id):
    try:
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