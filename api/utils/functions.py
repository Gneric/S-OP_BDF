from api.utils.dataLoader import *
from os import getcwd, scandir, remove, listdir
from os.path import join
import pandas as pd
import bcrypt

data_path = join(getcwd(),'api','data')
template_path = join(getcwd(),'api','templates')
def cleanDataFolder():
    for file in scandir(data_path):
        remove(file)

ALLOWED_EXT = set(['xlsx','xls'])
def allowed_extensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

ALLOWED_NAMES = set(['BASELINE','LAUNCH','PROMO','VALORIZACION','PRODUCTOS'])
def allowed_names(filename):
    return '.' in filename and filename.rsplit(' - ', 1)[0] in ALLOWED_NAMES

def checkFiles():
    return len(listdir(data_path))


db_table_area = {
    "1" : "baseline",
    "2" : "launch",
    "3" : "promo",
    "4" : "valorizacion",
    "5" : "shoppers"
}
def checkExcelFiles(area_id, year, month):
    for f in scandir(data_path):
        xl = pd.ExcelFile(f)
        for sheet in xl.sheet_names:
            if sheet == 'Hoja1':
                df = pd.read_excel(f, sheet)
                if area_id == 1:
                    return Loadbaseline(df, year, month)
                if area_id == 2:
                    return LoadLaunch(df, year, month)
                if area_id == 3:
                    return LoadPromo(df, year, month)
                if area_id == 4:
                    return LoadValorizacion(df, year, month)
                if area_id == 5:
                    return LoadShoppers(df, year, month)
                else:
                    return "El Area ID enviado no se encuentra en el listado de IDs aprovados", "error"
            else:
                return "No se encontro la hoja con el nombre correcto 'Hoja 1'", "error"

def getData(id, area_id):
    print(area_id)
    if area_id == 1:
        return requestDataBaseline(id)
    if area_id == 2:
        return requestDataLaunch(id)
    if area_id == 3:
        return requestDataPromo(id)
    if area_id == 4:
        return requestDataValorizacion(id) 
    if area_id == 5:
        return requestDataShoppers(id) 
    else:
        return ""

def checkInfoMonth(year, month):
    if int(month) < 10 and len(month) == 1:
        month = f"0{int(month)}"
    info = requestIDbyPeriod(f"{year}{month}")
    return { 'result' : info }


def checkDeleteTable(area_id, year, month):
    area_id = int(area_id)
    if int(month) < 10 and len(month) == 1:
        month = f"0{int(month)}"
    if area_id == 1:
        return deleteDataBaseline(year+month)
    if area_id == 2:
        return deleteDataLaunch(year+month)
    if area_id == 3:
        return deleteDataPromo(year+month)
    if area_id == 4:
        return deleteDataValorizacion(year+month)
    if area_id == 5:
        return deleteDataShoppers(year+month)
    else:
        return ""

def cloneData(file_id, area_id):
    try:
        data = []
        if area_id == 1:
            data = requestDataBaseline(file_id)
        if area_id == 2:
            data = requestDataLaunch(file_id)
        if area_id == 3:
            data = requestDataPromo(file_id)
        if area_id == 4:
            data = requestDataValorizacion(file_id)
        if area_id == 5:
            data = requestDataShoppers(file_id)
        if data == []:
            return "area_id not found"
        column_list = list(data["rows"][0].keys())
        values = [ list(i.values()) for i in data["rows"] ]
        xslx_name = f"{db_table_area[str(area_id)]}.xlsx"
        xslx_path = join(data_path, xslx_name)
        print(xslx_path)
        excel_path = createExcelFile(values,column_list,file_id,xslx_path)
        if excel_path == "":
            return ""
        return xslx_name
    except:
        return sys.exc_info()[1]
    

def getTemplates(year, month, area_id):
    try:
        path = createTemplate(f"{db_table_area[str(area_id)]}.xlsx", template_path, data_path, year, month)
        if path == "":
            return ""
        return path
    except:
        print(sys.exc_info()[1])
        return ""

def logUser(email, password):
    user_info = checkPassword(email)
    if user_info == "":
        return { 'error' : 'No existe usuario' }
    else:
        if bcrypt.checkpw(password.encode('utf-8'), user_info.get('hash_password').encode('utf-8')):
            return checkUser(email)
        else:
            raise

def signUser(username, mail, phone, password):
    try:
        hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(f"hash_password for user {username} : {hash_pwd}")
        user = {
            "userName": username,
            "mail": mail,
            "phone": phone,
            "hash_password" : hash_pwd,
            "profileImageUrl": "",
            "userTypeId": 1
        }
        result = insertUser(user)
        if result=="":
            raise
        else:
            return result
    except:
        print(sys.exc_info()[1])
        return "Failed to registerUser"

def userInfo(id = ""):
    try:
        if id == "":
            res = listUsers("")
            return { 'result' : res }
        else:
            res = listUsers(id)
            return { 'result' : res }
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
            return { "error": "error al modificar el usuario" }
        else:
            return { "result" : "ok" }
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al retornar respuesta del servidor" }

def pwdChange(user_id, pwd, new_pwd):
    try:
        user_info = checkPasswordByID(user_id)
        if user_info == "":
            return { 'error' : 'No existe usuario' }
        else:
            if bcrypt.checkpw(pwd.encode('utf-8'), user_info.get('hash_password').encode('utf-8')):
                res = changepw(user_id, bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt()))
                if res == "":
                    return { "error", "error al cambiar la contraseña" }
                else:
                    return { "result" : "ok" }
            else:
                { "error" : "La contraseña ingresada con coincide con la contraseña actual" }
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al cambiar la contraseña del usuario" }