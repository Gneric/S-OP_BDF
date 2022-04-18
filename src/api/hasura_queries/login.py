import sys
from src.api.hasura_queries.base_query import queryHasura

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