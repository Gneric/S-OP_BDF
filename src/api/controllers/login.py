
import bcrypt
from src.api.hasura_queries.login import *


def logUser(email, password):
    user_info = checkPassword(email)
    if user_info == None:
        return None
    else:
        if bcrypt.checkpw(password.encode('utf-8'), user_info.get('hash_password').encode('utf-8')):
            return checkUser(email)
        else:
            return None

def generate_token(user):
    is_admin = user['role'] == "Admin"
    user_roles = ["user"]
    admin_roles = ["user","admin"]
    payload =  str(user['id'])
    hasura_token = {
        "hasura_claims": {
            "x-hasura-allowed-roles" : admin_roles if is_admin else user_roles,
            "x-hasura-default-role": "admin" if is_admin else "user",
            "x-hasura-user-id": str(user['id'])
        }
    }
    return payload, hasura_token