from api.utils.hasura_api import *
from api.utils.dataLoader import LoadForecast, LoadLaunch, LoadPromo, LoadShoppers, LoadValorizacion, Loadbaseline, createExcelFile, createTemplate, createTemplateValorizacion
from os import getcwd, scandir, remove, listdir
from os.path import join
import pandas as pd
import bcrypt
from datetime import date, datetime

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


db_table_area = {"1":"baseline" ,"2":"launch", "3":"promo", "4":"valorizacion", "5":"shopper"}

def checkExcelFiles(area_id, year, month, current_user):
    for f in scandir(data_path):
        xl = pd.ExcelFile(f)
        for sheet in xl.sheet_names:
            if sheet == 'Hoja1' or sheet == db_table_area[str(area_id)]:
                df = pd.read_excel(f, sheet)
                if area_id == 1:
                    res = Loadbaseline(df, year, month)
                    if res != "":
                        audit_inputs({"id": current_user, "date": datetime.now(), "accion": "INSERT", "clasificacion": "BASELINE"})
                    return 
                if area_id == 2:
                    res = LoadLaunch(df, year, month)
                    if res != "":
                        audit_inputs({"id": current_user, "date": datetime.now(), "accion": "INSERT", "clasificacion": "LAUNCH"})
                    return 
                if area_id == 3:
                    res = LoadPromo(df, year, month)
                    if res != "":
                        audit_inputs({"id": current_user, "date": datetime.now(), "accion": "INSERT", "clasificacion": "PROMO"})
                    return 
                if area_id == 4:
                    res = LoadValorizacion(df, year, month)
                    if res != "":
                        audit_inputs({"id": current_user, "date": datetime.now(), "accion": "INSERT", "clasificacion": "VALORIZACION"})
                    return 
                if area_id == 5:
                    res = LoadShoppers(df, year, month)
                    if res != "":
                        audit_inputs({"id": current_user, "date": datetime.now(), "accion": "INSERT", "clasificacion": "SHOPPER"})
                    return 
                if area_id == 9:
                    res = LoadForecast(df, year, month)
                    if res != "":
                        audit_inputs({"id": current_user, "date": datetime.now(), "accion": "INSERT", "clasificacion": "FORECAST"})
                    return 
                else:
                    return "El Area ID enviado no se encuentra en el listado de IDs aprovados", "error"
            else:
                return f"No se encontro la hoja con el nombre correcto 'Hoja 1' / {db_table_area[area_id]}", "error"

def getData(id, area_id):
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


def checkDeleteTable(area_id, year, month, current_user):
    area_id = int(area_id)
    if int(month) < 10 and len(month) == 1:
        month = f"0{int(month)}"
    if area_id == 1:
        res = deleteDataBaseline(year+month)
        if res != "":
            audit_inputs({"id": current_user, "date": datetime.now(), "accion": "DELETE", "clasificacion": "BASELINE"})
        return res
    if area_id == 2:
        res = deleteDataLaunch(year+month)
        if res != "":
            audit_inputs({"id": current_user, "date": datetime.now(), "accion": "DELETE", "clasificacion": "LAUNCH"})
        return res
    if area_id == 3:
        res = deleteDataPromo(year+month)
        if res != "":
            audit_inputs({"id": current_user, "date": datetime.now(), "accion": "DELETE", "clasificacion": "PROMO"})
        return res
    if area_id == 4:
        res = deleteDataValorizacion(year+month)
        if res != "":
            audit_inputs({"id": current_user, "date": datetime.now(), "accion": "DELETE", "clasificacion": "VALORIZACION"})
        return res
    if area_id == 5:
        res = deleteDataShoppers(year+month)
        if res != "":
            audit_inputs({"id": current_user, "date": datetime.now(), "accion": "DELETE", "clasificacion": "SHOPPER"})
        return res
    else:
        return ""

def cloneData(file_id, area_id, current_user):
    try:
        data = []
        if area_id == 1:
            data = requestDataBaseline(file_id)
            if data != "":
                audit_inputs({"id": current_user, "date": datetime.now(), "accion": f"CLONE {file_id}", "clasificacion": "BASELINE"})
        if area_id == 2:
            data = requestDataLaunch(file_id)
            if data != "":
                audit_inputs({"id": current_user, "date": datetime.now(), "accion": f"CLONE {file_id}", "clasificacion": "LAUNCH"})
        if area_id == 3:
            data = requestDataPromo(file_id)
            if data != "":
                audit_inputs({"id": current_user, "date": datetime.now(), "accion": f"CLONE {file_id}", "clasificacion": "PROMO"})
        if area_id == 4:
            data = requestDataValorizacion(file_id)
            if data != "":
                audit_inputs({"id": current_user, "date": datetime.now(), "accion": f"CLONE {file_id}", "clasificacion": "VALORIZACION"})
        if area_id == 5:
            data = requestDataShoppers(file_id)
            if data != "":
                audit_inputs({"id": current_user, "date": datetime.now(), "accion": f"CLONE {file_id}", "clasificacion": "SHOPPER"})
        if data == []:
            return "area_id not found"
        column_list = list(data["rows"][0].keys())
        values = [ list(i.values()) for i in data["rows"] ]
        xslx_name = f"{db_table_area[str(area_id)]}.xlsx"
        xslx_path = join(data_path, xslx_name)
        excel_path = createExcelFile(values,column_list,file_id,xslx_path)
        if excel_path == "":
            return ""
        return xslx_name
    except:
        return sys.exc_info()[1]
    

def getTemplates(year, month, area_id):
    try:
        if year == "":
            year = str(datetime.today().strftime('%Y'))
        if month == "":
            month = str(datetime.today().strftime('%m'))
        if db_table_area[str(area_id)] == 'valorizacion':
            return createTemplateValorizacion(f"{db_table_area[str(area_id)]}.xlsx", template_path, data_path, year, month)
        if db_table_area[str(area_id)] != 'valorizacion':
            return createTemplate(f"{db_table_area[str(area_id)]}.xlsx", template_path, data_path, year, month)
    except:
        print(sys.exc_info()[1])
        return ""

def logUser(email, password):
    user_info = checkPassword(email)
    if user_info == None:
        return None
    else:
        if bcrypt.checkpw(password.encode('utf-8'), user_info.get('hash_password').encode('utf-8')):
            return checkUser(email)
        else:
            return None

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

def getVisualBD():
    return db_last_id()

def get_db_historico():
    return requestVisualBD()

def getPrepareSummary(id):
    return requestPrepareSummary(id)

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

def getActionTest(numbers):
    return request_action_test(numbers)

def getPermissionbyActions(action):
    try:
        permission_list = getPermissions(action)
        return  { 'result' : permission_list }, 200
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al retornar permisos" }, 400

def updatePermissions(permissions):
    try:
        rows_affected = updatePermissionByList(permissions)
        if rows_affected == "":
            return { "error" : "Error al actualizar permisos" }, 400
        else:
            return { 'result' : 'ok' }, 200
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al actualizar permisos" }, 400

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

def add_new_row(data):
    try:
        table_name = data['clasificacion']
        id = f'{datetime.now().strftime("%Y%m")}'
        if table_name == 'BASELINE':
            return addRow({'id':id,'clasificacion':table_name,'nart':data['nart'],'descripcion':data['descripcion'],'year':data['year'],'month':data['month'],'cantidad':data['cantidad']})
        elif table_name == 'LAUNCH':
            return addRow({'id':id,'clasificacion':table_name, 'canal': data['canal'], 'nart':data['nart'],'descripcion':data['descripcion'],'year':data['year'],'month':data['month'],'cantidad':data['cantidad']})
        elif table_name == 'PROMO':
            return addRow({'id':id, 'clasificacion':table_name, 'tipo_promo':data['tipo_promo'], 'canal': data['canal'], 'application_form': data['application_form'], 'nart':data['nart'], 'descripcion':data['descripcion'], 'year':data['year'], 'month':data['month'], 'cantidad':data['cantidad']})
        elif table_name == 'VALORIZACION':
            return addRow({'id':id,'clasificacion':table_name,'nart':data['nart'],'descripcion':data['descripcion'],'year':data['year'],'month':data['month'],'value':data['value'],'cantidad':data['cantidad']})
        elif table_name == 'SHOPPER':
            return addRow({'id':id,'clasificacion':table_name, 'tipo_promo':data['tipo_promo'], 'canal': data['canal'], 'nart':data['nart'],'descripcion':data['descripcion'],'year':data['year'],'month':data['month'], 'cantidad':data['cantidad']})
    except KeyError as err:
        print(f' Error add_new_row {err}')
        return 0


def update_changes_bd(data):
    try:
        result = {}
        upd_table = []
        upd_table.append({ 'name': 'BASELINE', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units']} for x in data if x['clasificacion']=='BASELINE']})
        upd_table.append({ 'name': 'LAUNCH', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units']} for x in data if x['clasificacion']=='LAUNCH']})
        upd_table.append({ 'name': 'PROMO', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units'] } for x in data if x['clasificacion']=='PROMO']})
        upd_table.append({ 'name': 'VALORIZACION', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units'] } for x in data if x['clasificacion']=='VALORIZACION']})
        upd_table.append({ 'name': 'SHOPPER', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units'] } for x in data if x['clasificacion']=='SHOPPER']})
        for table in upd_table:
            if len(table['rows']) > 0:
                result[table['name']] = updateInputTable(table['name'], table['rows'])
        return result
    except:
        print(sys.exc_info())
        return { 'error', 'error actualizando data' }, 400

def getinfo_db_main(data):
    try:
        return requestinfo_db_main(data['clasificacion'], data['year'], data['month'], data['bpu'], data['brand_category'], data['application_form'])
    except:
        print(sys.exc_info())
        return { 'error', 'error actualizando data' }, 400

def update_db_main(data):
    try:
        id = data[0]['id'] 
        for i in data:
            if i['id'] == 0: #Si es comodin
                if i['promo_spgr'] == "" or i['ajuste_netsales'] == 0:
                    data,remove(i)
                else:
                    i['id'] = id
        update = update_db_main_table(data)
        #audit = audit_db_main(data)
        return update
    except:
        print(sys.exc_info())
        return { 'error', 'error actualizando data' }, 400

def request_cargar_db_main():
    try:
        data = request_data_last_id()
        curr_month = f'{datetime.now().strftime("%Y%m")}'
        if data == [] or data[0]["id"] < curr_month :
            return { 'error', 'no se encontro data en el mes actual' }, 400
        else:
            del_res = delete_db_main_id(data[0]["id"])
            res = insert_data_db_main(data)
            return { 'ok', f'{res} filas ingresadas a la tabla de datos Maestra'}, 200
    except:
        return { 'error', 'error cargando nuevos datos' }, 400
