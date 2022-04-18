
import bcrypt
from src.api.hasura_queries.login import checkPassword
from src.api.hasura_queries.users import *
 

def createUser(new_user):
    try:
        hash_pwd = bcrypt.hashpw(new_user['password'].encode('utf-8'), bcrypt.gensalt())
        decoded_pwd = hash_pwd.decode('utf-8')
        user = {
            "mail": new_user['mail'],
            "hash_password": decoded_pwd,
            "userName": new_user['username'],
            "phone": new_user['phone'],
            "isEnabled": new_user['isEnabled'],
            "name": new_user['name'],
            "role": new_user['role']
        }
        check_mail = checkMailExists(user['mail'])
        if check_mail != "":
            return { 'error' : 'el correo ingresado ya se encuentra registrado' }, 400
        res = insertUser(user)
        if res != "":
            return { 'result': "ok" }, 200
        else:
            return { 'error': 'error ingresando usuario' }, 400
    except:
        print(sys.exc_info()[1])
        return { 'error' : 'Failed to registerUser' }, 400

def userInfo(data = {}, id = ""):
    try:
        if data != {}:
            res = listUsers(data)
            return { 'result' : res }
        if id != "":
            res = listUserbyID(id)
            return { 'result' : res }
        else:
            return { 'error': 'no se encontro data para la busqueda' }, 400
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al retornar informacion de ususarios" }
 
def modUser(user, permissions):
    try:
        pwd = checkPassword(user['mail'])
        user['hash_password'] = pwd["hash_password"]
        permission2 = [{'userID': user['userID'], 'permissionID': p['permissionID'], 'isEnabled': p['isEnabled']} for p in permissions ]
        res = modifyUser(user, permission2)
        if res == "":
            return { "error": "error al modificar el usuario" }, 400
        else:
            return { "result" : "ok" }
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al retornar respuesta del servidor" }, 400

def pwdChange(user_id, pwd, new_pwd):
    try:
        user_info = checkPasswordByID(user_id)
        if user_info == "":
            return { 'error' : 'No existe usuario' }
        if bcrypt.checkpw(pwd.encode('utf-8'), user_info.get('hash_password').encode('utf-8')):
            hashed_pwd = bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt())
            decoded_pwd = hashed_pwd.decode("utf-8")
            res = changepw(user_id, hashed_pwd.decode('utf-8'))
            if res != "":
                return { "result" : "ok" }, 200
            else:
                return { "error", "error al cambiar la contraseña" }, 400
        else:
            { "error" : "La contraseña ingresada con coincide con la contraseña actual" }, 400
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al cambiar la contraseña del usuario" }, 400

